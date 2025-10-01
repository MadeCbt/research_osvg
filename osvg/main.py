"""
Open Source Video Game Database runner.

Copyright (C) 2025 Nicholas M. Synovic.

"""

import sys
from pathlib import Path

import pandas
from pandas import DataFrame
from pydantic import BaseModel

import osvg.types as osvg_types
from osvg.cli import CLI
from osvg.db import DB


def read_csv_file(filepath: Path, model: type[BaseModel]) -> DataFrame:
    # Read file
    df: DataFrame = pandas.read_csv(
        filepath_or_buffer=filepath,
        encoding="utf-8",
    )

    # Set all columns to be lower case
    df.columns = df.columns.str.lower()

    # Validate DataFrame against model
    osvg_types.validate_df(df=df, model=model)

    # Return DataFrame
    return df


def load_datasets_handler(df: DataFrame, db: DB) -> None:
    df.columns = df.columns.str.lower()  # Make all columns lowercase
    df = df.drop(columns="notes")  # Remove extra columns
    df.to_sql(
        name="datasets",
        if_exists="append",
        con=db.engine,
        index=True,
        index_label="_id",
    )


def load_video_games_handler(df: DataFrame, db: DB) -> None:
    df.columns = df.columns.str.lower()  # Make all columns lowercase
    df.to_sql(
        name="video_games",
        if_exists="append",
        con=db.engine,
        index=True,
        index_label="_id",
    )


def main() -> None:
    """
    Entrypoint to the `osvg` application.

    This function parses command-line arguments, instantiates the CLI class,
    and executes the appropriate subcommand based on the user's input.

    """
    # Parse the command line
    args: dict = CLI().parse().__dict__

    # Get the subparser that the user leveraged specified
    subparser_command: str = next(iter(args.keys())).split(".")[0]

    # Match subparser to runner
    match subparser_command:
        case "load":
            # Connect to the database
            db: DB = DB(db_path=args["load.db"])

            # Read video games CSV file
            video_games_df: DataFrame = read_csv_file(
                filepath=args["load.video_games"],
                model=osvg_types.VideoGamesCSV,
            )

            # Read datasets CSV file
            datasets_df: DataFrame = read_csv_file(
                filepath=args["load.datasets"],
                model=osvg_types.VideoGameDatasetsCSV,
            )

        case _:
            sys.exit(1)


if __name__ == "__main__":
    main()
