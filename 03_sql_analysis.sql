USE olist_ecommerce;

-- 0. Quick Sanity Check (Should return 99441)
SELECT COUNT(*) AS total_records FROM customers;


-- ====================================================================
-- Query 1: Pareto Cumulative State Concentration (Window Function: SUM() OVER)
-- Business Question: What is the cumulative customer share by top states?
-- ====================================================================
WITH state_summary AS (
    SELECT 
        customer_state,
        COUNT(customer_id) AS total_orders,
        ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS state_pct
    FROM customers
    GROUP BY customer_state
)
SELECT 
    customer_state,
    total_orders,
    state_pct,
    ROUND(SUM(state_pct) OVER (ORDER BY total_orders DESC), 2) AS cumulative_running_pct
FROM state_summary
ORDER BY total_orders DESC
LIMIT 10;


-- ====================================================================
-- Query 2: Top 3 Cities per State (DENSE_RANK() OVER Partitioning)
-- Business Question: In each state, which top 3 cities drive the most volume?
-- ====================================================================
WITH city_ranks AS (
    SELECT 
        customer_state,
        customer_city,
        COUNT(customer_id) AS order_count,
        DENSE_RANK() OVER (
            PARTITION BY customer_state 
            ORDER BY COUNT(customer_id) DESC
        ) AS city_rank
    FROM customers
    GROUP BY customer_state, customer_city
)
SELECT 
    customer_state,
    customer_city,
    order_count,
    city_rank
FROM city_ranks
WHERE city_rank <= 3
ORDER BY customer_state, city_rank;


-- ====================================================================
-- Query 3: Customer Retention & Frequency Segmentation (Case Logic)
-- Business Question: How many customers are repeat buyers vs one-time purchasers?
-- ====================================================================
WITH customer_orders AS (
    SELECT 
        customer_unique_id,
        COUNT(customer_id) AS purchase_frequency
    FROM customers
    GROUP BY customer_unique_id
)
SELECT 
    CASE 
        WHEN purchase_frequency = 1 THEN 'One-Time Buyer'
        WHEN purchase_frequency BETWEEN 2 AND 3 THEN 'Repeat Buyer (Low Frequency)'
        ELSE 'Loyal Buyer (4+ Orders)'
    END AS customer_tier,
    COUNT(customer_unique_id) AS total_customers,
    ROUND(COUNT(customer_unique_id) * 100.0 / (SELECT COUNT(DISTINCT customer_unique_id) FROM customers), 2) AS tier_percentage
FROM customer_orders
GROUP BY customer_tier
ORDER BY total_customers DESC;