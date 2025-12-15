# URL Shortener Project Plan

## Project Goal
Build a production-grade URL shortener that teaches distributed systems concepts.

---

## Version 0.1 — Core Functionality + Baseline Metrics

Single sync worker, establish baseline before scaling.

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Architecture and flow diagrams, plan.md | Completed |
| 1 | Docker + health check API (1 Gunicorn worker) | Completed |
| 2 | Models + DB setup with `create_all()` | Completed |
| 3 | Create URL API - short code generation | Completed |
| 4 | Read + redirect API | Completed |
| 5 | Click tracking | Completed |
| 6 | Validations | Completed |
| 7 | Create URL API - Collision tracking | Moved to Phase 1 |
| 8 | Load testing,  document single-worker limits with locust | Completed |

**Outcome:** Sync baseline established: Gunicorn server with 1 worker and synchronous Postgres operations achieves ~400 req/s maximum throughput with latency degradation (3x median, 5x P99). This ceiling represents the blocking I/O bottleneck to be addressed in subsequent phases.

**Proofs:**
- [results](docs/benchmarks.md#sync-baseline)

## Version 0.2 — Observability + Multi-Worker

Add visibility before optimization.

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Alembic migrations setup | Completed |
| 1 | Fix for collision during short code generation | Completed |
| 2 | Multiple Gunicorn workers load testing with baseline results | Completed |
| 3 | Prometheus metrics integration | Completed |

**Outcome:** ~400 req/s, 4 workers improved latency by ~45% but didn't break throughput ceiling) — [results](docs/benchmarks.md#sync-baseline
- Next optimization: caching to reduce database pressure

**Proofs:**
- [results](docs/benchmarks.md#sync-baseline)

## Version 0.3 — Async Writes for Click table

Reduce the db pressure by moving the click inserts initiated during redirects to a redis queue.
 
| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Redis queue for click events (push instead of insert) | Completed |
| 1 | Background worker for batch Click inserts | Completed |
| 3 | Load test with baseline results | Not Started |

**Outcome:** Async writes (~400 req/s maintained, P99 reduced by 35% to 51ms at 200 users, latency improved across all load levels) — 

**Proofs:**
- [results](docs/benchmarks.md#async-writes)
