from requests import get, Response
from json import dumps

def get_game_json(game: str, key: str)   ->  tuple[int, str]:
    # Construct URL
    url: str = f"https://api.rawg.io/api/games/{game}?key={key}"

    # Request data
    resp: Response = get(url=url, timeout=60)

    # Extract JSON if availible
    json_str: str
    if resp.status_code == 200:
        json_str = dumps(obj=resp.json(), indent=4)
    else:
        json_str = dumps(obj={})

    # Return data
    return (resp.status_code, json_str)
