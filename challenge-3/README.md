# Challenge 3: SQL Advertising System Failures Report

This folder contains the solution for Challenge 3.

Required file:

```text
applicant_query.sql
```

Required dialect:

```text
MySQL 8.x
```

## Problem

The advertising analytics team needs a report showing customers with more than
three failed campaign events.

An event is considered failed when:

```sql
status = 'failure'
```

## Tables

### customers

| Column | Type | Description |
| --- | --- | --- |
| `id` | `SMALLINT` | Customer ID |
| `first_name` | `VARCHAR(64)` | Customer first name |
| `last_name` | `VARCHAR(64)` | Customer last name |

### campaigns

| Column | Type | Description |
| --- | --- | --- |
| `id` | `SMALLINT` | Campaign ID |
| `customer_id` | `SMALLINT` | Customer ID |
| `name` | `VARCHAR(64)` | Campaign name |

### events

| Column | Type | Description |
| --- | --- | --- |
| `dt` | `VARCHAR(19)` | Event timestamp |
| `campaign_id` | `SMALLINT` | Campaign ID |
| `status` | `VARCHAR(64)` | Event status |

## Output

The query returns:

| Column | Meaning |
| --- | --- |
| `customer` | Customer full name, built from `first_name` and `last_name` |
| `failures` | Number of failed events across all campaigns for that customer |

Example:

| customer | failures |
| --- | ---: |
| Whitney Ferrero | 6 |

## Query Logic

The query works like this:

1. Start with `customers`.
2. Join each customer to their campaigns using `campaigns.customer_id`.
3. Join each campaign to its events using `events.campaign_id`.
4. Keep only rows where `events.status = 'failure'`.
5. Group the remaining rows by customer.
6. Count how many failed events each customer has.
7. Keep only customers where the failure count is greater than `3`.
8. Order the report by the failure count in descending order.

## Why `GROUP BY` Uses All Customer Columns

The query groups by:

```sql
c.id, c.first_name, c.last_name
```

Grouping by `c.id` keeps each customer distinct. Including `first_name` and
`last_name` keeps the query compatible with MySQL's `ONLY_FULL_GROUP_BY` mode,
which is commonly enabled in MySQL 8.x.

## Run Locally

Run the SQL file in a MySQL 8.x database that contains the required tables:

```bash
mysql your_database < applicant_query.sql
```

## Run The Tests

From the repository root:

```bash
python3 -m unittest discover -s challenge-3/tests
```

The tests verify the query structure and run a behavior check using an in-memory
SQLite database. For the behavior check only, the MySQL `CONCAT(...)` expression
is translated to SQLite string concatenation.
