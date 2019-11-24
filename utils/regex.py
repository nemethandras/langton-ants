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
