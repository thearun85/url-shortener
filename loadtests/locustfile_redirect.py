from locust import HttpUser, task, between

class RedirectURLUser(HttpUser):

    wait_time = between(0.01, 0.05)

    def on_start(self):
        response = self.client.get(
            "/api/urls",
            json={"url": "http://example.com/redirect-test"},
        )

        if response.status_code == 201:
            self.short_code = response.json().get("short_code")
        else:
            self.short_code = None

    @task
    def redirect_url(self):
        if self.short_code:
            self.client.post(
                f"/{self.short_code}",
                allow_redirects=False,
                name="/[short_code]",
            )
