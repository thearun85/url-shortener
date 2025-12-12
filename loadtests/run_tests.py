#!/usr/bin/env python3
"""
Load testing script using hey.
Seeds URLs then runs tests at various concurrency levels.
"""

import requests
import subprocess
import time
import sys
import os

APP_URL = os.getenv("APP_URL", "http://host.docker.internal:5000")
DURATION = os.getenv("TEST_DURATION", "10s")


def wait_for_app(timeout=60):
    """Wait for app to be ready."""
    print(f"Waiting for app at {APP_URL}...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"{APP_URL}/health", timeout=2)
            if r.status_code == 200:
                print("App is ready.\n")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    print("ERROR: App not ready after timeout")
    return False


def seed_urls(count=50):
    """Create test URLs and return a short code for redirect testing."""
    print(f"Seeding {count} URLs...")
    short_code = None
    
    for i in range(count):
        try:
            r = requests.post(
                f"{APP_URL}/api/urls",
                json={"url": f"https://example.com/page/{i}"},
                timeout=10
            )
            if r.status_code == 201:
                short_code = r.json().get("short_code")
        except requests.exceptions.RequestException as e:
            print(f"  Error seeding URL {i}: {e}")
    
    print(f"Done. Test short code: {short_code}\n")
    return short_code


def run_hey(name, url, concurrency, method="GET", body=None, disable_redirects=False):
    """Run hey and print results."""
    cmd = [
        "hey",
        "-z", DURATION,
        "-c", str(concurrency),
        "-m", method,
    ]
    
    if disable_redirects:
        cmd.append("-disable-redirects")
    
    if body:
        cmd.extend(["-H", "Content-Type: application/json", "-d", body])
    
    cmd.append(url)
    
    print(f"--- {name} (c={concurrency}) ---")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Parse and display key metrics
    output = result.stdout
    for line in output.split("\n"):
        line = line.strip()
        if any(k in line for k in ["Requests/sec", "Total:", "Slowest:", "Fastest:", "Average:", "50%", "95%", "99%", "[200]", "[201]", "[301]", "[302]", "[400]", "[404]", "[500]"]):
            print(f"  {line}")
    
    print()
    return output


def main():
    if not wait_for_app():
        sys.exit(1)
    
    short_code = seed_urls(50)
    if not short_code:
        print("ERROR: Failed to seed URLs")
        sys.exit(1)
    
    concurrency_levels = [1, 10, 50, 100]
    
    print("=" * 60)
    print("REDIRECT TEST (GET /<short_code>)")
    print("=" * 60)
    for c in concurrency_levels:
        run_hey(
            "Redirect",
            f"{APP_URL}/{short_code}",
            concurrency=c,
            disable_redirects=True
        )
    
    print("=" * 60)
    print("CREATE URL TEST (POST /api/urls)")
    print("=" * 60)
    for c in concurrency_levels:
        run_hey(
            "Create",
            f"{APP_URL}/api/urls",
            concurrency=c,
            method="POST",
            body='{"url":"https://example.com/loadtest"}'
        )
    
    print("=" * 60)
    print("HEALTH CHECK TEST (GET /health)")
    print("=" * 60)
    run_hey("Health", f"{APP_URL}/health", concurrency=100)
    
    print("Load tests complete.")


if __name__ == "__main__":
    main()
