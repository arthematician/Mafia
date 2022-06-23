#!/usr/bin/env python
import time
import sys
import argparse
from mafia import Mafia


def doArgs(argList, name):
    parser = argparse.ArgumentParser(description = name)
    parser.add_argument('-s', '--scenario', help = 'Scenario of the game', default = 'Ranger')
    return parser.parse_args(argList)

def main():
    progName = "Mafia game"
    args = doArgs(sys.argv[1:], progName)
    print('args:', args.scenario)

    print ("Starting %s" % (progName))
    startTime = float(time.time())

    game = Mafia(scenario = args.scenario)
    result = game.run()

    print ("Finished in %0.4f seconds" % (time.time() - startTime))

if __name__ == '__main__':
    main()
