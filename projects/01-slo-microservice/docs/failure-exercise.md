# Failure exercise: elevated errors and latency

1. Start the stack: `docker compose up --build -d`.
2. Confirm Prometheus target is healthy at http://localhost:9090/targets.
3. Open Grafana at http://localhost:3000 (local lab login: admin / change-me-locally).
4. Generate normal traffic:
   `for i in {1..100}; do curl -s http://localhost:8000/work >/dev/null; done`
5. Inject HTTP 503 responses:
   `for i in {1..100}; do curl -s -o /dev/null 'http://localhost:8000/work?fail=true'; done`
6. Inject latency:
   `for i in {1..30}; do curl -s -o /dev/null 'http://localhost:8000/work?delay_ms=800'; done`
7. Observe request rate, 5xx ratio, p95 latency and alert state. Allow several scrape/evaluation intervals.
8. Stop injecting failures and confirm recovery.

Record timestamps, detection delay, alert firing/recovery, evidence, mitigation, root-cause hypothesis and follow-up actions. Never claim an alert fired or a recovery time was achieved unless you observed it.
