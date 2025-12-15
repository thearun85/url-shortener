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
| 2 | Load test with baseline results | Not Started |

**Outcome:** Async writes (~400 req/s maintained, P99 reduced by 35% to 51ms at 200 users, latency improved across all load levels) — 

**Proofs:**
- [results](docs/benchmarks.md#async-writes)

## Version 0.4 — Redis cache for redirects

Overcome the I/O bottleneck resulting in throughput ceiling of ~400 RPS by implementing Redis cache.
 
| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Redis cache changes for redirects | Completed |
| 1 | Cache hit ratio metrics for prometheus | Completed |
| 2 | Load test comparison | Completed |

**Outcome:** Redis read cache (no improvement — Redis and Postgres co-located in Docker have equivalent network latency, indexed lookups already fast) — 

**Proofs:**
[results](docs/benchmarks.md#Redis Read Cache (v0.4))

## Version 0.5 — Overcome the throughput ceiling

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Increase the SQLAlchemy poolsize | Completed |
| 1 | Increase the number of sync workers to 8 | Completed |
| 2 | Use asynchronous processing in gunicorn with gevent | Completed |

**Observations:Phase 0** The pool isn't saturated because Gunicorn workers are the bottleneck, not DB connections. With sync workers, each can only handle 1 request at a time:
 
**Observations:Phase 1** Throughput stayed constant while latency degraded significantly. Signs of CPU contention, Docker resource limits or Context switching overhead.


**Outcome:** Gevent workers (**4x throughput breakthrough** — ~1,676 req/s, broke the sync I/O ceiling)

**Proofs:**  
[results](docs/benchmarks.md#gevent-workers)
