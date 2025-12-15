from locust import HttpUser, task, between

class CreateURLUser(HttpUser):

    wait_time = between(0.01, 0.05)

    @task
    def create_url(self):
        self.client.post(
            "/api/urls",
            json={"url": "https://example.com/loadtest"},
        )
