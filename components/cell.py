""" docstring """

import random

from utils.outputmessages import OutputMessages as msg
from utils.asciistyling import AsciiStyle as sty
from utils.asciistyling import AsciiColor as color
from utils.asciistyling import AsciiBackground as bg

# A cell on the game grid #

class Cell():
    """ docstring """

    OBSTACLE_COLOR = -1
    MIN_COLOR_INDEX = 0
    MAX_COLOR_INDEX = 4
    DEFAULT_COLOR = 0

    def __init__(self, arg_type):
        self.color = -1 # default value is obstacle #
        self.occupying_ant = None

        if arg_type >= 0:
            self.set_color(arg_type)

    def has_occupying_ant(self):
        """ docstring """
        # return False if None, True if set
        return bool(self.occupying_ant)

    def get_occupying_ant(self):
        """ docstring """
        return self.occupying_ant

    def set_occupying_ant(self, new_occupying_ant):
        """ docstring """
        self.occupying_ant = new_occupying_ant

    def remove_occupying_ant(self):
        """ docstring """
        self.occupying_ant = None

    def is_obstacle(self):
        """ docstring """
        # return False of True
        return bool(self.color < 0)

    def make_obstacle(self):
        """ docstring """
        self.color = self.OBSTACLE_COLOR

    def get_color(self):
        """ docstring """
        return self.color

    def set_color(self, arg_new_color):
        """ docstring """
        if arg_new_color < self.MIN_COLOR_INDEX or arg_new_color > self.MAX_COLOR_INDEX:
            msg.warning("syntax error, invalid cell color")
            return
        self.color = arg_new_color

    def reset_color(self):
        """ docstring """
        self.color = self.DEFAULT_COLOR

    def random_color(self):
        """ docstring """
        self.color = random.randint(self.MIN_COLOR_INDEX, self.MAX_COLOR_INDEX)

    def random_cell(self):
        """ docstring """
        self.color = random.randint(self.OBSTACLE_COLOR, self.MAX_COLOR_INDEX)

    def recalculate_color(self, arg_algorithm_index=1):
        """ docstring """

        current_color = self.get_color()

        if arg_algorithm_index == 1:
            new_color = (((4 * current_color) + 23) % (self.MAX_COLOR_INDEX + 1))

        self.set_color(new_color)

    def get_representation(self):
        """ docstring """

        if self.get_occupying_ant() is None:
            return_string = str(self.get_color())
        else:
            return_string = color.red(self.get_occupying_ant().get_name())

        return_string = sty.bold(return_string)

        if self.get_color() == 0:
            return_string = bg.white(color.white(return_string))
        elif self.get_color() == 1:
            return_string = bg.yellow(color.yellow(return_string))
        elif self.get_color() == 2:
            return_string = bg.blue(color.blue(return_string))
        elif self.get_color() == 3:
            return_string = bg.green(color.green(return_string))
        elif self.get_color() == 4:
            return_string = bg.cyan(color.cyan(return_string))
        else:
            return_string = sty.framed(bg.black(color.black("*")))

        return return_string

# END ##########################################################################
