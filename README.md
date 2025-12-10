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
docker compose exec psql -U postgres -d urlshortener -c '\dt'
```

## Teardown Application
```bash
docker compose down -v
```
## License

MIT
