-- create_tables.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS stock (
    id VARCHAR NOT NULL PRIMARY KEY,
    company_code VARCHAR NOT NULL,
    company_name VARCHAR,
    request_data VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS stock_timeseries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id VARCHAR NOT NULL,
    open FLOAT NOT NULL,
    high FLOAT NOT NULL,
    low FLOAT NOT NULL,
    close FLOAT NOT NULL,
    date VARCHAR NOT NULL,
    FOREIGN KEY(stock_id) REFERENCES stock(id)
);

CREATE TABLE IF NOT EXISTS market_cap (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id VARCHAR NOT NULL,
    currency VARCHAR NOT NULL,
    value FLOAT NOT NULL,
    date VARCHAR NOT NULL,
    FOREIGN KEY(stock_id) REFERENCES stock(id)
);

CREATE TABLE IF NOT EXISTS stock_performance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id VARCHAR NOT NULL,
    five_days FLOAT NOT NULL,
    one_month FLOAT NOT NULL,
    three_months FLOAT NOT NULL,
    year_to_date FLOAT NOT NULL,
    one_year FLOAT NOT NULL,
    date VARCHAR NOT NULL,
    FOREIGN KEY(stock_id) REFERENCES stock(id)
);

CREATE TABLE IF NOT EXISTS stock_operation (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id VARCHAR NOT NULL,
    operation_date VARCHAR NOT NULL,
    purchased_amount FLOAT NOT NULL,
    purchased_status VARCHAR NOT NULL,
    FOREIGN KEY(stock_id) REFERENCES stock(id)
);

CREATE TABLE IF NOT EXISTS competitor (
    id SERIAL PRIMARY KEY,
    stock_id VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    FOREIGN KEY(stock_id) REFERENCES stock(id)
);
