"""
Open Source Video Game Database CLI class.

Copyright (C) 2025 Nicholas M. Synovic.

"""

from argparse import ArgumentParser, Namespace, _SubParsersAction
from importlib.metadata import version
from pathlib import Path

import osvg


class CLI:
    """
    Represents the command-line interface (CLI) for the osvg application.

    Provides methods for parsing command-line arguments and managing the application's
    configuration.

    """

    def __init__(self) -> None:
        """
        Initialize a CLI object.

        Sets the default value for the database path argument.

        """
        # Set class args
        self.db_help: str = "Path to OSVG database"

        # Create parser and subparser
        self.parser: ArgumentParser = ArgumentParser(
            prog=osvg.PROGRAM_NAME,
            description=osvg.PROGRAM_DESCRIPTION,
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
        self._add_load()  # Step 1
        self._add_rawg()  # Step 2

    def _add_load(self) -> None:
        self.load_parser: ArgumentParser = self.subparsers.add_parser(
            name="load",
            description="Step 1",
        )
        self.load_parser.add_argument(
            "-d",
            "--db",
            type=lambda x: Path(x).resolve(),
            required=True,
            help=self.db_help,
            dest="load.db",
        )
        self.load_parser.add_argument(
            "--video-games",
            type=lambda x: Path(x).resolve(),
            required=True,
            help="Path to video games CSV file",
            dest="load.video_games",
        )
        self.load_parser.add_argument(
            "--datasets",
            type=lambda x: Path(x).resolve(),
            required=True,
            help="Path to datasets CSV file",
            dest="load.datasets",
        )

    def _add_rawg(self) -> None:
        self.rawg_parser: ArgumentParser = self.subparsers.add_parser(
            name="rawg",
            description="Step 2",
        )
        self.rawg_parser.add_argument(
            "-d",
            "--db",
            type=lambda x: Path(x).resolve(),
            required=True,
            help=self.db_help,
            dest="rawg.db",
        )
        self.rawg_parser.add_argument(
            "-k",
            "--key",
            type=str,
            required=True,
            help="RAWG developer key",
            dest="rawg.key",
        )

    def parse(self) -> Namespace:
        """
        Parse the command-line arguments.

        Returns:
            A Namespace object containing the parsed arguments. This object
            provides access to the arguments as attributes (e.g., args.init.db).

        """
        return self.parser.parse_args()
