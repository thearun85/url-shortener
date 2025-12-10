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
| 6 | Validations | Not Started |
| 7 | Create URL API - Collision tracking | Not Started |
| 8 | Load testing, baseline metrics, document single-worker limits | Not Started |

**Outcome:** Documented proof that single sync worker saturates at X RPS.
