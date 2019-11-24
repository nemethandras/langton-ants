#!/usr/bin/env python3

import hashlib
import re

# helper utilities #

def RegExMatch(argString, argCompiledPattern):
    match = argCompiledPattern.fullmatch(argString)
    if match:
        return match.groupdict()
    else:
        return None

def strBold(argPrintable):
    return "\x1b[1m" + str(argPrintable) + "\x1b[0m"

def strFaint(argPrintable):
    return "\x1b[2m" + str(argPrintable) + "\x1b[0m"

def strItalic(argPrintable):
    return "\x1b[3m" + str(argPrintable) + "\x1b[0m"

def strUnderlined(argPrintable):
    return "\x1b[4m" + str(argPrintable) + "\x1b[0m"

def strBlink(argPrintable):
    return "\x1b[5m" + str(argPrintable) + "\x1b[0m"

def strImageNegative(argPrintable):
    return "\x1b[7m" + str(argPrintable) + "\x1b[0m"

def strPrimaryFont(argPrintable):
    return "\x1b[10m" + str(argPrintable) + "\x1b[0m"

def strAlternateFont(argPrintable, argAlternateFontNo):
    if int(argAlternateFontNo) > 0 and int(argAlternateFontNo) < 10:
        insertedNo = str(argAlternateFontNo)
    else:
        insertedNo = "1"
    return "\x1b[1" + insertedNo + "m" + str(argPrintable) + "\x1b[0m"

def strBlack(argPrintable):
    return "\x1b[30m" + str(argPrintable) + "\x1b[0m"

def strRed(argPrintable):
    return "\x1b[31m" + str(argPrintable) + "\x1b[0m"

def strGreen(argPrintable):
    return "\x1b[32m" + str(argPrintable) + "\x1b[0m"

def strYellow(argPrintable):
    return "\x1b[33m" + str(argPrintable) + "\x1b[0m"

def strBlue(argPrintable):
    return "\x1b[34m" + str(argPrintable) + "\x1b[0m"

def strMagenta(argPrintable):
    return "\x1b[35m" + str(argPrintable) + "\x1b[0m"

def strCyan(argPrintable):
    return "\x1b[36m" + str(argPrintable) + "\x1b[0m"

def strWhite(argPrintable):
    return "\x1b[37m" + str(argPrintable) + "\x1b[0m"

def strBgBlack(argPrintable):
    return "\x1b[40m" + str(argPrintable) + "\x1b[0m"

def strBgRed(argPrintable):
    return "\x1b[41m" + str(argPrintable) + "\x1b[0m"

def strBgGreen(argPrintable):
    return "\x1b[42m" + str(argPrintable) + "\x1b[0m"

def strBgYellow(argPrintable):
    return "\x1b[43m" + str(argPrintable) + "\x1b[0m"

def strBgBlue(argPrintable):
    return "\x1b[44m" + str(argPrintable) + "\x1b[0m"

def strBgMagenta(argPrintable):
    return "\x1b[45m" + str(argPrintable) + "\x1b[0m"

def strBgCyan(argPrintable):
    return "\x1b[46m" + str(argPrintable) + "\x1b[0m"

def strBgWhite(argPrintable):
    return "\x1b[47m" + str(argPrintable) + "\x1b[0m"

def strFramed(argPrintable):
    return "\x1b[51m" + str(argPrintable) + "\x1b[0m"

def strEncircled(argPrintable):
    return "\x1b[52m" + str(argPrintable) + "\x1b[0m"

def strOverlined(argPrintable):
    return "\x1b[53m" + str(argPrintable) + "\x1b[0m"

def displayErrorMessage(error):
    print(strBold(strRed("Error")) + ", " + error.args[0])

def errorMessage(message):
    print( strBold(strRed("Error")) + ", " + message )

def warningMessage(message):
    print( strBold(strYellow("Warning")) + ", " + message )

def infoMessage(message):
    print( strBold(strBlue("Info")) + ", " + message )

def encode(argObject):
    return argObject.encode('utf-8')

def decode(argObject):
    return argObject.decode('utf-8')

def hashSHA1(argObject):
    return hashlib.sha1(argObject).hexdigest()

def integerHash(argHexDigest):
    return int(argHexDigest[:8], 16) # 8 hex digits of precision
