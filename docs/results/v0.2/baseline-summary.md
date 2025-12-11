# Version 0.2 Load Test Baseline

**Date:** 2025-12-11  
**Environment:** MacBook Air (8 cores), Docker, PostgreSQL  
**Tool:** Locust  
**Duration:** 3 minutes per test  
**Spawn Rate:** 10 users/second

## Test Matrix

| Test | Workers | Users | Report |
|------|---------|-------|--------|
| A | 1 | 20 | [1-worker-20-users-report.html](./1-worker-20-users-report.html) |
| B | 4 | 20 | [4-worker-20-users-report.html](./4-worker-20-users-report.html) |
| C | 1 | 100 | [1-worker-100-users-report.html](./1-worker-100-users-report.html) |
| D | 4 | 100 | [4-worker-100-users-report.html](./4-worker-100-users-report.html) |

---

## Results: 20 Users

| Metric | 1 Worker | 4 Workers | Diff |
|--------|----------|-----------|------|
| Total Requests | 5,542 | 4,408 | -20% |
| RPS | **37.4** | 30.2 | -19% |
| Avg Response | 497ms | 622ms | +25% |
| P50 | 4ms | 3ms | — |
| P95 | 9ms | 7ms | — |
| P99 | 34ms | 35ms | — |
| Max | 68,380ms | 68,386ms | — |

**Finding:** 1 worker outperformed 4 workers with low load. Multi-process overhead (memory, context switching) exceeded the benefit when there wasn't enough concurrent demand.

---

## Results: 100 Users

| Metric | 1 Worker | 4 Workers | Diff |
|--------|----------|-----------|------|
| Total Requests | 9,260 | 10,466 | +13% |
| RPS | 60.4 | **71.5** | +18% |
| Avg Response | 1,496ms | 1,316ms | -12% |
| P50 | 10ms | 12ms | — |
| P95 | 85ms | **39ms** | -54% |
| P99 | 68,000ms | 68,000ms | — |
| Max | 68,479ms | 68,416ms | — |

**Finding:** 4 workers clearly wins under higher load. 18% throughput improvement and P95 latency cut in half.

---

## Key Insights

### 1. Worker Scaling Requires Sufficient Load
Adding workers without sufficient concurrent load creates overhead without benefit. The crossover point is somewhere between 20-100 users for this application.

### 2. Persistent 68-Second Tail Latency
All tests showed ~68 second maximum response times regardless of worker count. This indicates a systemic bottleneck unrelated to application-layer parallelism.

**Problem:** Max latency of ~68 seconds in 3-minute tests, absent in 1-minute tests.

**Root Cause:** PostgreSQL checkpoint I/O

**Evidence from logs:**
```
checkpoint starting: time
checkpoint complete: write=20.686 s, total=20.701 s
```

**Timeline:**
| Time | RPS | P95 | Event |
|------|-----|-----|-------|
| 0:00 - 1:30 | 483 | 15-47ms | Healthy |
| 1:30 | 162 | 68ms | Checkpoint starts |
| 1:35 | 162 | 68,000ms | Queue backup |
| 2:00+ | 107 | — | Slow recovery |

**Explanation:** Checkpoint I/O blocks queries for ~20s. Requests queue up, and cumulative wait reaches 68s for tail requests.

**Mitigation (v0.3):** Redis caching to reduce DB write pressure, checkpoint tuning.

### 3. P95 vs P99 Gap
| Users | P95 | P99 |
|-------|-----|-----|
| 20 (1w) | 9ms | 34ms |
| 100 (1w) | 85ms | 68,000ms |
| 100 (4w) | 39ms | 68,000ms |

The jump from P95 to P99 at 100 users suggests a small percentage of requests hit the blocking bottleneck while most complete quickly.

---

## Conclusions

1. **Horizontal scaling works** — but only under sufficient load
2. **Bottleneck is not CPU** — adding workers helped throughput but didn't eliminate tail latency
3. **Next optimization target:** Database I/O (caching, connection pooling, read replicas)

---

## Next Steps (Version 0.3+)

1. **Redis caching** — Reduce database reads for redirect lookups
2. **Connection pooling tuning** — Optimize SQLAlchemy pool settings
3. **Investigate 68s timeout** — Profile to identify root cause
4. **Re-test after caching** — Compare before/after metrics
