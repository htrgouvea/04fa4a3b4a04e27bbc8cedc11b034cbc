import re
import sqlite3
import unittest
from pathlib import Path

QUERY_PATH = Path(__file__).resolve().parents[1] / "applicant_query.sql"


def _read_query() -> str:
    return QUERY_PATH.read_text(encoding="utf-8")


def _remove_sql_comments(sql: str) -> str:
    lines = []
    for line in sql.splitlines():
        stripped = line.strip()
        if not stripped.startswith("--"):
            lines.append(line)
    return "\n".join(lines).strip()


def _sqlite_compatible_query(mysql_query: str) -> str:
    query_without_comments = _remove_sql_comments(mysql_query)
    return query_without_comments.replace(
        "CONCAT(c.first_name, ' ', c.last_name)",
        "c.first_name || ' ' || c.last_name",
    )


class ApplicantQueryTest(unittest.TestCase):
    def test_query_is_pure_select_statement(self):
        query = _remove_sql_comments(_read_query()).lower()

        self.assertTrue(query.startswith("select"))
        self.assertNotIn("insert ", query)
        self.assertNotIn("update ", query)
        self.assertNotIn("delete ", query)
        self.assertNotIn("create ", query)
        self.assertNotIn("drop ", query)
        self.assertNotIn("alter ", query)

    def test_query_uses_mysql_8_concat_for_customer_name(self):
        query = _read_query()

        self.assertIn("CONCAT(c.first_name, ' ', c.last_name) AS customer", query)

    def test_query_filters_groups_and_orders_failures(self):
        query = re.sub(r"\s+", " ", _remove_sql_comments(_read_query()).lower())

        self.assertIn("where e.status = 'failure'", query)
        self.assertIn("group by c.id, c.first_name, c.last_name", query)
        self.assertIn("having count(*) > 3", query)
        self.assertIn("order by failures desc", query)

    def test_query_returns_customers_with_more_than_three_failures(self):
        connection = sqlite3.connect(":memory:")
        cursor = connection.cursor()

        cursor.executescript(
            """
            CREATE TABLE customers (
                id SMALLINT,
                first_name VARCHAR(64),
                last_name VARCHAR(64)
            );

            CREATE TABLE campaigns (
                id SMALLINT,
                customer_id SMALLINT,
                name VARCHAR(64)
            );

            CREATE TABLE events (
                dt VARCHAR(19),
                campaign_id SMALLINT,
                status VARCHAR(64)
            );

            INSERT INTO customers VALUES
                (1, 'Whitney', 'Ferrero'),
                (2, 'Dickie', 'Romera'),
                (3, 'Ana', 'Silva');

            INSERT INTO campaigns VALUES
                (1, 1, 'Upton Group'),
                (2, 1, 'Roob, Hudson and Rippin'),
                (3, 2, 'Ruecker, Hand and Haley'),
                (4, 3, 'Third Customer Campaign');

            INSERT INTO events VALUES
                ('2021-12-01 01:00:00', 1, 'failure'),
                ('2021-12-01 02:00:00', 1, 'failure'),
                ('2021-12-01 03:00:00', 1, 'failure'),
                ('2021-12-01 04:00:00', 2, 'failure'),
                ('2021-12-01 05:00:00', 2, 'failure'),
                ('2021-12-01 06:00:00', 2, 'failure'),
                ('2021-12-01 07:00:00', 3, 'failure'),
                ('2021-12-01 08:00:00', 3, 'failure'),
                ('2021-12-01 09:00:00', 3, 'failure'),
                ('2021-12-01 10:00:00', 3, 'success'),
                ('2021-12-01 11:00:00', 4, 'failure'),
                ('2021-12-01 12:00:00', 4, 'failure'),
                ('2021-12-01 13:00:00', 4, 'failure'),
                ('2021-12-01 14:00:00', 4, 'failure');
            """
        )

        query = _sqlite_compatible_query(_read_query())
        result = cursor.execute(query).fetchall()

        self.assertEqual(
            result,
            [
                ("Whitney Ferrero", 6),
                ("Ana Silva", 4),
            ],
        )

        connection.close()


if __name__ == "__main__":
    unittest.main()
