
#import re


class Regex():

    @staticmethod
    def match(arg_string, arg_compiled_pattern):

        return_value = None

        match = arg_compiled_pattern.fullmatch(arg_string)

        if match:
            return_value = match.groupdict()

        return return_value

# END ##########################################################################
