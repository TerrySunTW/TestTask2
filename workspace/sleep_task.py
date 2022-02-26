import sys
import os
import json
import argparse
import time

def Do_Task(args):
    time.sleep(int(args.sleep_duration))
    f=open("out/result.txt","w")
    f.write(json.dumps(args))
    f.close()

def ParameterValidator(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-sleep_duration', required=True, help="sleep second for task. (ex: 30)")
    args = parser.parse_args(arguments)
    print(args)
    return args

def main(arguments):
    ValidatedArgs=ParameterValidator(arguments)
    Do_Task(ValidatedArgs)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

