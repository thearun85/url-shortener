# V0.3 Sync Baseline Summary

**Date:** 2025-12-12  
**Tool:** hey (replaced Locust)  
**Duration:** 10s per test  

---

## Key Finding: Checkpoint-Induced Latency Spikes

Results show **unpredictable 19-second stalls** caused by PostgreSQL checkpoint I/O during write-heavy operations. Performance varies wildly depending on when checkpoints occur.

Example from same test run:
- Redirect c=1: **111 RPS**, 1.9ms avg ✓
- Redirect c=10: **1.8 RPS**, 12ms avg ❌ (hit checkpoint)

This inconsistency is the core problem V0.3 async writes will solve.

---

## Redirect Test (GET /<short_code>)

Each redirect does: SELECT (lookup URL) + INSERT (click tracking)

### 1 Worker

| Concurrency | Avg | P50 | P95 | P99 | RPS | Responses |
|-------------|-----|-----|-----|-----|-----|-----------|
| 1 | 1.9ms | 1.8ms | 2.3ms | 4.1ms | 111 | 2840 |
| 10 | 12ms | 10ms | 26ms | — | 1.8 | 27 |
| 50 | 4.67s | 37ms | 19.6s | 19.6s | 10.7 | 210 |
| 100 | 157ms | 72ms | 131ms | 1.16s | 114 | 2605 |

### 4 Workers

| Concurrency | Avg | P50 | P95 | P99 | RPS | Responses |
|-------------|-----|-----|-----|-----|-----|-----------|
| 1 | 19.6ms | 1.9ms | 2.4ms | 5.3ms | 51 | 1099 |
| 10 | 6.9ms | 5.7ms | 15.6ms | — | 2.6 | 43 |
| 50 | 4.39s | 22ms | 19.7s | 19.8s | 10 | 196 |
| 100 | 98ms | 39ms | 95ms | 124ms | 149 | 3259 |

**Observation:** 4 workers helps at c=100 (149 vs 114 RPS), but checkpoint stalls still dominate.

---

## Create URL Test (POST /api/urls)

Each create does: INSERT (new URL)

### 1 Worker

| Concurrency | Avg | P50 | P95 | P99 | RPS | Responses |
|-------------|-----|-----|-----|-----|-----|-----------|
| 1 | 6.9ms | — | — | — | 0.15 | 2 |
| 10 | 735ms | 8.2ms | 19.6s | — | 3.1 | 54 |
| 50 | 67ms | 60ms | 69ms | 72ms | 135 | 3224 |
| 100 | 60ms | 62ms | 112ms | 132ms | 22.8 | 367 |

### 4 Workers

| Concurrency | Avg | P50 | P95 | P99 | RPS | Responses |
|-------------|-----|-----|-----|-----|-----|-----------|
| 1 | 8.2ms | — | — | — | 0.1 | 1 |
| 10 | 3.02s | 5.3ms | 19.6s | — | 3.3 | 65 |
| 50 | 25ms | 24ms | 34ms | 37ms | 131 | 2819 |
| 100 | 193ms | 27ms | 59ms | 82ms | 45 | 835 |

**Observation:** Create at low concurrency (c=1, c=10) consistently hits checkpoint stalls.

---

## Health Check Test (GET /health)

No database operations — should be fast.

| Workers | Avg | P50 | P95 | P99 | RPS |
|---------|-----|-----|-----|-----|-----|
| 1 | 4.81s | 13ms | 19.4s | 19.4s | 18 |
| 4 | 3.91s | 12ms | 19.4s | 19.8s | 25 |

**Observation:** Even health checks stall when workers are blocked on DB writes. P50 is 12-13ms (good), but P95+ hits 19s (blocked behind writes).

---

## Analysis

### Why 19 seconds?

PostgreSQL default `checkpoint_timeout` is 5 minutes, but checkpoints can trigger earlier based on WAL volume. The ~19-20s stalls suggest checkpoint I/O blocking the single DB connection.

### Why inconsistent results?

Tests that start right after a checkpoint completes run fast. Tests that trigger or wait for a checkpoint stall badly. With continuous load testing, we're constantly writing and triggering checkpoints.

### Why doesn't 4 workers help much?

Workers share the same database. When PostgreSQL checkpoints, ALL workers block on DB I/O. More workers = more parallelism for CPU, but doesn't solve I/O bottleneck.

---
