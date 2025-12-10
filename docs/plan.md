# URL Shortener Project Plan

## Project Goal
Build a production-grade URL shortener that teaches distributed systems concepts.

---

## Version 0.1 — Core Functionality + Baseline Metrics

Single sync worker, establish baseline before scaling.

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Architecture docs, diagrams, plan.md | In Progress |
| 1 | Docker + health check API (1 Gunicorn worker) | Not Started |
| 2 | Models + DB setup with `create_all()` | Not Started |
| 3 | Create URL API (short code generation, collision tracking) | Not Started |
| 4 | Read + redirect API | Not Started |
| 5 | Click tracking API | Not Started |
| 6 | Validations | Not Started |
| 7 | Load testing, baseline metrics, document single-worker limits | Not Started |

**Outcome:** Documented proof that single sync worker saturates at X RPS.
