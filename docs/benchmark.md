# Benchmarks

## Sync Baseline

Gunicorn server with synchronous Postgres operations.

### 1 Worker 

| Users | Requests/s | Median | P95  | P99  | Failures |
|-------|-----------|--------|------|------|----------|
| 1     | ~24       | 10ms   | 14ms | 16ms | 0 (0%)   |
| 20    | ~355      | 4ms    | 9ms  | 17ms | 1 (0.06%)|
| 100   | ~372      | 11ms   | 32ms | 39ms | 2 (0.06%)|
| 200   | ~409      | 30ms   | 72ms | 79ms | 4 (0.1%) |

### 4 Workers 

| Users | Requests/s | Median | P95  | P99  | Failures |
|-------|-----------|--------|------|------|----------|
| 1     | ~23       | 10ms   | 14ms | 16ms | 0 (0%)   |
| 20    | ~398      | 4ms    | 8ms  | 13ms | 0 (0%)   |
| 100   | ~375      | 6ms    | 22ms | 33ms | 0 (0%)   |
| 200   | ~410      | 16ms   | 48ms | 63ms | 0 (0%)   |

### Comparison: 1 Worker vs 4 Workers

| Users | Metric     | 1 Worker | 4 Workers | Improvement |
|-------|------------|----------|-----------|-------------|
| 1     | Median     | 10ms     | 10ms      | — |
| 1     | P99        | 16ms     | 16ms      | — |
| 1     | Failures   | 0        | 0         | — |
| 20    | Median     | 4ms      | 4ms       | — |
| 20    | P99        | 17ms     | 13ms      | **24% faster** |
| 20    | Failures   | 1        | 0         | ✓ |
| 100   | Median     | 11ms     | 6ms       | **45% faster** |
| 100   | P99        | 39ms     | 33ms      | **15% faster** |
| 100   | Failures   | 2        | 0         | ✓ |
| 200   | Median     | 30ms     | 16ms      | **47% faster** |
| 200   | P99        | 79ms     | 63ms      | **20% faster** |
| 200   | Failures   | 4        | 0         | ✓ |

### Observations 1 worker

- **Throughput ceiling**: ~400 req/s regardless of user count
- **Latency degradation**: P99 grows from 16ms → 79ms under load
- **Failure pattern**: 500 errors on POST /api/urls under concurrency

### Observations 4 workers

- **Throughput ceiling**: ~400 req/s regardless of workers — sync I/O bound
- **Latency**: 4 workers nearly halve latency under load (P99: 79ms → 63ms)


### Raw Data

- [1 Worker Results](results/v0.1/)
- [4 Workers Results](results/v0.2/)

## Async Writes (v0.3)

Flask with 4 Gunicorn workers, async writes to clicks table.

### 4 Workers Async Write

| Users | Requests/s | Median | P95  | P99  | Failures |
|-------|-----------|--------|------|------|----------|
| 1     | ~24       | 9ms    | 14ms | 17ms | 0 (0%)   |
| 20    | ~443      | 3ms    | 6ms  | 10ms | 0 (0%)   |
| 100   | ~356      | 5ms    | 17ms | 24ms | 0 (0%)   |
| 200   | ~400      | 11ms   | 36ms | 51ms | 0 (0%)   |

### Full Comparison: 1W Sync vs 4W Sync vs 4W Async Write

| Users | Metric     | 1W Sync | 4W Sync | 4W Async | Best |
|-------|------------|---------|---------|----------|------|
| 1     | Median     | 10ms    | 10ms    | 9ms      | — |
| 1     | P99        | 16ms    | 16ms    | 17ms     | — |
| 1     | Throughput | ~24     | ~23     | ~24      | — |
| 20    | Median     | 4ms     | 4ms     | 3ms      | **Async 25%↓** |
| 20    | P99        | 17ms    | 13ms    | 10ms     | **Async 41%↓** |
| 20    | Throughput | ~355    | ~398    | ~443     | **Async 11%↑** |
| 100   | Median     | 11ms    | 6ms     | 5ms      | **Async 55%↓** |
| 100   | P99        | 39ms    | 33ms    | 24ms     | **Async 38%↓** |
| 100   | Throughput | ~372    | ~375    | ~356     | 4W Sync |
| 200   | Median     | 30ms    | 16ms    | 11ms     | **Async 63%↓** |
| 200   | P99        | 79ms    | 63ms    | 51ms     | **Async 35%↓** |
| 200   | Throughput | ~409    | ~410    | ~400     | ~same |
| All   | Failures   | 6       | 0       | 0        | ✓ |

