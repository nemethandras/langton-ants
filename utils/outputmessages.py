
from utils.asciistyling import AsciiStyle as sty
from utils.asciistyling import AsciiColor as color

class OutputMessages():

    @staticmethod
    def error_details(error):
        print("{0}, {1}".format(sty.bold(color.red("Error")), error.args[0]))

    @staticmethod
    def error(message):
        print("{0}, {1}".format(sty.bold(color.red("Error")), message))

    @staticmethod
    def warning(message):
        print("{0}, {1}".format(sty.bold(color.yellow("Warning")), message))

    @staticmethod
    def info(message):
        print("{0}, {1}".format(sty.bold(color.blue("Info")), message))

# END ##########################################################################
