-- Supabase Schema for Retail Agentic AI Platform

-- Inventory Table
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(255) NOT NULL,
    location_id VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    UNIQUE(sku, location_id)
);

-- Sales Table
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    region VARCHAR(255) NOT NULL,
    timeframe VARCHAR(255) NOT NULL,
    volume NUMERIC(15, 2) NOT NULL,
    UNIQUE(region, timeframe)
);

-- Orders Table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(255) UNIQUE NOT NULL,
    status VARCHAR(50) NOT NULL,
    days_delayed INT DEFAULT 0
);

-- Products Table (For Finance/Margin calculations)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(255) UNIQUE NOT NULL,
    category VARCHAR(255) NOT NULL,
    margin_percentage NUMERIC(5, 2) NOT NULL
);
