# REST API: Best TV Shows in Genre
# Language: Python 3.12

from __future__ import annotations

import json
from urllib.parse import urlencode
from urllib.request import urlopen

API_URL = "https://jsonmock.hackerrank.com/api/tvseries"
REQUEST_TIMEOUT_SECONDS = 10


def _fetch_page(page: int) -> dict:
    """
    Fetch one page from the TV series API.

    The challenge requires HTTP GET. urlopen performs a GET request when no
    request body is provided.
    """
    query_string = urlencode({"page": page})
    url = f"{API_URL}?{query_string}"

    with urlopen(url, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        response_body = response.read().decode("utf-8")

    return json.loads(response_body)


def _normalize_genre(genre: str) -> str:
    """Prepare a genre for case-insensitive comparison."""
    return genre.strip().lower()


def _show_has_genre(show: dict, target_genre: str) -> bool:
    """
    Check whether a show belongs to the requested genre.

    The API stores genres as a comma-separated string, for example:
    "Action, Adventure, Drama".
    """
    genres_text = show.get("genre") or ""
    genres = [
        _normalize_genre(genre)
        for genre in genres_text.split(",")
        if genre.strip()
    ]

    return target_genre in genres


def _parse_rating(raw_rating) -> float | None:
    """
    Convert the API rating into a number.

    Invalid or missing ratings are ignored by returning None.
    """
    if raw_rating is None:
        return None

    try:
        return float(raw_rating)
    except (TypeError, ValueError):
        return None


def _is_better_candidate(
    candidate_name: str,
    candidate_rating: float,
    best_name: str | None,
    best_rating: float,
) -> bool:
    """
    Decide if the current show should become the new answer.

    A candidate wins when it has a higher rating. If ratings are equal, the
    alphabetically lower name wins, as required by the challenge.
    """
    if candidate_rating > best_rating:
        return True

    is_tied_rating = candidate_rating == best_rating
    is_alphabetically_lower = best_name is None or candidate_name < best_name

    return is_tied_rating and is_alphabetically_lower


def bestInGenre(genre: str) -> str:
    """
    Finds the highest-rated TV series in the given genre.

    Parameters:
        genre (str): The genre to search for (e.g., 'Action', 'Comedy', 'Drama')

    Returns:
        str: The name of the highest-rated show in the genre. If there is a tie,
             returns the alphabetically lower name. Returns the name as a string.

    Notes:
        - Ties are broken by alphabetical order of the show name
        - Genre matching is case-insensitive
        - Shows can have multiple genres (comma-separated)
    """
    target_genre = _normalize_genre(genre or "")
    best_name: str | None = None
    best_rating = float("-inf")

    current_page = 1
    total_pages = 1

    while current_page <= total_pages:
        page_data = _fetch_page(current_page)
        total_pages = int(page_data.get("total_pages", 1) or 1)

        for show in page_data.get("data", []) or []:
            if not _show_has_genre(show, target_genre):
                continue

            rating = _parse_rating(show.get("imdb_rating"))
            if rating is None:
                continue

            name = show.get("name")
            if not isinstance(name, str) or not name:
                continue

            if _is_better_candidate(name, rating, best_name, best_rating):
                best_name = name
                best_rating = rating

        current_page += 1

    return best_name if best_name is not None else ""


if __name__ == "__main__":
    result = bestInGenre("Action")
    print(repr(result))
