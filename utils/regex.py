# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


""" docstring """

#import re

class Regex():
    """ docstring """

    @staticmethod
    def match(arg_string, arg_compiled_pattern):
        """ docstring """

        return_value = None

        match = arg_compiled_pattern.fullmatch(arg_string)

        if match:
            return_value = match.groupdict()

        return return_value

# END ##########################################################################
