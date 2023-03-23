# python_flask_prometheus_poc

Example python flask application and dummy load generator to test  prometheus metrics from flask

This project aims to test Prometheus generated metrics from a Flask application. Ideally you would deploy this application using Docker or in a Kubernetes cluster.

A Docker image is already available from Docker Hub:

```shell
docker pull nicc777/python_flask_prometheus_poc
```

Docker quick start:

```shell
docker run -p 8082:8080 --name pyprom --rm nicc777/python_flask_prometheus_poc:latest
```

And then start Locust and run a simple test using the provided `locustfile.py` file.

