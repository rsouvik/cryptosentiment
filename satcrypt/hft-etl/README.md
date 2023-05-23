# hft-etl
This repo contains:
- the Docker Compose file to run local, pre-configured instances of InfluxDB and Grafana
- an implementation for collecting historical pricing data from CryptoCompare and writing to InfluxDB

### Getting Started
- in the root of the project, run `docker build -t hft-etl .` 
- then, run `docker-compose up -d` to bring up InfluxDB, Grafana, and the collection job(s)
    - collection will run at a 60 minute interval, pulling the last 60 minutes of OHLCV data for cryptocurrencies defined in `src/coins.json`

### Sources
Classes that subclass the `Source` class are responsible for making requests to an external endpoint and parsing the response.

Each subclass of `Source` should implement a `fetch_all` method the yields OHLCV records.

#### `Source` Parent Class
This parent class contains the follwing helper methods:
- `fetch`: makes a GET request to the specified endpoint
    - params:
        - endpoint: string
        - headers: Dict
    - response:
        - requests.Response

### Config
Classes that subclass `Config` are responsible for passing the path to a specific configuration file to the parent class and defining relevant properties.

### Known Deficits/Shortcomings
- The interval between collection runs is only configurable with a code change as are the minutes of history
- InfluxDB token is static, not generated and disseminated
- Lack of retries on failed requests