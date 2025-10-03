from datetime import datetime
from typing import Optional

from pandas import DataFrame
from pydantic import BaseModel
from pydantic_core import ValidationError


def validate_df(df: DataFrame, model: type[BaseModel]) -> None:
    for _, row in df.iterrows():
        model(**row.to_dict())


class VideoGamesCSV(BaseModel):
    dataset_url: str
    name: str
    source_code_url: str
    steam_id: Optional[int] = None


class VideoGameDatasetsCSV(BaseModel):
    name: str
    url: str
    repository_url: Optional[str] = None
    date_published: Optional[datetime] = None
    author: Optional[str] = None
    dataset_type: str
    dataset_uri: str
    notes: Optional[str] = None
