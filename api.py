import requests
from config import TMDB_API_KEY, BASE_URL, LANG

def tmdb_get(endpoint, params=None):
    params = params or {}
    params["api_key"] = TMDB_API_KEY
    params["language"] = LANG

    try:
        r = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"~ API error: {e}")
        return None
