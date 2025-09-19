"""
Open Source Video Game Database runner.

Copyright (C) 2025 Nicholas M. Synovic.

"""

import sys

from osvg.cli import CLI
from osvg.db import DB


def main() -> None:
    """
    Entrypoint to the `osvg` application.

    This function parses command-line arguments, instantiates the CLI class,
    and executes the appropriate subcommand based on the user's input.

    """
    # Parse the command line
    args: dict = CLI().parse().__dict__

    # Get the subparser that the user leveraged specified
    subparser_command: str = next(iter(args.keys()))[0].split(".")[0]

    # Match subparser to runner
    match subparser_command:
        case "init":
            DB(db_path=args["init.db"])
        case _:
            sys.exit(1)


if __name__ == "__main__":
    main()
