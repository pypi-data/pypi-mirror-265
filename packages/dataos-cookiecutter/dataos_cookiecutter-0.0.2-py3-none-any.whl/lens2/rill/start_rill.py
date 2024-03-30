import re
import subprocess
import os


def add_start_subparser(subparsers):
    subparsers.set_defaults(func=executes_start)


def executes_start():
    # Change directory to Rill directory
    os.chdir("rill")  # Change this to the actual path where Rill is installed

    # Run 'rill start --readonly' command
    start_command = "rill start --readonly"
    subprocess.run(start_command, shell=True)
