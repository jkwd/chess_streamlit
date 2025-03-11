from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from typing import ClassVar
from dlt.common.libs.pydantic import DltConfig


class Accuracies(BaseModel):
    white: Optional[float] = None
    black: Optional[float] = None

class PlayerColor(BaseModel):
    rating: int
    result: str
    id: str = Field(alias="@id")
    username: str
    uuid: str

class PlayersGamesBase(BaseModel):
    url: str
    pgn: str
    time_control: str
    end_time: datetime
    rated: bool
    accuracies: Optional[Accuracies] = None
    tcn: str
    uuid: str
    initial_setup: str
    fen: str
    time_class: str
    rules: str
    white: PlayerColor
    black: PlayerColor

class PlayersGames(PlayersGamesBase):
  dlt_config: ClassVar[DltConfig] = {"skip_nested_types": True}
