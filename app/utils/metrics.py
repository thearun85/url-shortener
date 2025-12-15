from prometheus_client import Counter, Histogram, generate_latest, REGISTRY, CONTENT_TYPE_LATEST

url_creates_total = Counter(
    "url_creates_total",
    "Total URLs created"
)

url_redirects_total = Counter(
    "url_redirects_total",
    "Total Redirects served"
)

url_collisions_total = Counter(
    "url_collisions_total",
    "Total short code collisions"
)

request_duration_seconds = Histogram(
    'request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint'],
    buckets = [0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

def get_metrics():
    return generate_latest(REGISTRY), CONTENT_TYPE_LATEST
