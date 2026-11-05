# Project 01 — SLO-Driven Microservice Reliability

Build and operate a small HTTP service with Prometheus instrumentation, Grafana dashboards, alert rules, automated tests and repeatable failure exercises. This project demonstrates practical SRE thinking—not simply installing monitoring tools.

## Architecture

```mermaid
flowchart LR
  U[User / load generator] --> A[FastAPI service]
  A --> M[/metrics endpoint]
  P[Prometheus] -->|scrapes| M
  P -->|PromQL datasource| G[Grafana]
  P --> R[Alert rules]
```

## Stack
Python 3.12, FastAPI, Prometheus client, Prometheus, Grafana, Docker Compose and pytest.

## Run locally
Prerequisites: Docker Engine and Docker Compose plugin.

```bash
docker compose up --build -d
docker compose ps
```

- App: http://localhost:8000
- Liveness: http://localhost:8000/health/live
- Readiness: http://localhost:8000/health/ready
- Metrics: http://localhost:8000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (`admin` / `change-me-locally`)

Keep these ports local. Change the demo Grafana password before any non-local exposure.

## Run tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

PowerShell activation: `.venv\Scripts\Activate.ps1`.

## Generate traffic

```bash
for i in {1..100}; do curl -s http://localhost:8000/work >/dev/null; done
for i in {1..100}; do curl -s -o /dev/null 'http://localhost:8000/work?fail=true'; done
for i in {1..30}; do curl -s -o /dev/null 'http://localhost:8000/work?delay_ms=800'; done
```

Read `docs/slo-and-alerting.md` and follow `docs/failure-exercise.md`. Complete the incident report template using actual observations.

## Known limitations and next improvements
- Metrics are in-memory; don't scale horizontally without choosing an aggregation strategy.
- Alert rules are starter examples, not full multi-window/multi-burn-rate SLO alerts.
- The `fail=true` parameter is a test hook, not a production failure mechanism.
- Add CI, container scanning, load testing and deployment automation as later milestones.
- Validate alert behavior and dashboard queries in your own environment before describing them as working.

## Interview questions
1. Why are liveness and readiness different?
2. What is the difference between SLI, SLO and SLA?
3. Why can a 99.9% SLO be inappropriate for some services?
4. Why alert on error-budget burn rather than every individual 500?
5. What are Prometheus label-cardinality risks?
6. What happens to in-memory metrics when the process restarts?
7. How would you test an alert before relying on it?
8. What would you do if Grafana were unavailable but the service remained healthy?
