-- Advertising System Failures Report
-- Dialect: MySQL 8.x
--
-- Goal:
-- Return every customer with more than 3 failed campaign events.
--
-- Output columns:
-- customer: first name and last name together
-- failures: number of events where status = 'failure'

SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer,
    COUNT(*) AS failures
FROM customers AS c
JOIN campaigns AS cp
    ON cp.customer_id = c.id
JOIN events AS e
    ON e.campaign_id = cp.id
WHERE e.status = 'failure'
GROUP BY c.id, c.first_name, c.last_name
HAVING COUNT(*) > 3
ORDER BY failures DESC;
