# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import argparse
import os
import time

DEBUG_DEFINITION = 'DBG_MODE'

class Timer:
    def __init__(self):
        self.tics = [time.perf_counter()]

    def add_tic(self):
        self.tics.append(time.perf_counter())

    def get_elapsed(self):
        try:
            return str('{:.3f}'.format(self.tics[-1] - self.tics[-2]))
        except IndexError:
            print('Elapsed is null')
            exit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='File to run')
    args = parser.parse_args()

    file = args.file

    if not file.endswith('.cpp'):
        file += '.cpp'

    if file.startswith('.\\'):
        file = file[2:]

    assert(file in os.listdir())

    print(f'[DEBUG MODE] Compiling {file} with c++17...')

    compileTime = Timer()
    os.system(f'g++ -g -std=c++17 -Wall -D{DEBUG_DEFINITION} {file}')
    compileTime.add_tic()

    print(f'Successfully compiled in {compileTime.get_elapsed()}s')
    print('--------------------')
    os.system('a.exe')


if __name__ == '__main__':
    main()
