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
cellGrid = list()
cellGridHeight = -1 # invalid initial value for checking #
cellGridWidth = -1 # invalid initial value for checking #
antList = list()
roundCount = 0

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

# getAnt #######################################################################

def getAnt(argAntName):
    antName = argAntName.lower()

    for currentAnt in antList:
        if currentAnt.getName() == antName:
            return currentAnt

    # if an ant was not found, None is returned #
    return None

# performAntActions ############################################################

def performAntActions(argAnt):
    global cellGrid

    if argAnt is None:
        return None

    antOriginPosRow = argAnt.getPosRow()
    antOriginPosColumn = argAnt.getPosColumn()
    antOriginCell = cellGrid[antOriginPosRow][antOriginPosColumn]

    antTargetPosRow = antOriginPosRow + argAnt.getTargetPosRowRelation()
    antTargetPosColumn = antOriginPosColumn + argAnt.getTargetPosColumnRelation()

    try:
        antTargetCell = cellGrid[antTargetPosRow][antTargetPosColumn]
    except IndexError as e:
        uiFunction_escape(list(argAnt.getName()))
        return None

    # move if possible #
    if antTargetCell.hasOccupyingAnt() or antTargetCell.isObstacle():
        antTargetCell = antOriginCell
        antTargetPosRow = antOriginPosRow
        antTargetPosColumn = antOriginPosColumn
    else:
        argAnt.setPosition(antTargetPosRow, antTargetPosColumn)

        antOriginCell.removeOccupyingAnt()
        antTargetCell.setOccupyingAnt(argAnt)

    # turn
    antTargetCellOriginalColor = antTargetCell.getColor()
    argAnt.changeOrientation(rule[antTargetCellOriginalColor], cellGridHeight, cellGridWidth)

    # change cell color based on formula #
    antTargetCell.recalculateColor()

    # if everything went in order, return ant for a possible new iteration #
    return argAnt

# decorator: printGridAfter ####################################################

def printGridAfter(argFunction):
    def newFunction(arguments):
        argFunction(arguments)
        uiFunction_print(list())
    return newFunction

# decorator: printResult #######################################################

def printResult(argFunction):
    def newFunction(arguments):
        result = argFunction(arguments)
        if result is not None:
            print(str(result))
    return newFunction

# user interface definitions ###################################################

# uiFunction_quit ##############################################################

def uiFunction_quit(arguments):
    if len(arguments) > 0:
        msg.warning("too many parameters")
        return

    sys.exit(0)
### BREAKPOINT #

# uiFunction_print #############################################################

# reference function for @printGridAfter
def uiFunction_print(arguments):
    global cellGrid

    if len(arguments) > 0:
        msg.warning("too many parameters")
        return

    for n1 in range(0, cellGridHeight):
        rowString = ""

        for n2 in range(0, cellGridWidth):
            cell = cellGrid[n1][n2].getRepresentation()

            rowString += cell

        print(rowString)

# uiFunction_ant ###############################################################

@printResult
def uiFunction_ant(arguments):
    global antList

    if len(arguments) > 0:
        msg.warning("too many parameters")
        return None

    resultString = ""

    for i in range(0, len(antList)):
        currentAnt = antList[i]
        resultString += currentAnt.getName();

        if i < len(antList) - 1:
            resultString += ", "

    return "The following ants are on the grid: " + resultString

# uiFunction_reset #############################################################

@printGridAfter
def uiFunction_reset(arguments):
    global cellGrid

    if len(arguments) > 0:
        msg.warning("too many parameters")
        return

    for n1 in range(0, cellGridHeight):
        for n2 in range(0, cellGridWidth):
            cellGrid[n1][n2].resetColor()

    msg.info("the grid cells have been reset")

# uiFunction_random ############################################################

@printGridAfter
def uiFunction_random(arguments):
    global cellGrid

    if len(arguments) > 0:
        msg.warning("too many parameters")
        return

    for n1 in range(0, cellGridHeight):
        for n2 in range(0, cellGridWidth):
            cellGrid[n1][n2].randomCell()

    msg.info("the grid cells have been randomized")

# uiFunction_arcade ############################################################

@printGridAfter
def uiFunction_arcade(arguments):
    global cellGrid
    global antList

    if len(arguments) > 0:
        msg.warning("too many parameters")
        return

    for n1 in range(0, cellGridHeight):
        for n2 in range(0, cellGridWidth):
            if n1 == 0 or n1 == (cellGridHeight - 1) or n2 == 0 or n2 == (cellGridWidth - 1):
                cellGrid[n1][n2].makeObstacle()
            else:
                cellGrid[n1][n2].randomColor()

    for ant in antList:
        row = ant.getPosRow()
        column = ant.getPosColumn()

        if row == 0 or row == (cellGridHeight - 1) or column == 0 or column == (cellGridWidth - 1):
            uiFunction_escape(list(ant.getName()))

    msg.info("a random arcade grid has been created")

