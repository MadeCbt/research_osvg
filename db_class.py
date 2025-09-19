from pathlib import Path
from sqlalchemy import (
    Column,
    Engine,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Text,
    DateTime,
    Boolean,
    Table,
    create_engine,
    text,
)
from sqlalchemy.sql import func
from datetime import datetime


class DB:
    def __init__(self, db_path: Path) -> None:
        # Establish class variables
        self.db_path = db_path
        self.metadata: MetaData = MetaData()
        
        # Connect to the database
        self.engine: Engine = create_engine(
            url=f"sqlite:///{self.db_path}",
            echo=False
        )
        
        # Create tables and write constants if they do not exist
        self._create_tables()
        self._write_constants()

    def _create_tables(self) -> None:
        # Authors table
        _: Table = Table(
            "authors",
            self.metadata,
            Column("_id", Integer, primary_key=True),
            Column("name", String(255)),
            Column("email", String(255)),
            Column("created_at", DateTime, default=func.now()),
            Column("updated_at", DateTime, onupdate=func.now()),
            Column("is_active", Boolean, default=True),
        )

        # Publishers table
        _: Table = Table(
            "publishers",
            self.metadata,
            Column("_id", Integer, primary_key=True),
            Column("name", String(255)),
            Column("email", String(255)),
            Column("created_at", DateTime, default=func.now()),
            Column("updated_at", DateTime, onupdate=func.now()),
            Column("is_active", Boolean, default=True),
        )

        # Repos table
        _: Table = Table(
            "repos",
            self.metadata,
            Column("_id", Integer, primary_key=True),
            Column("title", String(255)),
            Column("author", String(255)),
            Column("url", String(500)),
            Column("gh_metadata", Text),
            Column("created_at", DateTime, default=func.now()),
            Column("updated_at", DateTime, onupdate=func.now()),
            Column("is_active", Boolean, default=True),
        )

        # Indexers table
        _: Table = Table(
            "indexers",
            self.metadata,
            Column("_id", Integer, primary_key=True),
            Column("title", String(255)),
            Column("url", String(500)),
            Column("metadata", Text),
            Column("created_at", DateTime, default=func.now()),
            Column("updated_at", DateTime, onupdate=func.now()),
            Column("is_active", Boolean, default=True),
        )

        # Marketplaces table
        _: Table = Table(
            "marketplaces",
            self.metadata,
            Column("_id", Integer, primary_key=True),
            Column("title", String(255)),
            Column("author", String(255)),
            Column("publisher_id", Integer, ForeignKey("publishers._id")),
            Column("url", String(500)),
            Column("created_at", DateTime, default=func.now()),
            Column("updated_at", DateTime, onupdate=func.now()),
            Column("is_active", Boolean, default=True),
        )

        # Video Games table
        _: Table = Table(
            "video_games",
            self.metadata,
            Column("_id", Integer, primary_key=True),
            Column("title", String(255)),
            Column("author_id", Integer, ForeignKey("authors._id")),
            Column("repo_id", Integer, ForeignKey("repos._id")),
            Column("marketplace_id", Integer, ForeignKey("marketplaces._id")),
            Column("indexer_id", Integer, ForeignKey("indexers._id")),
            Column("description", Text),
            Column("genre", String(100)),
            Column("version", String(50)),
            Column("rating", String(10)),
            Column("price", String(20)),
            Column("created_at", DateTime, default=func.now()),
            Column("updated_at", DateTime, onupdate=func.now()),
            Column("is_published", Boolean, default=False),
        )

        # Datasets table
        _: Table = Table(
            "datasets",
            self.metadata,
            Column("_id", Integer, primary_key=True),
            Column("title", String(255)),
            Column("author", String(255)),
            Column("url", String(500)),
            Column("repo_id", Integer, ForeignKey("repos._id")),
            Column("video_game_id", Integer, ForeignKey("video_games._id")),
            Column("dataset_type", String(100)),
            Column("file_size", Integer),
            Column("created_at", DateTime, default=func.now()),
            Column("updated_at", DateTime, onupdate=func.now()),
            Column("is_active", Boolean, default=True),
        )

        self.metadata.create_all(bind=self.engine, checkfirst=True)

    def _write_constants(self) -> None:
        """Write any constant data needed for the database."""
        pass

    def get_last_row_id(self, table_name: str) -> int:
        """Get the last row ID from a specified table."""
        sql = text(f"SELECT _id FROM {table_name} ORDER BY _id DESC;")
        try:
            with self.engine.connect() as conn:
                result = conn.execute(statement=sql).first()
                return result[0] if result else 0
        except (TypeError, AttributeError):
            return 0

    def insert_author(self, name: str, email: str) -> int:
        """Insert a new author and return the ID."""
        sql = text("""
            INSERT INTO authors (name, email, created_at, is_active) 
            VALUES (:name, :email, :created_at, :is_active)
        """)
        with self.engine.connect() as conn:
            conn.execute(sql, {
                "name": name,
                "email": email,
                "created_at": datetime.now(),
                "is_active": True
            })
            conn.commit()
        return self.get_last_row_id("authors")

    def insert_video_game(self, title: str, author_id: int, **kwargs) -> int:
        """Insert a new video game and return the ID."""
        sql = text("""
            INSERT INTO video_games (title, author_id, repo_id, marketplace_id, 
                                   indexer_id, description, genre, version, 
                                   rating, price, created_at, is_published) 
            VALUES (:title, :author_id, :repo_id, :marketplace_id, 
                    :indexer_id, :description, :genre, :version, 
                    :rating, :price, :created_at, :is_published)
        """)
        with self.engine.connect() as conn:
            conn.execute(sql, {
                "title": title,
                "author_id": author_id,
                "repo_id": kwargs.get("repo_id"),
                "marketplace_id": kwargs.get("marketplace_id"),
                "indexer_id": kwargs.get("indexer_id"),
                "description": kwargs.get("description"),
                "genre": kwargs.get("genre"),
                "version": kwargs.get("version"),
                "rating": kwargs.get("rating"),
                "price": kwargs.get("price"),
                "created_at": datetime.now(),
                "is_published": kwargs.get("is_published", False)
            })
            conn.commit()
        return self.get_last_row_id("video_games")

    def get_all_games(self) -> list:
        """Get all video games with author information."""
        sql = text("""
            SELECT vg._id, vg.title, vg.genre, vg.price, vg.is_published,
                   vg.description, vg.version, vg.rating,
                   a.name as author_name, a.email as author_email
            FROM video_games vg
            LEFT JOIN authors a ON vg.author_id = a._id
            ORDER BY vg._id
        """)
        with self.engine.connect() as conn:
            return conn.execute(sql).fetchall()

    def get_all_authors(self) -> list:
        """Get all authors."""
        sql = text("SELECT _id, name, email, is_active FROM authors ORDER BY _id")
        with self.engine.connect() as conn:
            return conn.execute(sql).fetchall()

    def delete_game(self, game_id: int) -> bool:
        """Delete a video game by ID."""
        sql = text("DELETE FROM video_games WHERE _id = :id")
        try:
            with self.engine.connect() as conn:
                result = conn.execute(sql, {"id": game_id})
                conn.commit()
                return result.rowcount > 0  # True if a row was deleted
        except Exception:
            return False

    def delete_author(self, author_id: int) -> bool:
        """Delete an author by ID. Note: Will fail if author has games."""
        sql = text("DELETE FROM authors WHERE _id = :id")
        try:
            with self.engine.connect() as conn:
                result = conn.execute(sql, {"id": author_id})
                conn.commit()
                return result.rowcount > 0  # True if a row was deleted
        except Exception:
            return False

    def delete_author_and_games(self, author_id: int) -> bool:
        """Delete an author and all their games."""
        try:
            with self.engine.connect() as conn:
                # First delete all games by this author
                conn.execute(text("DELETE FROM video_games WHERE author_id = :id"), {"id": author_id})
                # Then delete the author
                result = conn.execute(text("DELETE FROM authors WHERE _id = :id"), {"id": author_id})
                conn.commit()
                return result.rowcount > 0
        except Exception:
            return False
