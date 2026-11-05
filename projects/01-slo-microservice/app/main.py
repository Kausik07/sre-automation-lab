from fastapi import FastAPI, Response, status
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
import asyncio
import time

app = FastAPI(title="SRE Demo Service", version="1.0.0")
REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "http_status"])
LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["method", "endpoint"],
                    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5))

@app.middleware("http")
async def observe_requests(request, call_next):
    started = time.perf_counter()
    code = 500
    try:
        response = await call_next(request)
        code = response.status_code
        return response
    finally:
        if request.url.path != "/metrics":
            REQUESTS.labels(request.method, request.url.path, str(code)).inc()
            LATENCY.labels(request.method, request.url.path).observe(time.perf_counter() - started)

@app.get("/")
async def root():
    return {"service": "sre-demo-service", "status": "ok"}

@app.get("/health/live")
async def liveness():
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness():
    return {"status": "ready"}

@app.get("/work")
async def work(delay_ms: int = 0, fail: bool = False):
    delay = min(max(delay_ms, 0), 3000) / 1000
    if delay:
        await asyncio.sleep(delay)
    if fail:
        return Response('{"error":"simulated failure"}', status_code=503, media_type="application/json")
    return {"result": "completed", "delay_ms": int(delay * 1000)}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)
