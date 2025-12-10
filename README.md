# url-shortener

A production-grade URL shortener built to learn and demonstrate distributed systems concepts.

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
curl http://localhost:5000
```

## Verify Database is created
```bash
docker compose exec db psql -U postgres -d urlshortener -c '\dt'
```

## Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/urls | Create a short code for the url |

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

## Teardown Application
```bash
docker compose down -v
```

MIT

## License
