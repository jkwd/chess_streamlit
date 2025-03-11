"""A source loading player profiles and games from chess.com api"""

from typing import Any, Callable, Dict, Iterator, List, Sequence
import logging

import dlt
from dlt.common.typing import TDataItem
from dlt.sources import DltResource
from dlt.sources.helpers import requests

from .helpers import get_path_with_retry, get_url_with_retry
from .data_contracts import PlayersGames

# Create a logger
logger = logging.getLogger('dlt')

# Set the log level
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler('data/dlt.log')

# Add the handler to the logger
logger.addHandler(handler)


@dlt.source(name="chess")
def source(
    username: str
) -> Sequence[DltResource]:
    """
    A dlt source for the chess.com api. It groups several resources (in this case chess.com API endpoints) containing
    various types of data: user profiles or chess match results
    Args:
        players (List[str]): A list of the player usernames for which to get the data.
        start_month (str, optional): Filters out all the matches happening before `start_month`. Defaults to None.
        end_month (str, optional): Filters out all the matches happening after `end_month`. Defaults to None.
    Returns:
        Sequence[DltResource]: A sequence of resources that can be selected from including players_profiles,
        players_archives, players_games, players_online_status
    """
    return (
        players_games(username),
    )


@dlt.resource(
    write_disposition="replace",
    columns={
        "last_online": {"data_type": "timestamp"},
        "joined": {"data_type": "timestamp"},
    },
)
def players_profiles(username: str) -> TDataItem:
    """
    Yields player profile for a given player usernames.
    Args:
        username (str): player username to retrieve profile for.
    Yields:
        TDataItem: Player profiles data.
    """

    # get archives in parallel by decorating the http request with defer
    @dlt.defer
    def _get_profile(username: str) -> TDataItem:
        return get_path_with_retry(f"player/{username}")

    yield _get_profile(username)


@dlt.resource(write_disposition="replace", selected=False)
def players_archives(username: str) -> Iterator[List[TDataItem]]:
    """
    Yields url to game archives for a specified player username.
    Args:
        username: str: Player username to retrieve archives for.
    Yields:
        List[TDataItem]: List of player archive data.
    """

    data = get_path_with_retry(f"player/{username}/games/archives")
    yield data.get("archives", [])


@dlt.resource(
    write_disposition="replace", columns=PlayersGames
)
def players_games(
    username: str
) -> Iterator[Callable[[], List[TDataItem]]]:
    """
    Yields player's `username` games.
    Args:
        username: str: Player username to retrieve games for.
    Yields:
        Iterator[Callable[[], List[TDataItem]]]: An iterator over callables that return a list of games for a player.
    """

    # get a list of already checked archives
    # from your point of view, the state is python dictionary that will have the same content the next time this function is called
    checked_archives = dlt.current.resource_state().setdefault("archives", [])
    # get player archives, note that you can call the resource like any other function and just iterate it like a list
    archives = players_archives(username)

    # get archives in parallel by decorating the http request with defer
    @dlt.defer
    def _get_archive(url: str) -> List[TDataItem]:
        logger.warning(f"Getting archive from {url}")
        try:
            games = get_url_with_retry(url).get("games", [])
            return games  # type: ignore
        except requests.HTTPError as http_err:
            # sometimes archives are not available and the error seems to be permanent
            if http_err.response.status_code == 404:
                return []
            raise

    # enumerate the archives
    for url in archives:
        # the `url` format is https://api.chess.com/pub/player/{username}/games/{YYYY}/{MM}
        
        # do not download archive again
        if url in checked_archives:
            continue
        checked_archives.append(url)
        
        # get the filtered archive
        yield _get_archive(url)