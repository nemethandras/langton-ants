#!/usr/bin/env python3

# Python imports ###############################################################

import sys
import re

# program imports ##############################################################

from components.cell import Cell
from components.ant import Ant
from utils.outputmessages import OutputMessages as msg
from utils.regex import Regex as regex

################################################################################
#  Langton Ants ################################################################
################################################################################
#  An extended version of the original Langton Ants simulation #################
################################################################################

# global variables #############################################################

rule = [270, 90, 315, 45, 90]
speedup = 2
cell_grid = list()
cell_grid_height = -1 # invalid initial value for checking #
cell_grid_width = -1 # invalid initial value for checking #
ant_list = list()
round_count = 0

# regular expression matchers ##################################################

REGEX_RULE_CLA = re.compile("^rule=(?P<value>((45|90|270|315)-){4}(45|90|270|315))")
REGEX_SPEEDUP_CLA = re.compile("^speedup=(?P<value>[1-9][0-9]*)")

REGEX_COLOR_ANY = re.compile("(?P<color>[0-4])")
REGEX_OBSTACLE = re.compile("(?P<symbol>\\*)")
REGEX_COORDINATES = re.compile("(?P<row>0|[1-9][0-9]*),(?P<column>0|[1-9][0-9]*)")
REGEX_COUNT = re.compile("(?P<count>([0-9]|[1-9][0-9]*))")

REGEX_ANT_ANY = re.compile("(?P<name>[a-zA-Z])")
REGEX_ANT_DATA = re.compile("(?P<name>[a-zA-Z]),(?P<row>(0|[1-9][0-9]*)),(?P<column>(0|[1-9][0-9]*))")

# control function definitions #################################################

# get_ant ######################################################################

def get_ant(arg_ant_name):

    ant_name = arg_ant_name.lower()

    for current_ant in ant_list:
        if current_ant.get_name() == ant_name:
            return current_ant

    # if an ant was not found, None is returned #
    return None

# perform_ant_actions ##########################################################

def perform_ant_actions(arg_ant):

    global cell_grid

    if arg_ant is None:
        return None

    ant_origin_pos_row = arg_ant.get_pos_row()
    ant_origin_pos_column = arg_ant.get_pos_column()
    ant_origin_cell = cell_grid[ant_origin_pos_row][ant_origin_pos_column]

    ant_target_pos_row = ant_origin_pos_row + arg_ant.get_target_pos_row_relation()
    ant_target_pos_column = ant_origin_pos_column + arg_ant.get_target_pos_column_relation()

    try:
        ant_target_cell = cell_grid[ant_target_pos_row][ant_target_pos_column]
    except IndexError as err:
        msg.error(str(err))
        ui_function_escape(list(arg_ant.get_name()))
        return None

    # move if possible #
    if ant_target_cell.has_occupying_ant() or ant_target_cell.is_obstacle():
        ant_target_cell = ant_origin_cell
        ant_target_pos_row = ant_origin_pos_row
        ant_target_pos_column = ant_origin_pos_column
    else:
        arg_ant.set_position(ant_target_pos_row, ant_target_pos_column)

        ant_origin_cell.remove_occupying_ant()
        ant_target_cell.set_occupying_ant(arg_ant)

    # turn
    ant_target_cell_original_color = ant_target_cell.get_color()
    arg_ant.change_orientation(rule[ant_target_cell_original_color], cell_grid_height, cell_grid_width)

    # change cell color based on formula #
    ant_target_cell.recalculate_color()

    # if everything went in order, return ant for a possible new iteration #
    return arg_ant

# decorator: print_grid_after ##################################################

def print_grid_after(arg_function):
    def new_function(arguments):
        arg_function(arguments)
        ui_function_print(list())
    return new_function

# decorator: print_result ######################################################

def print_result(arg_function):
    def new_function(arguments):
        result = arg_function(arguments)
        if result is not None:
            print(str(result))
    return new_function

# user interface definitions ###################################################

# ui_function_quit #############################################################

def ui_function_quit(arguments):

    if len(arguments) > 0:
        msg.warning("too many parameters")
        return

    sys.exit(0)
