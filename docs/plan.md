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
| 1 | Multiple Gunicorn workers | Not Started |
| 2 | Prometheus metrics integration | Not Started |
| 3 | Grafana dashboard | Not Started |

**Outcome:** Live dashboard showing multi-worker performance, baseline for Version 0.3 optimizations.
