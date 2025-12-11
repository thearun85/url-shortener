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
| 5 | Click tracking API | Completed |
| 6 | Validations | Completed |
| 7 | Create URL API - Collision tracking | Completed |
| 8 | Load testing, baseline metrics, document single-worker limits with locust | Completed |

**Outcome:** Documented proof that single sync worker sustains ~34 RPS with 4ms median latency, but 68-second tail latency under pressure due to request queuing.

## Version 0.2 — Observability + Multi-Worker

Add visibility before optimization.

| Phase | Description | Status |
|-------|-------------|--------|
| 0a | Alembic migrations setup | Completed |
| 0b | Changes to run migrations via shell script | Completed |
| 1 | Multiple Gunicorn workers load testing with baseline results | Not Started |
| 2 | Prometheus metrics integration | Completed |
| 3 | Grafana dashboard | On Hold |

**Outcome:** 
- Alembic migrations enable safe multi-worker deployments
- Load testing showed 4 workers = +18% RPS under 100 users, but no improvement at 20 users
- Persistent 68s tail latency confirms database I/O bottleneck (not CPU)
- Prometheus tracks creates, collisions, redirects
- Next optimization: caching to reduce database pressure
