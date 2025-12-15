# Benchmarks

## Phase 0: Sync Baseline (v0.1)

Gunicorn server (1 worker) with synchronous Postgres operations.

### Results

| Users | Requests/s | Median | P95  | P99  | Failures |
|-------|-----------|--------|------|------|----------|
| 1     | ~24       | 10ms   | 14ms | 16ms | 0 (0%)   |
| 20    | ~355      | 4ms    | 9ms  | 17ms | 1 (0.06%)|
| 100   | ~372      | 11ms   | 32ms | 39ms | 2 (0.06%)|
| 200   | ~409      | 30ms   | 72ms | 79ms | 4 (0.1%) |

### Observations

- **Throughput ceiling**: ~400 req/s regardless of user count
- **Latency degradation**: P99 grows from 16ms → 79ms under load
- **Failure pattern**: 500 errors on POST /api/urls under concurrency

### Raw Data

See [results/v0.1/](docs/results/v0.1/) for full CSVs.