# uiFunction_step ##############################################################

def uiFunction_step(arguments):
    if len(arguments) > 0:
        msg.warning("too many parameters")
        return

    msg.info("one move has been made")
    uiFunction_move(list("1"))

# uiFunction_move ##############################################################

@printGridAfter
def uiFunction_move(arguments):
    global roundCount

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
        roundCount += 1

        for currentAnt in antList:
            currentAntType = currentAnt.getType()

            if currentAntType == "standard":
                performAntActions(currentAnt)
                continue

            if currentAntType == "busy":
                for i in range(1, speedup + 1):
                    currentAnt = performAntActions(currentAnt)
                continue

            if currentAntType == "lazy":
                if ((roundCount - 1) % speedup) == 0:
                    performAntActions(currentAnt)
                continue

# uiFunction_position ##########################################################

@printResult
def uiFunction_position(arguments):
    if len(arguments) < 1:
        msg.warning("missing parameter")
        return None

    if len(arguments) > 1:
        msg.warning("too many parameters")
        return None

    antName = arguments[0]

    ant = getAnt(antName)

    if ant is None:
        msg.warning("invalid parameter, no ant with the given name")
        return None

    return "The position of ant '" + antName + "' is: " + ant.getPositionStr()

# uiFunction_field #############################################################

@printResult
def uiFunction_field(arguments):
    global cellGrid

    if len(arguments) < 1:
        msg.warning("missing parameter")
        return None

    if len(arguments) > 1:
        msg.warning("too many parameters")
        return None

    argCoordinates = arguments[0]

    parsed = regex.match(argCoordinates, REGEX_COORDINATES)
    if parsed is None:
        msg.warning("syntax error in the parameter")
        return None

    row = int(parsed["row"])
    column = int(parsed["column"])

    # values < 0 have been eliminated at parsing
    if row > cellGridHeight or column > cellGridWidth:
        msg.warning("no cell exists at the indices given")
        return None

    return "The field in the " + str(row + 1) + ". row and the " + str(column + 1) + ". column has the color: " + cellGrid[row][column].getRepresentation()

# uiFunction_direction #########################################################

@printResult
def uiFunction_direction(arguments):
    if len(arguments) < 1:
        msg.warning("missing parameter")
        return None

    if len(arguments) > 1:
        msg.warning("too many parameters")
        return None

    antName = arguments[0]

    ant = getAnt(antName)

    if ant is None:
        msg.warning("invalid parameter, no ant with the given name")
        return None

    return ant.getOrientationStr()

# uiFunction_create ############################################################

def uiFunction_create(arguments):
    global cellGrid
    global antList

    if len(arguments) < 1:
        msg.warning("missing parameter")
        return

    if len(arguments) > 1:
        msg.warning("too many parameters")
        return

    parsed = regex.match(arguments[0], REGEX_ANT_DATA)

    if parsed is not None:
        newAntName = parsed["name"]
        newAntPosRow = int(parsed["row"])
        newAntPosColumn = int(parsed["column"])
    else:
        msg.warning("syntax error in the parameter")
        return

    if getAnt(newAntName) is not None:
        msg.warningMessage("an ant with this name already exists")
        return

    if newAntPosRow > cellGridHeight or newAntPosColumn > cellGridWidth:
        msg.warning("no cell exists at the indices given")
        return

    if cellGrid[newAntPosRow][newAntPosColumn].getOccupyingAnt() is not None:
        msg.warning("the cell at the given indices is already occupied by another ant")
        return

    if cellGrid[newAntPosRow][newAntPosColumn].isObstacle():
        msg.warning("the cell at the given indices contains an obstacle")
        return

    newAnt = Ant(newAntName, newAntPosRow, newAntPosColumn, cellGridHeight, cellGridWidth)
    antList.append(newAnt)
    antList.sort()
    cellGrid[newAntPosRow][newAntPosColumn].setOccupyingAnt(newAnt)

    msg.info("Created a new ant '" + newAntName + "' in the " + newAntPosRow + ". row and the " + newAntPosColumn + ". column.")

# uiFunction_escape ############################################################

