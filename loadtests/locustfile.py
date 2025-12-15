from locust import HttpUser, task, between
import random

class URLShortenerUser(HttpUser):

    wait_time = between(0.01, 0.05)

    def on_start(self):
        self.short_codes = []
        response = self.client.post(
            "/api/urls",
            json={"url": "http://example.com/test"},
        )

        if response.status_code  == 201:
            self.short_codes.append(response.json().get("short_code"))

    @task(1)
    def health_check(self):
        self.client.get("/health")

    @task(3)
    def create_url(self):
        response = self.client.post(
            "/api/urls",
            json={"url": "http://example.com/page"},
        )
        if response.status_code == 201:
            code = response.json().get("short_code")
            if code:
                self.short_codes.append(code)
        
    @task(10)
    def redirect_url(self):
        if self.short_codes:
            code = random.choice(self.short_codes)
            self.client.get(
                f"/{code}", 
                allow_redirects=False, 
                name="/[short_code]"),

    @task(2)
    def get_url_details(self):
        if self.short_codes:
            code = random.choice(self.short_codes)
            self.client.get(
                f"/api/urls/{code}",
                name="/api/urls/[short_code]",
            )
