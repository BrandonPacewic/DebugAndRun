#! /usr/bin/python3

# Usage dbrun <filename>  
# Can also be used with an input file and an ouput flie
# Ex: dbrun <filename> / <inputfile> / <outputfile>
#
# Both an input file and an output file is not required but an 
# input file is required for an ouput file
#

import sys
import os

from subprocess import Popen, PIPE


class _os():
    class colors:
        OKGREEN = '\033[92m'
        WARNINGRED = '\033[91m'
        WARNINGYELLOW = '\033[93m'
        ENDC = '\033[0m'

    class errors:
        EXPECTEDARGUMENTS = "[EXPECTED ONE ARGUMENTS]"
        INVALIDOPPERATOR = "[INVALID OPPERATOR FOUND]"
        NOFILE = "[EXPECTED FILE FOUND NONE]"
        FILENOTFOUND = "[NO FILE IN DIR NAMED]"

    def checkAssert(CONDITION, EXPECTED, COLOR, ERROR, EXIT):
        try:
            assert(CONDITION == EXPECTED)
        except AssertionError:
            print(f"{COLOR}{ERROR}{_os.colors.ENDC}")
            exit() if EXIT else print(f"{_os.colors.WARNINGYELLOW}[WORKING]{_os.colors.ENDC}") 


def runningMsg(file, inputFile, exitFile):
    print(f"[DEBUG MODE] Compiling {file} with C++17")
    
    if inputFile is not None:
        print(f"[INPUT FILE] Selected Input File is {inputFile}")

    if exitFile is not None:
        print(f"[OUTPUT FILE] Selected Output File is {exitFile}")

    print("--------------------")


def getLines(inputFile):
    try:
        with open(inputFile, 'r') as f:
            lines = f.readlines()

        return lines
    
    except OSError:
        print(f"{_os.colors.WARNINGRED}{_os.errors.FILENOTFOUND} -> {inputFile}{_os.colors.ENDC}")
        exit()

def writeLines(exitFile, newLines):
    try:
        with open(exitFile, 'w') as f:
            f.writelines(newLines)
    
    except OSError:
        print(f"{_os.colors.WARNINGRED}{_os.errors.FILENOTFOUND} -> {exitFile}{_os.colors.ENDC}")
        exit()


def findTargetLine(file, target):
    # No need for try + except because findFileForGpp has already been called
    with open(file, 'r') as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            if line == target:
                return i

    return None

def enterDbgMode(file, targetLine):
    if targetLine is None:
        return

    with open(file, 'r+') as f:
        lines = f.readlines()
        lines[targetLine] = "#define DBG_MODE\n"
        f.truncate(0)
        f.seek(0)
        f.writelines(lines)

def exitDbgMode(file, targetLine):
    if targetLine is None:
        return

    with open(file, 'r+') as f:
        lines = f.readlines()
        lines[targetLine] = "//dbg\n"
        f.truncate(0)
        f.seek(0)
        f.writelines(lines)


def inputLines(programInput):
    p = Popen([os.getcwd() + '/a.out'], stdout=PIPE, stdin=PIPE)

    for line in programInput:
        p.stdin.write(line.encode('utf-8'))

    p.stdin.flush()
    return [line.decode() for line in p.stdout.readlines()]


def findFileForGpp(file):
    try:
        assert(file in os.listdir())
    except AssertionError:
        print(f"g++:{_os.colors.WARNINGRED} error: {_os.colors.ENDC}{file}: No such file found")
        exit()


def wholeInputCheck(inputOperator, inputFile, exitOperator, exitFile):
    if inputOperator is None:
        return

    _os.checkAssert(inputOperator == '/', True, _os.colors.WARNINGRED, _os.errors.INVALIDOPPERATOR, True)
    _os.checkAssert(inputFile is not None, True, _os.colors.WARNINGRED, _os.errors.NOFILE, True)

    if exitOperator is None:
        return

    _os.checkAssert(exitOperator == '/', True, _os.colors.WARNINGRED, _os.errors.INVALIDOPPERATOR, True)
    _os.checkAssert(exitFile is not None, True, _os.colors.WARNINGRED, _os.errors.NOFILE, True)


def main(argv):
    _os.checkAssert(len(argv) in range(1, 6), True, _os.colors.WARNINGRED, _os.errors.EXPECTEDARGUMENTS, True)

    file = argv[0]
    inputOperator = argv[1] if len(argv) > 1 else None
    inputFile = argv[2] if len(argv) > 2 else None
    exitOperator = argv[3] if len(argv) > 3 else None
    exitFile = argv[4] if len(argv) > 4 else None

    # Asserting that whole input is valid
    wholeInputCheck(inputOperator, inputFile, exitOperator, exitFile)

    if file[-3:] != ".cc":  # Adds a suffix if none is provided
        file += ".cc"

    findFileForGpp(file)
    targetLine = findTargetLine(file, target="//dbg\n")
    enterDbgMode(file, targetLine)
    os.system(f"g++ {file}")
    exitDbgMode(file, targetLine)

    runningMsg(file, inputFile, exitFile)

    if inputOperator is None:
        os.system("./a.out")
        exit()

    programOutput = inputLines(getLines(inputFile))

    if exitOperator is None:
        for line in programOutput:
            print(line)

        exit()

    writeLines(exitFile, programOutput)
    print(f"{_os.colors.OKGREEN}[SUCCESS]{_os.colors.ENDC} Write lines to file {exitFile} successful")


if __name__ == "__main__":
    main(sys.argv[1:])
