from locust import HttpUser, task
from locust import between


class SecretaryBookingUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def secretary_book_competition_and_view_points(self):

        self.client.post('/showSummary', data={"email": "admin@irontemple.com"})

        self.client.get(f'/book/Fall%20Classic/Iron%20Temple')

        self.client.post('/purchasePlaces', data={
            'competition': "Fall Classic",
            'club': "Iron Temple",
            'places': '2'
            })

        self.client.get("/showclubs")