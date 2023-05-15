# misw4204-grupo17-converter

## Local Setup
This project is able to run in a local environment following the next steps.


```bash
  pyenv install 3.9
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
```
## Cloud Setup


## Running performance tests

1. Install k6 bin, https://k6.io/docs/get-started/installation/
2. set up local env, python, pg, redis. docker-compose up
3. run the tests locally

```
  docker-compose up influxdb grafana
  k6 run --out influxdb=http://localhost:8086/k6 ./performance/performance-test.js
```

#### Note: k6 test are able to run on clod or in a distributed environment, for this scenario we are just using local execution.
