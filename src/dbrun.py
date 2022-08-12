#! /usr/bin/python3

# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

from typing import List, Optional
from subprocess import Popen, PIPE

import argparse
import os
import logging
import time

DBG_DEF = 'DBG_MODE'

class colors:
    OKGREEN = '\033[92m'
    WARNINGRED = '\033[91m'
    WARNINGYELLOW = '\033[93m'
    ENDC = '\033[0m'


class errors:
    EXPECTED_ARGUMENTS = '[EXPECTED ONE ARGUMENTS]'
    INVALID_OPPERATOR = '[INVALID OPPERATOR FOUND]'
    NO_FILE = '[EXPECTED FILE FOUND NONE]'
    LEN_MISSMATCH = '[LINE LENGTH MISSMATCH]'
    NO_TARGET_LINE = f'[COULD NOT FIND TARGET LINE]{colors.ENDC} -> None'

    @staticmethod
    def file_not_found(*args) -> None:
        for arg in args:
            logging.error(f'{colors.WARNINGRED}[FILE NOT FOUND]{colors.ENDC} NO FILE IN DIR NAMED -> {arg}')
        exit()

    @staticmethod
    def gpp_file_not_found(file: str) -> None:
        logging.error(f'g++:{colors.WARNINGRED} error: {colors.ENDC}{file}: No such file found')
        exit()


class timer:
    def __init__(self):
        self.tics = [time.perf_counter()]

    def add_tic(self) -> None:
        self.tics.append(time.perf_counter())

    def get_elapsed(self) -> str:
        try:
            return str('{:.3f}'.format(self.tics[-1] - self.tics[-2]))
        except IndexError:
            print('Elapsed is null')
            exit()


def check_condition(condition: bool = False, expect: bool = True, 
                    color: str = colors.WARNINGRED, msg: str = None, 
                    leave: bool = True) -> None:
    """Template for basic console logging"""
    try:
        assert(condition is expect)
    except AssertionError:
        logging.error(f'{color}{msg}{colors.ENDC}')
        exit() if leave else print(f'{colors.WARNINGYELLOW}[WORKING]{colors.ENDC}')


def running_msg(file: str, compileTime: time, inputFile: str = None, exitFile: str = None) -> None:
    print(f'[DEBUG MODE] Compiling {file} with C++17')
    print(f'Successfully compiled in {compileTime.get_elapsed()}s')
    if inputFile is not None:
        print(f'[INPUT FILE] Selected Input File is {inputFile}')
    if exitFile is not None:
        print(f'[OUTPUT FILE] Selected Output File is {exitFile}')
    print('--------------------')


def get_file_lines(fname: str) -> List[str]:
    try:
        with open(fname, 'r') as file:
            lines = file.readlines()
    except OSError:
        errors.file_not_found(fname)
    return lines


def create_file_if_needed(fname: str) -> None:
    if not fname in os.listdir():
        os.system(f'touch {fname}') 


def write_file_lines(fname: str, lines: List[str]) -> None:
    try:
        with open(fname, 'w') as file:
            file.writelines(lines)
    except OSError:
        errors.file_not_found(fname)


def locate_target_line(fname: str, target: str) -> Optional[int]:
    try:
        with open(fname, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line == target: 
                    return i
    except OSError:
        errors.file_not_found(fname)

    return None


def gpp_assert_file_in_dir(fname: str) -> None:
    try:
        assert(fname in os.listdir())
    except AssertionError:
        errors.gpp_file_not_found(fname)


def cpp_program_interact(lines: List[str]) -> List[str]:
    program = Popen([f'{os.getcwd()}/a.out'], stdout=PIPE, stdin=PIPE)
    for line in lines:
        program.stdin.write(line.encode('utf-8'))
    program.stdin.flush()
    return [line.decode() for line in program.stdout.readlines()]


def whole_input_check(file: str, inputOperator: str, inputFile: str, 
                      exitOperator: str, exitFile: str) -> None:
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


def main():
    logging.basicConfig(
        level=logging.DEBUG, 
        format=f'{colors.WARNINGRED}[ERROR - %(asctime)s]{colors.ENDC} - %(message)s',
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, metavar='N', nargs='+')
    args = parser.parse_args()

    file = args.input[0]
    inputOperator = args.input[1] if len(args.input) > 1 else None
    inputFile = args.input[2] if len(args.input) > 2 else None
    exitOperator = args.input[3] if len(args.input) > 3 else None
    exitFile = args.input[4] if len(args.input) > 4 else None

    whole_input_check(file, inputOperator, inputFile, exitOperator, exitFile)

    if not '.' in file:
        file += '.cpp'

    gpp_assert_file_in_dir(file)

    targetLine = locate_target_line(file, target=f'#ifdef {DBG_DEF}\n')
    check_condition(targetLine is not None, color=colors.WARNINGYELLOW, msg=errors.NO_TARGET_LINE, leave=False)

    compileTime = timer()
    os.system(f'g++ -g -std=c++17 -Wall -D{DBG_DEF} {file}')
    compileTime.add_tic()

    running_msg(file, compileTime, inputFile, exitFile)

    if inputOperator is None:
        os.system('./a.out')
        exit()

    programOutput = cpp_program_interact(get_file_lines(inputFile))

    if exitFile is None:
        def _print_file_lines(lines: List[str], pend='') -> None:
            for line in lines:
                print(line, end=pend)
        
        _print_file_lines(programOutput)
        exit()

    create_file_if_needed(exitFile)
    write_file_lines(exitFile, programOutput)
    print(f'{colors.OKGREEN}[SUCCESS]{colors.ENDC} Write lines to file {exitFile} successful')


if __name__ == '__main__':
    main()
