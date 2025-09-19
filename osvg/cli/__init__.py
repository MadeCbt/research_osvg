from argparse import ArgumentParser, Namespace, _SubParsersAction
from importlib.metadata import version
from pathlib import Path

import osvg


def resolve_path(path: str) -> Path:
    return Path(path).resolve()


class CLI:
    def __init__(self) -> None:
        # Set class args
        self.db_help: str = "Path to OSVG database"

        # Create parser and subparser
        self.parser: ArgumentParser = ArgumentParser(
            prog=osvg.PROGRAM_NAME,
            description=osvg.PROGRAM_DESCRPTION,
        )
        self.subparsers: _SubParsersAction[ArgumentParser] = (
            self.parser.add_subparsers()
        )

        # Add version argument
        self.parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=version(distribution_name="osvg"),
        )

        # Implement subparsers
        self._add_init()  # Step 0

    def _add_init(self) -> None:
        self.init_parser: ArgumentParser = self.subparsers.add_parser(
            name="init",
            description="Step 0",
        )
        self.init_parser.add_argument(
            "-d",
            "--db",
            type=resolve_path,
            required=True,
            help=self.db_help,
        )

    def parse(self) -> Namespace:
        return self.parser.parse_args()
