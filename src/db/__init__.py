from sqlalchemy import MetaData, Table, Engine, create_engine, Column, String, Integer, ForeignKeyConstraint
from pathlib import Path

class DB:
    def __init__(self, db_path: Path) -> None:
        # Instantiate class variables
        self.db_path: Path = db_path
        self.metadata: MetaData = MetaData()

        # Create connection to the database
        self.engine: Engine = create_engine(url=f"sqlite:///{db_path}")

        # Create tables if they do not already exists
        self._create_tables()

    def _create_tables(self)    ->  None:
        # datasets table
        _: Table = Table(
            "datasets",
            self.metadata,
            Column(
                "id",
                Integer,
                primary_key=True,
            ),
            Column(
                "name",
                String,
            ),
            Column(
                "url",
                String,
            ),
            Column(
                "type",
                String
            )
        )

        # video_game table
        _: Table = Table(
            "video_games",
            self.metadata,
            Column(
                "id",
                Integer,
                primary_key=True,
            ),
            Column(
                "dataset_id",
                Integer,
            ),
            Column(
                "name",
                String
            ),
            ForeignKeyConstraint(
                ["dataset_id"],
                ["datasets.id"]
            )
        )

        self.metadata.create_all(bind=self.engine, checkfirst=True)

DB(Path("test.db"))
