-- Create DB
CREATE DATABASE demo;
USE demo;

-- Create a sample table partitioned by date
CREATE TABLE sales (
    id INT,
    sale_date DATE,
    amount DECIMAL(10,2)
)
DUPLICATE KEY(id)
PARTITION BY RANGE(sale_date) (
    PARTITION p2025_08_09 VALUES [('2025-08-09'), ('2025-08-10')),
    PARTITION p2025_08_10 VALUES [('2025-08-10'), ('2025-08-11')),
    PARTITION p2025_08_11 VALUES [('2025-08-11'), ('2025-08-12'))
)
DISTRIBUTED BY HASH(id) BUCKETS 1
PROPERTIES (
    "replication_num" = "1"
);

-- Insert some sample data
INSERT INTO sales VALUES
(1, '2025-08-09', 100.50),
(2, '2025-08-10', 200.75),
(3, '2025-08-11', 300.00);
