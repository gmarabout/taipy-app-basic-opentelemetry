# Taipy and OpenTelemetry

[![tests](https://github.com/gmarabout/taipy-app-basic-opentelemetry/actions/workflows/pylint.yml/badge.svg)](https://github.com/gmarabout/taipy-app-basic-opentelemetry/actions/workflows/tests.yml)

---

This project shows how to monitor a simple Taipy app with OpenTelemetry.
It uses:

- [Prometheus](https://prometheus.io/docs/introduction/overview/) to store and query metrics, including one custom metric
- [Jaeger](https://jaegertracing.io/) to store and query traces
- [Loki](https://grafana.com/docs/loki/latest/) to store logs
- [Grafana](https://grafana.com/grafana/) to query logs

## Installation

Clone the project on your computer: `git clone https://github.com/gmarabout/taipy-app-basic-opentelemetry.git`.

## Usage

The project uses Docker Compose to run the Taipy app and all the monitoring services.

To run all the services, enter `docker compose up` in a terminal.

- Click [here](http://localhost:5000) to run the **Taipy app** (which is a simple multiplier).
- Click [here](http://localhost:3000) to open **Grafana**.
- Click [here](http://localhost:16686/) to open **Jaeger**.
- Click [here](http://localhost:9090/) to open **Prometheus**.
