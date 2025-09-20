from locust import HttpUser, task
from locust import between


class SecretaryUser(HttpUser):
    wait_time = between(1, 5)

    @task(2)
    def secretary_book_competition_and_view_points(self):
        self.client.post("/showSummary", data={
            "email": "admin@irontemple.com"
        })
        self.client.get("/book/Fall%20Classic/Iron%20Temple")
        self.client.post(
            "/purchasePlaces",
            data={
                "competition": "Fall Classic",
                "club": "Iron Temple",
                "places": "2"
            },
        )
        self.client.get("/logout")

    @task
    def another_secretary_book_another_competition(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})
        self.client.get("/book/Winter%20Classic/Simply%20Lift")
        self.client.post(
            "/purchasePlaces",
            data={
                "competition": "Winter Classic",
                "club": "Simply Lift",
                "places": "3",
            },
        )
        self.client.get("/logout")

    @task
    def a_secretary_view_clubs(self):
        self.client.post("/showSummary", data={"email": "kate@shelifts.co.uk"})
        self.client.get("/showclubs")
        self.client.get("/logout")

    @task
    def invalid_login_attempt(self):
        self.client.post("/showSummary", data={"email": "wrongmail@nthg.com"})
