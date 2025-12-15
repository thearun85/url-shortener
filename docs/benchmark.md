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
