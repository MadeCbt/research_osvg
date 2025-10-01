"""
Open Source Video Game Database runner.

Copyright (C) 2025 Nicholas M. Synovic.

"""

import sys
from pathlib import Path

import pandas
from pandas import DataFrame, Series
from pandas.core.groupby import DataFrameGroupBy
from pydantic import BaseModel

import osvg.types as osvg_types
from osvg.cli import CLI
from osvg.db import DB


def read_csv_file(filepath: Path, model: type[BaseModel]) -> DataFrame:
    # Read file
    df: DataFrame = pandas.read_csv(
        filepath_or_buffer=filepath,
        encoding="utf-8",
        engine="pyarrow",
        date_format="%-m/%-d/%Y",
    )

    # Set all columns to be lower case
    df.columns = df.columns.str.lower()

    # Validate DataFrame against model
    osvg_types.validate_df(df=df, model=model)

    # Return DataFrame
    return df


def create_video_game_to_dataset_table(
    video_game_df: DataFrame,
    dataset_df: DataFrame,
) -> tuple[DataFrame, DataFrame]:
    # Data structure to store information
    data: dict[str, list[int]] = {"video_game_id": [], "dataset_id": []}

    # Create unique video games dataframe
    unique_vg_df: DataFrame = video_game_df.copy().drop_duplicates(
        subset="source_code_url"
    )

    # Iterate through unique video game rows
    idx: int
    row: Series
    for idx, row in unique_vg_df.iterrows():
        # Get the video game source
        vg_source: str = row["source_code_url"]

        # Find all instances of that video game in the original DataFrame
        vg_specific_df: DataFrame = video_game_df[
            video_game_df["source_code_url"] == vg_source
        ]

        # Get all datasets associated with this video game
        vg_datasets: Series[str] = vg_specific_df["dataset_url"]

        # Iterate through datasets
        dataset: str
        for dataset in vg_datasets:
            # Lookup dataset ID in the dataset DataFrame
            dataset_id: int = dataset_df[dataset_df["url"] == dataset].index[0]

            # Append information to the data structure
            data["video_game_id"].append(idx)
            data["dataset_id"].append(dataset_id)

    return (unique_vg_df, DataFrame(data=data))


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

            # Create many to many DataFrame table
            video_games_df, vg2ds_df = create_video_game_to_dataset_table(
                video_game_df=video_games_df,
                dataset_df=datasets_df,
            )

            # Format DataFrames
            datasets_df = datasets_df.drop(columns="notes")

            # Write data to tables
            db.write_df_to_table(df=datasets_df, table="datasets")
            db.write_df_to_table(df=video_games_df, table="video_games")
            db.write_df_to_table(
                df=vg2ds_df,
                table="video_games_to_datasets",
            )

        case _:
            sys.exit(1)


if __name__ == "__main__":
    main()
