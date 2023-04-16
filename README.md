# misw4204-grupo17-converter



## Running performance tests

1. Install k6 bin, https://k6.io/docs/get-started/installation/
2. set up local env, python, pg, redis.
3. run the tests locally

```
  k6 run ./performance/performance-test.js
```

#### Note: k6 test are able to run on clod or in a distributed environment, for this scenario we are just using local execution.