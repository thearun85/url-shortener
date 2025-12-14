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

## Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Check the status of URL shortener |

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

## Teardown Application
```bash
docker compose down -v
```
