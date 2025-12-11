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

## Validations
| Field | Validation |
|-------|------------|
| url | Cannot be empty |
| url | Cannot exceed 2048 characters |
| short_code | Cannot be empty |
| short_code | Cannot exceed 10 characters |

### Invalid URL
```bash
curl -X POST http://localhost:5000/api/urls -H "Content-Type: application/json"
``` -d '{"url": "not-a-url"}'

### Invalid short code
```bash
curl http://localhost:5000/api/urls/abc!@#
```

## Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/urls | Create a short code for the url |
| GET | /api/urls/<short_code> | Get the details of a short code |
| GET | /<short_code> | Launch the url referred by the short code |
| GET | /metrics | Get the collision metrics | 

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
	"clicks":0,"created_at":"2025-12-10T18:50:28.253664",
	"original_url":"http://localexample.com",
	"short_code":"5i6"
}
```

**Redirect URL:**

```bash
curl http://localhost:5000/<short_code>
```

**Get Metrics:**
```bash
curl http://localhost:5000/metrics
```
Expected Output:
```json
{"collision_rate":0.0,"total_collisions":0,"total_creates":7}
```

## Teardown Application
```bash
docker compose down -v
```

## Load Testing
```bash
docker compose -f docker-compose.loadtest.yml up --build
http://localhost:8089
```

## Database Migrations

### Initial Setup
```bash
alembic init alembic
```
Creates `alembic.ini` and `alembic/` folder.

### Generate Migration
```bash
alembic revision --autogenerate -m "description"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback
```bash
alembic downgrade -1
```

MIT

## License
