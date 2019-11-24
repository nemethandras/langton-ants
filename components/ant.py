
import re

from utils.regex import Regex as regex
from utils.codec import ObjectCodec as codec
from utils.codec import Hashing as hashing

# An ant #

class Ant(object):

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

    def __init__(self, argAntName, argPosRow, argPosColumn, cellGridHeight, cellGridWidth):

        self.name = None
        self.orientation = None

        parsed = regex.match(argAntName, self.REGEX_ANT_DIRECTION)

        if parsed is not None:
            if parsed["North"] is not None:
                self.name = parsed["North"].lower()
                self.orientation = 0
            elif parsed["South"] is not None:
                self.name = parsed["South"].lower()
                self.orientation = 180

        self.hash = hashing.integer_hash(hashing.hash_sha1(codec.encode(self.getName())))
        self.antType = None  # "standard" ant, "busy" ant, "lazy" ant #

        parsed = regex.match(self.getName(), self.REGEX_ANT_TYPE)

        if parsed is not None:
            if parsed["standard"] is not None:
                self.antType = "standard"
            elif parsed["busy"] is not None:
                self.antType = "busy"
            elif parsed["lazy"] is not None:
                self.antType = "lazy"

        self.posRow = -1
        self.posColumn = -1
        self.setPosition(argPosRow, argPosColumn)

        self.targetPosRowRelation = 0
        self.targetPosColumnRelation = 0
        self.__determineTargetPosRelations(cellGridHeight, cellGridWidth)


    def __lt__(self, other):
        return self.getName() < other.getName()

    def __le__(self, other):
        return self.getName() <= other.getName()

    def __eq__(self, other):
        return self.getName() == other.getName()

    def __ne__(self, other):
        return self.getName() != other.getName()

    def __gt__(self, other):
        return self.getName() > other.getName()

    def __ge__(self, other):
        return self.getName() >= other.getName()

    def __hash__(self):
        return self.getHash()

    def getName(self):
        return self.name

    def getHash(self):
        return self.hash

    def getOrientationStr(self):
        return self.ORIENTATION_TO_STR_DICT[self.orientation]

    def changeOrientation(self, argAngle, cellGridHeight, cellGridWidth):
        self.orientation = (self.orientation + argAngle) % 360
        self.__determineTargetPosRelations(cellGridHeight, cellGridWidth)

    def getTargetPosRowRelation(self):
        return self.targetPosRowRelation

    def getTargetPosColumnRelation(self):
        return self.targetPosColumnRelation

    def setTargatPosRelation(self, argTargetPosRowRelation, argTargetPosColumnRelation):
        self.targetPosRowRelation = argTargetPosRowRelation
        self.targetPosColumnRelation = argTargetPosColumnRelation

    def getType(self):
        return self.antType

    def getPositionStr(self):
        return str(self.posRow) + "," + str(self.posColumn)

    def getPosRow(self):
        return self.posRow

    def getPosColumn(self):
        return self.posColumn

    def setPosition(self, argPosRow, argPosColumn):
        self.posRow = argPosRow
        self.posColumn = argPosColumn

    def __determineTargetPosRelations(self, cellGridHeight, cellGridWidth):
        orientationStr = self.getOrientationStr()

        if orientationStr == self.ORIENTATION_NORTH:
            if self.getPosRow() > 0:
                self.setTargatPosRelation(self.ONENORTH, self.INPLACE)
        elif orientationStr == self.ORIENTATION_NORTHEAST:
            if self.getPosRow() > 0 and self.getPosColumn() < cellGridWidth - 1:
                self.setTargatPosRelation(self.ONENORTH, self.ONEEAST)
        elif orientationStr == self.ORIENTATION_EAST:
            if self.getPosColumn() < cellGridWidth - 1:
                self.setTargatPosRelation(self.INPLACE, self.ONEEAST)
        elif orientationStr == self.ORIENTATION_SOUTHEAST:
            if self.getPosRow() < cellGridHeight - 1 and self.getPosColumn() < cellGridWidth - 1:
                self.setTargatPosRelation(self.ONESOUTH, self.ONEEAST)
        elif orientationStr == self.ORIENTATION_SOUTH:
            if self.getPosRow() < cellGridHeight - 1:
                self.setTargatPosRelation(self.ONESOUTH, self.INPLACE)
        elif orientationStr == self.ORIENTATION_SOUTHWEST:
            if self.getPosRow() < cellGridHeight - 1 and self.getPosColumn() > 0:
                self.setTargatPosRelation(self.ONESOUTH, self.ONEWEST)
        elif orientationStr == self.ORIENTATION_WEST:
            if self.getPosColumn() > 0:
                self.setTargatPosRelation(self.INPLACE, self.ONEWEST)
        elif orientationStr == self.ORIENTATION_NORTHWEST:
            if self.posRow > 0 and self.getPosColumn() > 0:
                self.setTargatPosRelation(self.ONENORTH, self.ONEWEST)


