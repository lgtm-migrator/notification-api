# Comparing api lambda vs k8s

First set the environment variable
```
export TEST_AUTH_HEADER="ApiKey-v1 XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
```

## k8s

master:
```
locust --config=tests-perf/api_lambda_vs_k8s/locust-api-k8s.conf
```

3 workers:
```
locust -f tests-perf/api_lambda_vs_k8s/locust-api-lambda.py --worker
```

## lambda

master:
```
locust --config=tests-perf/api_lambda_vs_k8s/locust-api-lambda.conf
```

3 workers:
```
locust -f tests-perf/api_lambda_vs_k8s/locust-api-lambda.py --worker
```