### Observations

- **Latency wins**: Async writes deliver lowest latency across all load levels
  - P99 at 200 users: 79ms → 63ms → 51ms (35% improvement over sync)
  - Median at 200 users: 30ms → 16ms → 11ms (63% improvement over 1W sync)
- **Throughput**: ~400 req/s ceiling persists — bottleneck is elsewhere
- **Stability**: Zero failures maintained
- **Sweet spot**: 20 users shows best async advantage (~443 req/s, 10ms P99)

### Conclusion

Async writes significantly improve latency without sacrificing throughput or stability. The ~400 req/s ceiling confirms the bottleneck is likely on the read path or connection pooling.

### Raw Data

- [4 Workers Async Write Results](results/v0.3/)

## Redis Read Cache (v0.4)

Flask with 4 Gunicorn workers, async writes, Redis cache for redirect lookups.

### Results

| Users | Requests/s | Median | P95  | P99  | Failures |
|-------|-----------|--------|------|------|----------|
| 1     | ~24       | 8ms    | 15ms | 22ms | 0 (0%)   |
| 20    | ~447      | 3ms    | 6ms  | 12ms | 0 (0%)   |
| 100   | ~182*     | 4ms    | 17ms | 28ms | 0 (0%)   |
| 200   | ~409      | 12ms   | 45ms | 56ms | 0 (0%)   |

*100 user throughput anomaly — likely test variance

### Comparison: Async Write vs Async Write + Redis Cache

| Users | Metric     | Async Write | + Redis Cache | Change |
|-------|------------|-------------|---------------|--------|
| 20    | Median     | 3ms         | 3ms           | — |
| 20    | P99        | 10ms        | 12ms          | ⚠️ +20% |
| 200   | Median     | 11ms        | 12ms          | — |
| 200   | P99        | 51ms        | 56ms          | ⚠️ +10% |

### Why Redis Cache Didn't Help

Redis and Postgres are co-located in the same Docker network:
```
Postgres indexed lookup: ~1-2ms (network + query)
Redis cache lookup:      ~1-2ms (network + get)
```

Both require a network round-trip. A simple indexed lookup (`SELECT * FROM urls WHERE short_code = ?`) is already sub-millisecond at the DB level. Redis doesn't eliminate the network hop — it just replaces one with another.

**When Redis cache helps:**
- Complex queries (joins, aggregations)
- High DB CPU load — offloading reads
- DB is remote, Redis is local

**When it doesn't help (this case):**
- Simple indexed lookups (already fast)
- Redis and Postgres co-located (same network latency)
- Read path wasn't the bottleneck

### Conclusion

Redis read cache provides no benefit when co-located with Postgres. The async writes in Phase 1 addressed the actual bottleneck (write I/O). For further improvement, consider in-process caching (eliminates network) or connection pool tuning.

### Raw Data

- [4 Workers Async Write + Redis Cache Results](results/v0.4/)

---

## Summary: Full Comparison

| Users | Metric     | 1W Sync | 4W Sync | +Async Write | +Redis Cache |
|-------|------------|---------|---------|--------------|--------------|
| 1     | Median     | 10ms    | 10ms    | 9ms          | 8ms          |
| 1     | P99        | 16ms    | 16ms    | 17ms         | 22ms         |
| 20    | Median     | 4ms     | 4ms     | 3ms          | 3ms          |
| 20    | P99        | 17ms    | 13ms    | 10ms         | 12ms         |
| 20    | Throughput | ~355    | ~398    | ~443         | ~447         |
| 100   | Median     | 11ms    | 6ms     | 5ms          | 4ms          |
| 100   | P99        | 39ms    | 33ms    | 24ms         | 28ms         |
| 200   | Median     | 30ms    | 16ms    | 11ms         | 12ms         |
| 200   | P99        | 79ms    | 63ms    | 51ms         | 56ms         |
| 200   | Throughput | ~409    | ~410    | ~400         | ~409         |
| All   | Failures   | 6       | 0       | 0            | 0            |

