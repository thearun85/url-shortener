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
- [results](docs/benchmarks.md#Phase-0-sync-baseline)

## Version 0.2 — Observability + Multi-Worker

Add visibility before optimization.

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Alembic migrations setup | Yet to Start |
| 1 | Multiple Gunicorn workers load testing with baseline results | Yet to Start |
| 2 | Prometheus metrics integration | Yet to Start |
| 3 | Fix for collision during short code generation | Yet to Start |
