# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


""" docstring """

from utils.asciistyling import AsciiStyle as sty
from utils.asciistyling import AsciiColor as color

class OutputMessages():
    """ docstring """

    @staticmethod
    def error_details(error):
        """ docstring """
        print("{0}, {1}".format(sty.bold(color.red("Error")), error.args[0]))

    @staticmethod
    def error(message):
        """ docstring """
        print("{0}, {1}".format(sty.bold(color.red("Error")), message))

    @staticmethod
    def warning(message):
        """ docstring """
        print("{0}, {1}".format(sty.bold(color.yellow("Warning")), message))

    @staticmethod
    def info(message):
        """ docstring """
        print("{0}, {1}".format(sty.bold(color.blue("Info")), message))

# END ##########################################################################
