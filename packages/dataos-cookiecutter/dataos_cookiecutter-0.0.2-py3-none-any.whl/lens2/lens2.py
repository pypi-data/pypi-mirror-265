# main script
import argparse
from lens2.checks import create_checks
from lens2.lens import create_lens
from lens2.rill import create_rill


def main():
    parser = argparse.ArgumentParser(description="Command-line interface for lens2")
    subparsers = parser.add_subparsers(dest="subcommand")

    create_checks.add_subparser(subparsers)
    create_lens.add_subparser(subparsers)
    create_rill.add_subparser(subparsers)

    args = parser.parse_args()

    if args.subcommand == "lens":
        create_lens.execute_lens(args)
    elif args.subcommand == "checks":
        create_checks.execute_checks(args)
    elif args.subcommand == "rill":
        create_rill.execute_rill(args)
    else:
        parser.print_help()
