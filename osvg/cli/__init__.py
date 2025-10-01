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
        self._add_load_datasets()  # Step 1
        self._add_load_video_games()  # Step 2

    def _add_load_datasets(self) -> None:
        self.load_datasets_parser: ArgumentParser = self.subparsers.add_parser(
            name="load-datasets",
            description="Step 1",
        )
        self.load_datasets_parser.add_argument(
            "-d",
            "--db",
            type=lambda x: Path(x).resolve(),
            required=True,
            help=self.db_help,
            dest="load_datasets.db",
        )
        self.load_datasets_parser.add_argument(
            "-f",
            "--file",
            type=lambda x: Path(x).resolve(),
            required=True,
            help="Path to datasets CSV file",
            dest="load_datasets.file",
        )

    def _add_load_video_games(self) -> None:
        self.load_video_games_parser: ArgumentParser = self.subparsers.add_parser(
            name="load-video-games",
            description="Step 1",
        )
        self.load_video_games_parser.add_argument(
            "-d",
            "--db",
            type=lambda x: Path(x).resolve(),
            required=True,
            help=self.db_help,
            dest="load_video_games.db",
        )
        self.load_video_games_parser.add_argument(
            "-f",
            "--file",
            type=lambda x: Path(x).resolve(),
            required=True,
            help="Path to datasets CSV file",
            dest="load_video_games.file",
        )

    def parse(self) -> Namespace:
        """
        Parse the command-line arguments.

        Returns:
            A Namespace object containing the parsed arguments. This object
            provides access to the arguments as attributes (e.g., args.init.db).

        """
        return self.parser.parse_args()
