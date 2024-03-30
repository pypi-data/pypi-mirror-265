from lens2.rill import generate_rill, start_rill


def add_subparser(subparsers):
    rill_parser = subparsers.add_parser("rill")
    rill_parser.add_argument("action", choices=["create", "start"], help="Create lens rill yaml to explore view.")

    generate_rill.add_create_subparser(rill_parser)


def execute_rill(args):
    if args.action == "create":
        generate_rill.execute_create()
    elif args.action == "start":
        start_rill.executes_start()
