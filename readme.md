# MarketWatch Project

## Need more info

- Stock_values sould be persisted and retrieved only for request_data dates? Or must be filled for all dates?
- What's status and purchased_status for?
- MarketWatch has robot restriction and IP blocks. There is another source for desired information or interface to retreive data?

## TODO:

- [x] Create Project
- [x] Install Framework
- [x] Start application
- [x] Create dockerfile for application, should serve on port 8000
- [x] Create new endpoint to retrieve data `[GET] /stock/{stock_symbol}:`
- [x] Create infra for Polygon.io
- [x] Retreive data from Polygon.io
- [x] Parse data and make response
- [x] Create new endpoint to register operations `[POST] /stock/{stock_symbol}`
- [x] Parse data and compose response
- [x] Create docker compose for database (PostgresDB)
- [x] Install DB deps
- [x] Create DB connection
- [x] Create DB entities for stock data
- [x] Create infra for MarketWatch
- [x] Persist data for stocks and their purchased amounts
- [x] Retrieve Performance and Competitors data from MarketWatch
- [x] Compose response and fill all Expected Json Response
- [ ] Implement logs for application
- [ ] Improve docker-compose with cache
- [ ] Implement caching per stock mechanism on the GET

## Domain

### Stock

### Stock-timeseries

- stock_id: String
- open: Float
- high: Float
- low: Float
- close: Float
- date: unix timestamp

### Market_cap

- Currency: String
- Value: Float
- date: unix timestamp

### Stock-Operations

- stock_id: string
- operation_date: Datetime
- purchased_amount: Integer
- purchased_status: String
- date: unix timestamp

### Stock-performance

- five_days: Float
- one_month: Float
- three_months: Float
- year_to_date: Float
- one_year: Float
- date: unix timestamp

### Stock-Domain

- stock_id: String
- company_code: String
- company_name: String
- request_data: Date (YYYY-MM-DD)
- Stock_values: stock-timeseries[]
- performance_data: Stock-performance for request_data
- market_cap: Market_cap for request_data

## Expected Json Response

- status: String
- purchased_amount: Integer
- purchased_status: String
- request_data: Date (YYYY-MM-DD)
- company_code: String
- company_name: String
- Stock_values: Object
  - open: Float
  - high: Float
  - low: Float
  - close: Float
- performance_data: Object
  - five_days: Float
  - one_month: Float
  - three_months: Float
  - year_to_date: Float
  - one_year: Float
- Competitors: Array[Object]
  - name: String
- market_cap: Object
  - Currency: String
  - Value: Float