def uiFunction_escape(arguments):
    global cellGrid
    global antList

    if len(arguments) < 1:
        msg.warning("missing parameter")
        return

    if len(arguments) > 1:
        msg.warning("too many parameters")
        return

    antName = arguments[0]

    parsed = regex.match(antName, REGEX_ANT_ANY)
    if parsed is None:
        msg.warning("invalid ant name")
        return

    ant = getAnt(antName)

    if ant is None:
        msg.warning("invalid parameter, no ant with the given name")
        return

    cellGrid[ant.getPosRow()][ant.getPosColumn()].removeOccupyingAnt()
    antList.remove(ant)

    msg.info("Ant '" + antName + "' has been deleted.")

    if (len(antList) < 1):
        msg.warning("all ants have left the game grid")

# uiFunction_help ##############################################################

def uiFunction_help(arguments):
    global uiFunctionsDict
    global uiCommandList

    for command in uiCommandList:
        print(str(command))

# user interface command dictionary ############################################

uiFunctionsDict = {
    # UI commands with zero (0) arguments #
        "quit"   : uiFunction_quit,
        "exit"   : uiFunction_quit,
        "q:"     : uiFunction_quit,
        "print"  : uiFunction_print,
        "ant"    : uiFunction_ant,
        "reset"  : uiFunction_reset,
        "step"   : uiFunction_step,
        "s:"     : uiFunction_step,
        "random" : uiFunction_random,
        "arcade" : uiFunction_arcade,
        "help" : uiFunction_help,
    # UI commands with one (1) arguments #
        "move"      : uiFunction_move,
        "position"  : uiFunction_position,
        "pos"       : uiFunction_position,
        "field"     : uiFunction_field,
        "direction" : uiFunction_direction,
        "create"    : uiFunction_create,
        "escape"    : uiFunction_escape,
        "remove"    : uiFunction_escape,
        "delete"    : uiFunction_escape,
        "del"    : uiFunction_escape
}
uiCommandList = list(uiFunctionsDict.keys())

# begin main control flow ######################################################

argList = sys.argv
filename = argList.pop(0)
arguments = argList
argumentcount = len(arguments)

if argumentcount < 1:
    msg.error("missing command line argument")
    sys.exit(1)
### BREAKPOINT #

gameFile = open(arguments[0], 'r')
gridRows = list()
for line in gameFile.readlines():
    gridRows.append(line.splitlines()[0])
gameFile.close()

cellGridHeight = len(gridRows)

if cellGridHeight < 1:
    msg.error("syntax error in the game file")
    sys.exit(1)
### BREAKPOINT #

for n1 in range(0, cellGridHeight):
    cellGrid.append(list())

    if cellGridWidth < 0:
        # the width of the first row is set as a reference value #
        cellGridWidth = len(gridRows[n1])

    if len(gridRows[n1]) != cellGridWidth:
        raise ValueError("syntax error in the game file")

    # split the line into 1-character elements #

    lineElements = list()
    for character in gridRows[n1]:
        lineElements.append(character)

    for n2 in range(0, cellGridWidth):

        parsed = regex.match(lineElements[n2], REGEX_ANT_ANY)

        if parsed is not None:
            cellGrid[n1].append( Cell(0) ) # initial color for cell with ant set to 0 (no requirements) #
            newAnt = Ant(parsed["name"], n1, n2, cellGridHeight, cellGridWidth)
            if newAnt in antList:
                raise ValueError("semantic error, ant already exists")
            antList.append(newAnt)
            antList.sort()
            cellGrid[n1][n2].setOccupyingAnt(newAnt)
            continue

        parsed = regex.match(lineElements[n2], REGEX_COLOR_ANY)

        if parsed is not None:
            cellGrid[n1].append( Cell(int(parsed["color"])) )
            continue

        parsed = regex.match(lineElements[n2], REGEX_OBSTACLE)

        if parsed is not None:
            cellGrid[n1].append( Cell(-1) )
            continue

        raise ValueError("syntax error, illegal character in the game file")
        continue

if argumentcount > 1:

    for n in range(1, argumentcount):

        parsed = regex.match(arguments[n], REGEX_RULE_CLA)
        if parsed is not None:
            newRule = parsed["value"].split("-")
            for i in range(0, len(rule)):
                rule[i] = int(newRule[i])
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
    userInput = input("LangtonAnts $ ")
    inputElements = userInput.split()
    inputElementCount = len(inputElements)

    if inputElementCount < 1:
        msg.warning("invalid command")
        continue

    uiCommand = inputElements.pop(0)
    # inputElements now only contains the parameters

    if uiCommand not in uiCommandList:
        msg.warning("invalid command")
        continue

    uiFunctionsDict[uiCommand](inputElements)
    continue

# end of main control flow #####################################################

