
import re


class Regex():

    @staticmethod
    def match(arg_string, arg_compiled_pattern):
        match = arg_compiled_pattern.fullmatch(arg_string)
        if match:
            return match.groupdict()
        else:
            return None

# END ##########################################################################