### BREAKPOINT #

# ui_function_print ############################################################

# reference function for @printGridAfter
def ui_function_print(arguments):

    global cell_grid

    if len(arguments) > 0:
        msg.warning("too many parameters")
        return

    for row_no in range(0, cell_grid_height):
        row_string = ""

        for col_no in range(0, cell_grid_width):
            cell = cell_grid[row_no][col_no].get_representation()

            row_string += cell

        print(row_string)

# ui_function_ant ##############################################################

@print_result
def ui_function_ant(arguments):

    global ant_list

    if len(arguments) > 0:
        msg.warning("too many parameters")
        return None

    result_string = ""

    for i in range(0, len(ant_list)):
        current_ant = ant_list[i]
        result_string += current_ant.get_name()

        if i < len(ant_list) - 1:
            result_string += ", "

    return "The following ants are on the grid: " + result_string

# ui_function_reset ############################################################

@print_grid_after
def ui_function_reset(arguments):

    global cell_grid

    if len(arguments) > 0:
        msg.warning("too many parameters")
        return

    for n1 in range(0, cell_grid_height):
        for n2 in range(0, cell_grid_width):
            cell_grid[n1][n2].reset_color()

    msg.info("the grid cells have been reset")

# ui_function_random ###########################################################

@print_grid_after
def ui_function_random(arguments):

    global cell_grid

    if len(arguments) > 0:
        msg.warning("too many parameters")
        return

    for n1 in range(0, cell_grid_height):
        for n2 in range(0, cell_grid_width):
            cell_grid[n1][n2].random_cell()

    msg.info("the grid cells have been randomized")

# ui_function_arcade ###########################################################

@print_grid_after
def ui_function_arcade(arguments):

    global cell_grid
    global ant_list

    if len(arguments) > 0:
        msg.warning("too many parameters")
        return

    for n1 in range(0, cell_grid_height):
        for n2 in range(0, cell_grid_width):
            if n1 == 0 or n1 == (cell_grid_height - 1) or n2 == 0 or n2 == (cell_grid_width - 1):
                cell_grid[n1][n2].make_obstacle()
            else:
                cell_grid[n1][n2].random_color()

    for ant in ant_list:
        row = ant.get_pos_row()
        column = ant.get_pos_column()

        if row == 0 or row == (cell_grid_height - 1) or column == 0 or column == (cell_grid_width - 1):
            ui_function_escape(list(ant.get_name()))

    msg.info("a random arcade grid has been created")

# ui_function_step #############################################################

def ui_function_step(arguments):

    if len(arguments) > 0:
        msg.warning("too many parameters")
        return

    msg.info("one move has been made")
    ui_function_move(list("1"))

# ui_function_move #############################################################

@print_grid_after
def ui_function_move(arguments):

    global round_count

    if len(arguments) < 1:
        msg.warning("missing parameter")
        return

    if len(arguments) > 1:
        msg.warning("too many parameters")
        return

    # arguments[0] is move count
    parsed = regex.match(arguments[0], REGEX_COUNT)

    if parsed is None:
        msg.warning("invalid argument")
        return

    count = int(parsed["count"])

    if count == 0:
        return # if 0 is given, no moves are made #

    for n in range(1, count + 1):
        round_count += 1

        for current_ant in ant_list:
            current_ant_type = current_ant.get_type()

            if current_ant_type == "standard":
                perform_ant_actions(current_ant)
                continue

            if current_ant_type == "busy":
                for i in range(1, speedup + 1):
                    current_ant = perform_ant_actions(current_ant)
                continue

            if current_ant_type == "lazy":
                if ((round_count - 1) % speedup) == 0:
                    perform_ant_actions(current_ant)
                continue

# ui_function_position #########################################################

@print_result
def ui_function_position(arguments):

    if len(arguments) < 1:
        msg.warning("missing parameter")
        return None

    if len(arguments) > 1:
        msg.warning("too many parameters")
        return None

    ant_name = arguments[0]

    ant = get_ant(antName)

    if ant is None:
        msg.warning("invalid parameter, no ant with the given name")
        return None

    return "The position of ant '" + ant_name + "' is: " + ant.get_position_str()

