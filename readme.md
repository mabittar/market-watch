# MarketWatch Project

## Need more info

- Stock_values sould be persisted and retrieved only for request_data dates? Or must be filled for all dates?
- What's status and purchased_status for?

## TODO:

- [ ] Create Project
- [ ] Install Framework
- [ ] Start application
- [ ] Create dockerfile for application, should serve on port 8000
- [ ] Create new endpoint to retrieve data `[GET] /stock/{stock_symbol}:`
- [ ] Create infra for Polygon.io
- [ ] Retreive data from Polygon.io
- [ ] Parse data and make response
- [ ] Create docker compose for database (PostgresDB)
- [ ] Install DB deps
- [ ] Create DB connection
- [ ] Create DB entities for stock data
- [ ] Request from endpoint, persist data and make responses
- [ ] Create infra for MarketWatch
- [ ] Retrieve Performance and Competitors data from MarketWatch
- [ ] Parse data and compose response
- [ ] Create new endpoint to register operations `[POST] /stock/{stock_symbol}`
- [ ] Create docker compose for database (PostgresDB)
- [ ] Install DB deps
- [ ] Create DB connection
- [ ] Create DB entities for stock data
- [ ] Persist data for stocks and their purchased amounts
- [ ] Compose response and fill all Expected Json Response
- [ ] Improve docker-compose with cache
- [ ] Implement caching per stock mechanism on the GET
- [ ] Implement logs for application


## Domain

### Stock

### Stock-timeseries

- stock_id: String
- date: unix timestamp
- open: Float
- high: Float
- low: Float
- close: Float

### Market_cap

- Currency: String
- Value: Float

### Stock-Operations

- stock_id: string
- operation_date: Datetime
- purchased_amount: Integer
- purchased_status: String

### Stock-performance

- five_days: Float
- one_month: Float
- three_months: Float
- year_to_date: Float
- one_year: Float

### Stock-Domain

- stock_id: String
- company_code: String
- company_name: String
- Stock_values: stock-timeseries[]
- performance_data: Stock-performance[]
- market_cap: Market_cap

## Expected Json Response

- Status: String
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
