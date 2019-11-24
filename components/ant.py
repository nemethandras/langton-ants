
import re

from utils.regex import Regex as regex
from utils.codec import ObjectCodec as codec
from utils.codec import Hashing as hashing

# An ant #

class Ant():

    # Orientations #
    ORIENTATION_NORTH = "N"
    ORIENTATION_NORTHEAST = "NE"
    ORIENTATION_EAST = "E"
    ORIENTATION_SOUTHEAST = "SE"
    ORIENTATION_SOUTH = "S"
    ORIENTATION_SOUTHWEST = "SW"
    ORIENTATION_WEST = "W"
    ORIENTATION_NORTHWEST = "NW"

    ORIENTATION_TO_STR_DICT = {
        0:   ORIENTATION_NORTH,
        45:  ORIENTATION_NORTHEAST,
        90:  ORIENTATION_EAST,
        135: ORIENTATION_SOUTHEAST,
        180: ORIENTATION_SOUTH,
        225: ORIENTATION_SOUTHWEST,
        270: ORIENTATION_WEST,
        315: ORIENTATION_NORTHWEST
    }

    # RegEx matchers #
    REGEX_ANT_DIRECTION = re.compile("((?P<North>[A-Z])|(?P<South>[a-z]))")
    REGEX_ANT_TYPE = re.compile("((?P<standard>[a-h])|(?P<busy>[i-q])|(?P<lazy>[r-z]))")

    # ant directional target meta values #
    ONENORTH = -1
    ONEWEST = -1
    INPLACE = 0
    ONESOUTH = 1
    ONEEAST = 1

    def __init__(self, arg_ant_name, arg_pos_row, arg_pos_column, cell_grid_height, cell_grid_width):

        self.name = None
        self.orientation = None

        parsed = regex.match(arg_ant_name, self.REGEX_ANT_DIRECTION)

        if parsed is not None:
            if parsed["North"] is not None:
                self.name = parsed["North"].lower()
                self.orientation = 0
            elif parsed["South"] is not None:
                self.name = parsed["South"].lower()
                self.orientation = 180

        self.hash = hashing.integer_hash(hashing.hash_sha1(codec.encode(self.get_name())))
        self.ant_type = None  # "standard" ant, "busy" ant, "lazy" ant #

        parsed = regex.match(self.get_name(), self.REGEX_ANT_TYPE)

        if parsed is not None:
            if parsed["standard"] is not None:
                self.ant_type = "standard"
            elif parsed["busy"] is not None:
                self.ant_type = "busy"
            elif parsed["lazy"] is not None:
                self.ant_type = "lazy"

        self.pos_row = -1
        self.pos_column = -1
        self.set_position(arg_pos_row, arg_pos_column)

        self.target_pos_row_relation = 0
        self.target_pos_column_relation = 0
        self.__determine_target_pos_relations(cell_grid_height, cell_grid_width)


    def __lt__(self, other):
        return self.get_name() < other.get_name()

    def __le__(self, other):
        return self.get_name() <= other.get_name()

    def __eq__(self, other):
        return self.get_name() == other.get_name()

    def __ne__(self, other):
        return self.get_name() != other.get_name()

    def __gt__(self, other):
        return self.get_name() > other.get_name()

    def __ge__(self, other):
        return self.get_name() >= other.get_name()

    def __hash__(self):
        return self.get_hash()

    def get_name(self):
        return self.name

    def get_hash(self):
        return self.hash

    def get_orientation_str(self):
        return self.ORIENTATION_TO_STR_DICT[self.orientation]

    def change_orientation(self, arg_angle, cell_grid_height, cell_grid_width):
        self.orientation = (self.orientation + arg_angle) % 360
        self.__determine_target_pos_relations(cell_grid_height, cell_grid_width)

    def get_target_pos_row_relation(self):
        return self.target_pos_row_relation

    def get_target_pos_column_relation(self):
        return self.target_pos_column_relation

    def set_targat_pos_relation(self, arg_target_pos_row_relation, arg_target_pos_column_relation):
        self.target_pos_row_relation = arg_target_pos_row_relation
        self.target_pos_column_relation = arg_target_pos_column_relation

    def get_type(self):
        return self.ant_type

    def get_position_str(self):
        return str(self.pos_row) + "," + str(self.pos_column)

    def get_pos_row(self):
        return self.pos_row

    def get_pos_column(self):
        return self.pos_column

    def set_position(self, arg_pos_row, arg_pos_column):
        self.pos_row = arg_pos_row
        self.pos_column = arg_pos_column

    def __determine_target_pos_relations(self, cell_grid_height, cell_grid_width):
        orientation_str = self.get_orientation_str()

        if orientation_str == self.ORIENTATION_NORTH:
            if self.get_pos_row() > 0:
                self.set_targat_pos_relation(self.ONENORTH, self.INPLACE)
        elif orientation_str == self.ORIENTATION_NORTHEAST:
            if self.get_pos_row() > 0 and self.get_pos_column() < cell_grid_width - 1:
                self.set_targat_pos_relation(self.ONENORTH, self.ONEEAST)
        elif orientation_str == self.ORIENTATION_EAST:
            if self.get_pos_column() < cell_grid_width - 1:
                self.set_targat_pos_relation(self.INPLACE, self.ONEEAST)
        elif orientation_str == self.ORIENTATION_SOUTHEAST:
            if self.get_pos_row() < cell_grid_height - 1 and self.get_pos_column() < cell_grid_width - 1:
                self.set_targat_pos_relation(self.ONESOUTH, self.ONEEAST)
        elif orientation_str == self.ORIENTATION_SOUTH:
            if self.get_pos_row() < cell_grid_height - 1:
                self.set_targat_pos_relation(self.ONESOUTH, self.INPLACE)
        elif orientation_str == self.ORIENTATION_SOUTHWEST:
            if self.get_pos_row() < cell_grid_height - 1 and self.get_pos_column() > 0:
                self.set_targat_pos_relation(self.ONESOUTH, self.ONEWEST)
        elif orientation_str == self.ORIENTATION_WEST:
            if self.get_pos_column() > 0:
                self.set_targat_pos_relation(self.INPLACE, self.ONEWEST)
        elif orientation_str == self.ORIENTATION_NORTHWEST:
            if self.pos_row > 0 and self.get_pos_column() > 0:
                self.set_targat_pos_relation(self.ONENORTH, self.ONEWEST)

# END ##########################################################################
