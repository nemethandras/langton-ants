#!/usr/bin/env python3

import random

from antclass import Ant
from utils import *

# A cell on the game grid #

class Cell(object):

    OBSTACLE_COLOR = -1
    MIN_COLOR_INDEX = 0
    MAX_COLOR_INDEX = 4
    DEFAULT_COLOR = 0

    def __init__(self, argType):
        self.color = -1 # default value is obstacle #
        self.occupyingAnt = None
        
        if argType >= 0:
            self.setColor(argType)
    
    def hasOccupyingAnt(self):
        if self.occupyingAnt is not None:
            return True
        else:
            return False
    
    def getOccupyingAnt(self):
        return self.occupyingAnt
    
    def setOccupyingAnt(self, newOccupyingAnt):
        self.occupyingAnt = newOccupyingAnt

    def removeOccupyingAnt(self):
        self.occupyingAnt = None

    def isObstacle(self):
        if self.color < 0:
            return True
        else:
            return False
    
    def makeObstacle(self):
        self.color = self.OBSTACLE_COLOR
    
    def getColor(self):
        return self.color

    def setColor(self, argNewColor):
        if argNewColor < self.MIN_COLOR_INDEX or argNewColor > self.MAX_COLOR_INDEX:
            warningMessage("syntax error, invalid cell color")
            return
        self.color = argNewColor
    
    def resetColor(self):
        self.color = self.DEFAULT_COLOR
    
    def randomColor(self):
        self.color = random.randint(self.MIN_COLOR_INDEX, self.MAX_COLOR_INDEX)
        
    def randomCell(self):
        self.color = random.randint(self.OBSTACLE_COLOR, self.MAX_COLOR_INDEX)
    
    def recalculateColor(self, argAlgorithmIndex=1):
        currentColor = self.getColor()
        
        if argAlgorithmIndex == 1:
            newColor = (((4 * currentColor) + 23) % (self.MAX_COLOR_INDEX + 1))
        
        self.setColor(newColor)

    def getRepresentation(self):
    
        if self.getOccupyingAnt() is None:
            returnString = str(self.getColor())
        else:
            returnString = strRed(self.getOccupyingAnt().getName())
       
        returnString = strBold(returnString)
        
        if (self.getColor() == 0):
            returnString = strBgWhite(strWhite(returnString))
        elif (self.getColor() == 1):
            returnString = strBgYellow(strYellow(returnString))
        elif (self.getColor() == 2):
            returnString = strBgBlue(strBlue(returnString))
        elif (self.getColor() == 3):
            returnString = strBgGreen(strGreen(returnString))
        elif (self.getColor() == 4):
            returnString = strBgCyan(strCyan(returnString))
        else:
            returnString = strFramed(strBgBlack(strBlack("*")))
        
        return returnString

