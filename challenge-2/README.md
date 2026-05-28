# Challenge 2: REST API Best TV Shows in Genre

This folder contains the solution for Challenge 2.

Required file:

```text
solution_best_in_genre.py
```

Required function signature:

```python
def bestInGenre(genre: str) -> str:
```

The code uses Python 3.12, as required by the challenge.

## Problem

Given a genre, call the TV series API and return the name of the highest-rated
show in that genre.

API endpoint:

```text
https://jsonmock.hackerrank.com/api/tvseries
```

The API is paginated. Page 1 is requested like this:

```text
https://jsonmock.hackerrank.com/api/tvseries?page=1
```

Additional pages use the same `page` query parameter:

```text
https://jsonmock.hackerrank.com/api/tvseries?page=2
```

## Rules

- Match genres case-insensitively.
- A show can have multiple genres separated by commas.
- Choose the show with the highest `imdb_rating`.
- If two shows have the same rating, return the alphabetically lower name.
- Return an empty string when no valid show is found.

## Algorithm

The solution follows these steps:

1. Normalize the input genre by trimming spaces and converting it to lowercase.
2. Start on page 1.
3. Fetch the current page with HTTP GET.
4. Read `total_pages` from the API response.
5. Loop through each show in the page data.
6. Split the show's genre string by commas and normalize each genre.
7. Skip shows that do not match the requested genre.
8. Convert `imdb_rating` into a number.
9. Skip shows with missing or invalid ratings.
10. Keep the best show seen so far.
11. Continue until every page has been processed.
12. Return the best show name.

## Example

Input:

```python
bestInGenre("Action")
```

Output:

```python
"Game of Thrones"
```

## Why The Code Is Split Into Helpers

The challenge only requires `bestInGenre`, but the solution also uses small
private helper functions:

- `_fetch_page(...)` handles the HTTP GET request.
- `_normalize_genre(...)` makes genre comparison consistent.
- `_show_has_genre(...)` checks comma-separated genre values.
- `_parse_rating(...)` converts API ratings into numbers.
- `_is_better_candidate(...)` handles rating and tie-breaking rules.

This keeps the main function focused on the challenge logic while preserving
the exact required public function signature.

## Run The Sample

From this folder:

```bash
python3 solution_best_in_genre.py
```

This performs a real API request and prints the result for `"Action"`.

## Run The Tests

From this folder:

```bash
python3 -m unittest discover -s tests
```

The tests use fake API pages, so they do not need internet access.

The tests cover:

- The official sample result.
- Pagination.
- Case-insensitive genre matching.
- Multiple comma-separated genres.
- Alphabetical tie-breaking.
- Missing or invalid ratings.
- Empty results.
