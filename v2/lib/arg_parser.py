import argparse
import os
from pprint import pprint
import sys

class Arg_Parser:
    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()

        parser.add_argument("-o", "--output_directory", type=str,
            required=False, default=os.environ.get("HOME", "/tmp"),
            metavar="folder",
            help="Folder for all outputs from the script",
        )

        parser.add_argument("-s", "--switch", type=str, required=False,
            metavar="hostname", help="Hostname of switch", action="append"
        )

        args            = parser.parse_args()
        output_dir      = args.output_directory
        script_function = parser.prog.replace(".py", "")

        if script_function.startswith("./"):
            script_function = script_function[2:]

        switches = []

        if args.switch:
            switches = args.switch
        else:
            print("ERROR: No switch(es) were specified\n")
            parser.print_help()
            sys.exit()

        return [switches, script_function, output_dir]
