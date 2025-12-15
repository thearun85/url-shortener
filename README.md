# url-shortener
A production grade URL Shortener built to learn and demonstrate distributed system design concepts.

## Why This Project?

Not another tutorial URL shortener. This project deliberately exposes bottlenecks, measures them , then fixes them - with proof at every step.

**The approach:**

1. Start with intentional constraints (single worker, 3-char short codes)
2. Load test to demonstrate limits
3. Add infrastructure (caching, scaling, queues) with visible before/ after metrics
4. Document decisions and tradeoffs

## Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| Framework | Flask | Sync-first exposes bottlenecks |
| ORM | Plain SQLAlchemy | Explicit session handling |
| Database | PostgreSQL | Production standard |
| Server | Gunicorn (sync) | Worker scaling visible |
| Container | Docker + Compose | Reproducible |


## Running Locally
```bash
docker compose up --build
curl http://localhost:5000
```

## Validations
| Field | Validation |
|-------|------------|
| url | Cannot be empty |
| url | Cannot exceed 2048 characters |
| url | Valid Email format |
| short_code | Cannot be empty |
| short_code | Cannot exceed 10 characters |


## Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Check the status of URL shortener |
| POST | /api/urls | Create a short code for the url |
| GET | /api/urls/<short_code> | Get the details of a short code |
| GET | /<short_code> | Launch the url referred by the short code |

**Health check API:**

```bash
curl http://localhost:5000/health
```
Expected Output:
```json
{
	"status":"healthy"
}
```

**Create Shortcode:**
```bash
curl -X POST http://localhost:5000/api/urls \
-H "Content-Type: application/json" \
-d '{"url":"http://localexample.com"}'
```
Expected Output:
```json
{
	"created_at":"2025-12-10T18:09:27.742641",
	"original_url":"http://localexample.com",
	"short_code":"btj"
}
```

**Get Shortcode Details:**

```bash
curl http://localhost:5000/api/urls/<short_code>
```
Expected Output:
```json
{
	"clicks":0,
	"created_at":"2025-12-10T18:50:28.253664",
	"original_url":"http://localexample.com",
	"short_code":"5i6",
}
```

**Redirect URL:**

```bash
curl http://localhost:5000/<short_code>
```

## Connect to Database
```bash
docker compose exec db psql -U postgres -d urlshortener
```

## Connect to Redis
```bash
docker compose exec redis redis-cli ping
```

## Teardown Application
```bash
docker compose down -v
```

## Running Locust
```bash
docker compose -f docker-compose.loadtest.yml run --rm loadtest -f /loadtests/locustfile.py --headless -u 100 -r 10 -t 60s --csv=/results/v0.2/test
```

## Running Prometheus
### http://localhost:9090/
## Performance
- v0.1  (Sync with 1 worker): ~400 req/s baseline
- v0.2 (Sync with 4 workers): ~400 req/s ceiling, latency improved by 45%
- v0.3 (Async writes): ~400 req/s, P99 reduced to 51ms (35% improvement)
- v0.4 (Redis Read Cache): No improvement — equivalent network latency with co-located Postgres
- v0.5 (Gevent workers): ~1,700 req/s (4x throughput), ceiling at ~1,500 req/s under heavy load with graceful degradation


See [benchmarks](docs/benchmarks.md) for detailed results.
