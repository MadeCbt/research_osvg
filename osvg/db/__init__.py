from pathlib import Path

from sqlalchemy import (
    Column,
    DateTime,
    Engine,
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
        # Author table
        _: Table = Table(
            "authors",
            self.metadata,
            Column("_id", Integer, primary_key=True),
            Column("name", String),
            Column("email", String),
            Column("github_account", String),
            Column("github_author_api", String),
        )

        # Datasets table
        _: Table = Table(
            "datasets",
            self.metadata,
            Column("_id", Integer, primary_key=True),
            Column("author_id", Integer),
            Column("name", String),
            Column("dataset_type", String),
            Column("date_published", DateTime),
            Column("date_collected", DateTime),
            Column("url", String),
            Column("repository_url", String),
            Column("dataset_uri", String),
            Column("raw_dataset", String),
        )

        # # video_game table
        # _: Table = Table(
        #     "video_games",
        #     self.metadata,
        #     Column(
        #         "id",
        #         Integer,
        #         primary_key=True,
        #     ),
        #     Column(
        #         "dataset_id",
        #         Integer,
        #     ),
        #     Column("name", String),
        #     ForeignKeyConstraint(["dataset_id"], ["datasets.id"]),
        # )

        self.metadata.create_all(bind=self.engine, checkfirst=True)


DB(Path("test.db"))
