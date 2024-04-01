import argparse

from psyserver.init import init_dir
from psyserver.db import create_studies_table
from psyserver.run import run_server

__version__ = "0.5.0"


def main():
    parser = argparse.ArgumentParser(
        prog="psyserver",
        description=("A server for hosting online studies."),
    )
    subparsers = parser.add_subparsers(
        title="commands",
        required=True,
    )

    # run command
    parser_run = subparsers.add_parser("run", help="run the server")
    parser_run.set_defaults(func=run_server)
    parser_run.add_argument(
        "psyserver_dir",
        nargs="?",
        default=None,
        help="path to the psyserver directory with config files.",
    )

    # config command
    parser_config = subparsers.add_parser(
        "init", help="create an example psyserver directory"
    )
    parser_config.set_defaults(func=init_dir)

    # init_db command
    parser_init_db = subparsers.add_parser(
        "init_db", help="Create the database file & table to track participant counts."
    )
    parser_init_db.set_defaults(func=create_studies_table)

    # parse arguments
    args = parser.parse_args()

    # run command
    if args.func == init_dir:
        return args.func()
    args.func(psyserver_dir=args.psyserver_dir)


if __name__ == "__main__":
    main()
