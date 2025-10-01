from pathlib import Path

from pandas import DataFrame
from sqlalchemy import (
    Column,
    DateTime,
    Engine,
    ForeignKeyConstraint,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)


class DB:
    def __init__(self, db_path: Path) -> None:
        # Instantiate class variables
        self.db_path: Path = db_path
        self.metadata: MetaData = MetaData()

        # Create connection to the database
        self.engine: Engine = create_engine(url=f"sqlite:///{db_path}")

        # Create tables if they do not already exists
        self._create_tables()

    def _create_tables(self) -> None:
        # Datasets table
        _: Table = Table(
            "datasets",
            self.metadata,
            Column("_id", Integer, primary_key=True),
            Column("author", String),
            Column("name", String),
            Column("dataset_type", String),
            Column("date_published", DateTime),
            Column("url", String),
            Column("repository_url", String),
            Column("dataset_uri", String),
        )

        # video_game table
        _: Table = Table(
            "video_games",
            self.metadata,
            Column("_id", Integer, primary_key=True),
            Column("dataset_url", String),
            Column("name", String),
            Column("source_code_url", String),
            Column("steam_id", Integer),
        )

        # video game to dataset table
        _: Table = Table(
            "video_games_to_datasets",
            self.metadata,
            Column("_id", Integer, primary_key=True),
            Column("video_game_id", Integer),
            Column("dataset_id", Integer),
            ForeignKeyConstraint(["dataset_id"], ["datasets._id"]),
            ForeignKeyConstraint(["video_game_id"], ["video_games._id"]),
        )

        self.metadata.create_all(bind=self.engine, checkfirst=True)

    def write_df_to_table(self, df: DataFrame, table: str) -> None:
        df.to_sql(
            name=table,
            con=self.engine,
            if_exists="append",
            index=True,
            index_label="_id",
        )