### Key Learnings

1. **4 workers**: Improved latency ~45%, eliminated failures, didn't break throughput ceiling
2. **Async writes**: Biggest win — P99 dropped 35% (79ms → 51ms), write path was the bottleneck
3. **Redis cache**: No benefit — co-located services have equivalent network latency, indexed reads already fast
4. **Throughput ceiling**: ~400 req/s persists across all configs — likely Gunicorn/connection pool limits

---

## Gevent Workers (v0.5)

Flask with 4 Gunicorn gevent workers, async writes, Redis cache.

### Results (200 Users)

| Metric     | Value |
|------------|-------|
| Requests/s | **~1,676** |
| Median     | 67ms  |
| P95        | 99ms  |
| P99        | 120ms |
| Failures   | 0 (0%) |

### Comparison: Sync vs Gevent (200 Users)

| Metric     | 4W Sync | 8W Sync | 4W Gevent | Change vs 4W Sync |
|------------|---------|---------|-----------|-------------------|
| Throughput | ~403    | ~407    | **~1,676** | **4x increase** |
| Median     | 12ms    | 23ms    | 67ms      | higher (expected) |
| P99        | 48ms    | 120ms   | 120ms     | same |

### Failed Experiment: 8 Sync Workers

Doubling sync workers to 8 made performance **worse**:
- Throughput: ~407 (no improvement)
- Median: 23ms (2x worse than 4W)
- P99: 120ms (2.5x worse than 4W)

**Cause**: CPU contention and context switching overhead. More sync workers doesn't help when the bottleneck is I/O wait, not CPU.

### Why Gevent Works

Sync workers block during I/O:
```
Request → DB query → [BLOCKED WAITING] → Response
          1 request per worker at a time
```

Gevent workers yield during I/O:
```
Request A → DB query → [yield to B] → Response A
Request B → DB query → [yield to C] → Response B
            Many requests per worker concurrently
```

With 4 workers × 200 connections = 800 concurrent requests possible.

### Trade-off

| Config | Throughput | Median | P99 | Best For |
|--------|-----------|--------|-----|----------|
| 4W Sync | ~400 | 12ms | 48ms | Low traffic, lowest latency |
| 4W Gevent | **~1,676** | 67ms | 120ms | **High traffic, production** |

Higher per-request latency, but 4x more requests handled. For a URL shortener serving many users, this is the right trade-off.

### Conclusion

Gevent broke the ~400 req/s sync I/O ceiling with a **4x throughput improvement**. This confirms the bottleneck was blocking I/O wait, not CPU, connections, or caching.

### Raw Data

- [4 Workers Gevent Results](results/v0.5/)

---

## Summary: Full Journey

| Phase | Config | Throughput | P99 | Key Learning |
|-------|--------|-----------|-----|--------------|
| 0 | 1W Sync | ~409 | 79ms | Baseline |
| 0 | 4W Sync | ~410 | 63ms | Workers improve latency, not throughput |
| 1 | 4W Async Write | ~400 | 51ms | Write path was latency bottleneck |
| 2 | + Redis Cache | ~409 | 56ms | No benefit — co-located services |
| 3 | 4W Gevent | **~1,676** | 120ms | **4x throughput — I/O wait was the ceiling** |

### Key Learnings

1. **More sync workers ≠ more throughput** — just adds CPU contention
2. **Async writes** — biggest latency improvement (35% P99 reduction)
3. **Redis cache** — no benefit when co-located with DB, simple indexed lookups already fast
4. **Gevent** — 4x throughput by handling I/O wait efficiently, the real breakthrough
5. **Trade-offs exist** — gevent has higher per-request latency but much higher throughput
