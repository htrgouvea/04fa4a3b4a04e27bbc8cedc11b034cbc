import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

SOLUTION_PATH = Path(__file__).resolve().parents[1] / "solution_best_in_genre.py"
SPEC = importlib.util.spec_from_file_location("solution_best_in_genre", SOLUTION_PATH)
solution_best_in_genre = importlib.util.module_from_spec(SPEC)

if SPEC.loader is None:
    raise ImportError(f"Could not load {SOLUTION_PATH}")

SPEC.loader.exec_module(solution_best_in_genre)
bestInGenre = solution_best_in_genre.bestInGenre


class BestInGenreTest(unittest.TestCase):
    def test_official_sample_action_returns_game_of_thrones(self):
        pages = {
            1: {
                "total_pages": 1,
                "data": [
                    {
                        "name": "Avatar: The Last Airbender",
                        "genre": "Action, Adventure, Animation",
                        "imdb_rating": "9.2",
                    },
                    {
                        "name": "Game of Thrones",
                        "genre": "Action, Adventure, Drama",
                        "imdb_rating": "9.3",
                    },
                    {
                        "name": "Shingeki no kyojin",
                        "genre": "Action, Adventure, Animation",
                        "imdb_rating": "8.9",
                    },
                ],
            },
        }

        with patch.object(solution_best_in_genre, "_fetch_page", side_effect=pages.get):
            self.assertEqual(bestInGenre("Action"), "Game of Thrones")

    def test_reads_all_pages(self):
        pages = {
            1: {
                "total_pages": 2,
                "data": [
                    {
                        "name": "First Page Comedy",
                        "genre": "Comedy",
                        "imdb_rating": "7.0",
                    },
                ],
            },
            2: {
                "total_pages": 2,
                "data": [
                    {
                        "name": "Second Page Comedy",
                        "genre": "Comedy",
                        "imdb_rating": "8.5",
                    },
                ],
            },
        }

        with patch.object(solution_best_in_genre, "_fetch_page", side_effect=pages.get):
            self.assertEqual(bestInGenre("Comedy"), "Second Page Comedy")

    def test_genre_matching_is_case_insensitive(self):
        pages = {
            1: {
                "total_pages": 1,
                "data": [
                    {
                        "name": "Drama Show",
                        "genre": "Drama",
                        "imdb_rating": "8.0",
                    },
                ],
            },
        }

        with patch.object(solution_best_in_genre, "_fetch_page", side_effect=pages.get):
            self.assertEqual(bestInGenre("dRaMa"), "Drama Show")

    def test_show_can_have_multiple_genres(self):
        pages = {
            1: {
                "total_pages": 1,
                "data": [
                    {
                        "name": "Mixed Genre Show",
                        "genre": "Comedy, Crime, Mystery",
                        "imdb_rating": "8.1",
                    },
                ],
            },
        }

        with patch.object(solution_best_in_genre, "_fetch_page", side_effect=pages.get):
            self.assertEqual(bestInGenre("Crime"), "Mixed Genre Show")

    def test_tie_uses_alphabetically_lower_name(self):
        pages = {
            1: {
                "total_pages": 1,
                "data": [
                    {
                        "name": "Zulu Show",
                        "genre": "Sci-Fi",
                        "imdb_rating": "9.0",
                    },
                    {
                        "name": "Alpha Show",
                        "genre": "Sci-Fi",
                        "imdb_rating": "9.0",
                    },
                ],
            },
        }

        with patch.object(solution_best_in_genre, "_fetch_page", side_effect=pages.get):
            self.assertEqual(bestInGenre("Sci-Fi"), "Alpha Show")

    def test_ignores_missing_and_invalid_ratings(self):
        pages = {
            1: {
                "total_pages": 1,
                "data": [
                    {
                        "name": "Missing Rating",
                        "genre": "Fantasy",
                        "imdb_rating": None,
                    },
                    {
                        "name": "Invalid Rating",
                        "genre": "Fantasy",
                        "imdb_rating": "unknown",
                    },
                    {
                        "name": "Valid Rating",
                        "genre": "Fantasy",
                        "imdb_rating": "8.4",
                    },
                ],
            },
        }

        with patch.object(solution_best_in_genre, "_fetch_page", side_effect=pages.get):
            self.assertEqual(bestInGenre("Fantasy"), "Valid Rating")

    def test_returns_empty_string_when_no_show_matches(self):
        pages = {
            1: {
                "total_pages": 1,
                "data": [
                    {
                        "name": "Comedy Show",
                        "genre": "Comedy",
                        "imdb_rating": "8.0",
                    },
                ],
            },
        }

        with patch.object(solution_best_in_genre, "_fetch_page", side_effect=pages.get):
            self.assertEqual(bestInGenre("Horror"), "")

    def test_returns_empty_string_for_empty_api_data(self):
        pages = {
            1: {
                "total_pages": 1,
                "data": [],
            },
        }

        with patch.object(solution_best_in_genre, "_fetch_page", side_effect=pages.get):
            self.assertEqual(bestInGenre("Action"), "")


if __name__ == "__main__":
    unittest.main()
