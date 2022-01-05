#! /usr/bin/python3

# Usage dbrun <filename>  
# Can also be used with an input file and an ouput flie
# Ex: dbrun <filename> / <inputfile> / <outputfile>
#
# Both an input file and an output file is not required but an 
# input file is required for an ouput file
#

from typing import List, Optional
from subprocess import Popen, PIPE
import sys
import os
import logging


class colors:
    OKGREEN = '\033[92m'
    WARNINGRED = '\033[91m'
    WARNINGYELLOW = '\033[93m'
    ENDC = '\033[0m'


class errors:
    EXPECTED_ARGUMENTS = "[EXPECTED ONE ARGUMENTS]"
    INVALID_OPPERATOR = "[INVALID OPPERATOR FOUND]"
    NO_FILE = "[EXPECTED FILE FOUND NONE]"
    LEN_MISSMATCH = "[LINE LENGTH MISSMATCH]"
    NO_TARGET_LINE = f"[COULD NOT FIND TARGET LINE]{colors.ENDC} -> None"

    @staticmethod
    def file_not_found(*args) -> exit:
        for arg in args:
            logging.error(f"{colors.WARNINGRED}[FILE NOT FOUND]{colors.ENDC} NO FILE IN DIR NAMED -> {arg}")
        exit()

    @staticmethod
    def gpp_file_not_found(file: str) -> exit:
        logging.error(f"g++:{colors.WARNINGRED} error: {colors.ENDC}{file}: No such file found")
        exit()


def check_condition(
    condition: bool = False, 
    expect: bool = True, 
    color: str = colors.WARNINGRED, 
    msg: str = None, 
    leave: bool = True,
) -> Optional[exit]:
    """Template for basic console logging"""
    try:
        assert(condition is expect)
    except AssertionError:
        logging.error(f"{color}{msg}{colors.ENDC}")
        exit() if leave else print(f"{colors.WARNINGYELLOW}[WORKING]{colors.ENDC}")


def running_msg(file: str, inputFile: str = None, exitFile: str = None) -> None:
    print(f"[DEBUG MODE] Compiling {file} with C++17")
    if inputFile is not None:
        print(f"[INPUT FILE] Selected Input File is {inputFile}")

    if exitFile is not None:
        print(f"[OUTPUT FILE] Selected Output File is {exitFile}")

    print("--------------------")


def get_file_lines(fname: str) -> List[str]:
    try:
        with open(fname, 'r') as file:
            return file.readlines()
    except OSError:
        errors.file_not_found(fname)


def write_file_lines(fname: str, lines: List[str]) -> None:
    try:
        with open(fname, 'w') as file:
            file.writelines(lines)
    except OSError:
        errors.file_not_found(fname)


def locate_target_line(fname: str, target: str) -> int:
    try:
        with open(fname, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line == target: 
                    return i
    except OSError:
        errors.file_not_found(fname)
    return None


def replace_line(fname: str, targetLine: int, replacementLine: str) -> None:
    if targetLine is None:
        check_condition(color=colors.WARNINGYELLOW, msg=errors.NO_TARGET_LINE, leave=False)
        return

    def _clear_file() -> None:
        file.truncate(0)
        file.seek(0)

    try:
        with open(fname, 'r+') as file:
            lines = file.readlines()
            lines[targetLine] = replacementLine
            _clear_file()
            file.writelines(lines)
    except OSError:
        errors.file_not_found(fname)


def gpp_assert_file_in_dir(fname: str) -> None:
    try:
        assert(fname in os.listdir())
    except AssertionError:
        errors.gpp_file_not_found(fname)


def cpp_program_interact(lines: List[str]) -> List[str]:
    p = Popen([f"{os.getcwd()}/a.out"], stdout=PIPE, stdin=PIPE)
    for line in lines:
        p.stdin.write(line.encode('utf-8'))
    p.stdin.flush()
    return [line.decode() for line in p.stdout.readlines()]


def whole_input_check(
    file: str,
    inputOperator: str, 
    inputFile: str, 
    exitOperator: str, 
    exitFile: str
) -> Optional[exit]:
    check_condition(file is not None, msg=errors.NO_FILE)

    if inputOperator is None:
        return

    check_condition(
        inputOperator == '/', 
        color=colors.WARNINGYELLOW, 
        msg=errors.INVALID_OPPERATOR, 
        leave=False,
    )
    check_condition(inputFile is not None, msg=errors.NO_FILE)

    if exitOperator is None:
        return

    check_condition(
        exitOperator == '/',
        color=colors.WARNINGYELLOW,
        msg=errors.INVALID_OPPERATOR,
        leave=False
    )
    check_condition(exitFile is not None, msg=errors.NO_FILE)


def main(**kwargs):
    whole_input_check(
        kwargs.get("file"),
        kwargs.get("operator"),    
        kwargs.get("inputFile"),
        kwargs.get("exitOperator"),    
        kwargs.get("exitFile"),
    )

    does_need_suffix = lambda file: file if file[-3:] == ".cc" else f"{file}.cc"
    file = does_need_suffix(kwargs.get("file"))

    gpp_assert_file_in_dir(file)
    targetLine = locate_target_line(file, target="//dbg\n")
    replace_line(file, targetLine, replacementLine="#define DBG_MODE\n")
    os.system(f"g++ {file}")
    replace_line(file, targetLine, replacementLine="//dbg\n")

    running_msg(file, kwargs.get("inputFile"), kwargs.get("exitFile"))

    if kwargs.get("inputOperator") is None:
        os.system("./a.out")
        exit()

    programOutput = cpp_program_interact(get_file_lines(kwargs.get("inputFile")))

    if kwargs.get("exitFile") is None:
        def _print_file_lines(lines: List[str], pend='') -> None:
            for line in lines:
                print(line, end=pend)
        
        _print_file_lines(programOutput, pend='\n')
        exit()

    write_file_lines(kwargs.get("exitFile"), programOutput)
    print(f"{colors.OKGREEN}[SUCCESS]{colors.ENDC} Write lines to file {kwargs.get('exitFile')} successful")


if __name__ == '__main__':
    check_condition(len(sys.argv) > 6, expect=False, msg="MAX OF 6 ARGUMENTS IS TO BE PROVIDED")
    main(
        file=sys.argv[1] if len(sys.argv) >= 2 else None, 
        operator=sys.argv[2] if len(sys.argv) >= 3 else None, 
        inputFile=sys.argv[3] if len(sys.argv) >= 4 else None, 
        exitOperator=sys.argv[4] if len(sys.argv) >= 5 else None, 
        exitFile=sys.argv[5] if len(sys.argv) == 6 else None,
    )
