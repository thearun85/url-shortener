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
