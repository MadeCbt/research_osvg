from datetime import datetime
from typing import Optional

from pandas import DataFrame
from pydantic import BaseModel
from pydantic_core import ValidationError


def validate_df(df: DataFrame, model: type[BaseModel]) -> None:
    for _, row in df.iterrows():
        try:
            model(**row.to_dict())
        except ValidationError:
            print(row)


class VideoGamesCSV(BaseModel):
    dataset_url: str
    name: str
    source_code_url: str
    steam_id: Optional[int] = None


class VideoGameDatasetsCSV(BaseModel):
    name: str
    url: str
    repository_url: str
    date_published: datetime
    author: str
    dataset_type: str
    dataset_uri: str
    notes: str