# ui_function_field ############################################################

@print_result
def ui_function_field(arguments):

    global cell_grid

    if len(arguments) < 1:
        msg.warning("missing parameter")
        return None

    if len(arguments) > 1:
        msg.warning("too many parameters")
        return None

    arg_coordinates = arguments[0]

    parsed = regex.match(arg_coordinates, REGEX_COORDINATES)
    if parsed is None:
        msg.warning("syntax error in the parameter")
        return None

    row = int(parsed["row"])
    column = int(parsed["column"])

    # values < 0 have been eliminated at parsing
    if row > cell_grid_height or column > cell_grid_width:
        msg.warning("no cell exists at the indices given")
        return None

    return "The field in the " + str(row + 1) + ". row and the " + str(column + 1) + ". column has the color: " + cell_grid[row][column].get_representation()

# ui_function_direction ########################################################

@print_result
def ui_function_direction(arguments):

    if len(arguments) < 1:
        msg.warning("missing parameter")
        return None

    if len(arguments) > 1:
        msg.warning("too many parameters")
        return None

    ant_name = arguments[0]

    ant = get_ant(antName)

    if ant is None:
        msg.warning("invalid parameter, no ant with the given name")
        return None

    return ant.get_orientation_str()

# ui_function_create ###########################################################

def ui_function_create(arguments):

    global cell_grid
    global ant_list

    if len(arguments) < 1:
        msg.warning("missing parameter")
        return

    if len(arguments) > 1:
        msg.warning("too many parameters")
        return

    parsed = regex.match(arguments[0], REGEX_ANT_DATA)

    if parsed is not None:
        new_ant_name = parsed["name"]
        new_ant_pos_row = int(parsed["row"])
        new_ant_pos_column = int(parsed["column"])
    else:
        msg.warning("syntax error in the parameter")
        return

    if get_ant(new_ant_name) is not None:
        msg.warning("an ant with this name already exists")
        return

    if new_ant_pos_row > cell_grid_height or new_ant_pos_column > cell_grid_width:
        msg.warning("no cell exists at the indices given")
        return

    if cell_grid[new_ant_pos_row][new_ant_pos_column].get_occupying_ant() is not None:
        msg.warning("the cell at the given indices is already occupied by another ant")
        return

    if cell_grid[new_ant_pos_row][new_ant_pos_column].is_obstacle():
        msg.warning("the cell at the given indices contains an obstacle")
        return

    new_ant = Ant(new_ant_name, new_ant_pos_row, new_ant_pos_column, cell_grid_height, cell_grid_width)
    ant_list.append(new_ant)
    ant_list.sort()
    cell_grid[new_ant_pos_row][new_ant_pos_column].set_occupying_ant(new_ant)

    msg.info("Created a new ant '" + new_ant_name + "' in the " + new_ant_pos_row + ". row and the " + new_ant_pos_column + ". column.")

# ui_function_escape ###########################################################

def ui_function_escape(arguments):

    global cell_grid
    global ant_list

    if len(arguments) < 1:
        msg.warning("missing parameter")
        return

    if len(arguments) > 1:
        msg.warning("too many parameters")
        return

    ant_name = arguments[0]

    parsed = regex.match(ant_name, REGEX_ANT_ANY)

    if parsed is None:
        msg.warning("invalid ant name")
        return

    ant = get_ant(ant_name)

    if ant is None:
        msg.warning("invalid parameter, no ant with the given name")
        return

    cell_grid[ant.get_pos_row()][ant.get_pos_column()].remove_occupying_ant()
    ant_list.remove(ant)

    msg.info("Ant '" + ant_name + "' has been deleted.")

    if len(ant_list) < 1:
        msg.warning("all ants have left the game grid")

# ui_function_help #############################################################

def ui_function_help(arguments):
    global ui_functions_dict
    global ui_command_list

    for command in ui_command_list:
        print(str(command))

# user interface command dictionary ############################################

ui_functions_dict = {
    # UI commands with zero (0) arguments #
        "quit"   : ui_function_quit,
        "exit"   : ui_function_quit,
        "q:"     : ui_function_quit,
        "print"  : ui_function_print,
        "ant"    : ui_function_ant,
        "reset"  : ui_function_reset,
        "step"   : ui_function_step,
        "s:"     : ui_function_step,
        "random" : ui_function_random,
        "arcade" : ui_function_arcade,
        "help"   : ui_function_help,
    # UI commands with one (1) arguments #
        "move"      : ui_function_move,
        "position"  : ui_function_position,
        "pos"       : ui_function_position,
        "field"     : ui_function_field,
        "direction" : ui_function_direction,
        "create"    : ui_function_create,
        "escape"    : ui_function_escape,
        "remove"    : ui_function_escape,
        "delete"    : ui_function_escape,
        "del"       : ui_function_escape
}
ui_command_list = list(ui_functions_dict.keys())

# begin main control flow ######################################################

arg_list = sys.argv
filename = arg_list.pop(0)
arguments = arg_list
argumentcount = len(arguments)

if argumentcount < 1:
    msg.error("missing command line argument")
    sys.exit(1)
### BREAKPOINT #

game_file = open(arguments[0], 'r')
grid_rows = list()
for line in game_file.readlines():
    grid_rows.append(line.splitlines()[0])
game_file.close()

cell_grid_height = len(grid_rows)

if cell_grid_height < 1:
    msg.error("syntax error in the game file")
    sys.exit(1)
### BREAKPOINT #

for n1 in range(0, cell_grid_height):
    cell_grid.append(list())

    if cell_grid_width < 0:
        # the width of the first row is set as a reference value #
        cell_grid_width = len(grid_rows[n1])

    if len(grid_rows[n1]) != cell_grid_width:
        raise ValueError("syntax error in the game file")

    # split the line into 1-character elements #

    line_elements = list()
    for character in grid_rows[n1]:
        line_elements.append(character)

    for n2 in range(0, cell_grid_width):

        parsed = regex.match(line_elements[n2], REGEX_ANT_ANY)

        if parsed is not None:
            cell_grid[n1].append(Cell(0)) # initial color for cell with ant set to 0 (no requirements) #
            new_ant = Ant(parsed["name"], n1, n2, cell_grid_height, cell_grid_width)
            if new_ant in ant_list:
                raise ValueError("semantic error, ant already exists")
            ant_list.append(new_ant)
            ant_list.sort()
            cell_grid[n1][n2].set_occupying_ant(new_ant)
            continue

        parsed = regex.match(line_elements[n2], REGEX_COLOR_ANY)

        if parsed is not None:
            cell_grid[n1].append(Cell(int(parsed["color"])))
            continue

        parsed = regex.match(line_elements[n2], REGEX_OBSTACLE)

        if parsed is not None:
            cell_grid[n1].append(Cell(-1))
            continue

        raise ValueError("syntax error, illegal character in the game file")
        continue

if argumentcount > 1:

    for n in range(1, argumentcount):

        parsed = regex.match(arguments[n], REGEX_RULE_CLA)
        if parsed is not None:
            new_rule = parsed["value"].split("-")
            for i in range(0, len(rule)):
                rule[i] = int(new_rule[i])
            continue

        parsed = regex.match(arguments[n], REGEX_SPEEDUP_CLA)
        if parsed is not None:
            speedup = int(parsed["value"])
            continue

        # else #
        msg.error("invalid command line argument")
        sys.exit(1)
####### BREAKPOINT #

# begin interactive user interface #############################################

while True:
    user_input = input("LangtonAnts $ ")
    input_elements = user_input.split()
    input_element_count = len(input_elements)

    if input_element_count < 1:
        msg.warning("invalid command")
        continue

    ui_command = input_elements.pop(0)
    # input_elements now only contains the parameters

    if ui_command not in ui_command_list:
        msg.warning("invalid command")
        continue

    ui_functions_dict[ui_command](input_elements)
    continue

# end of main control flow #####################################################
