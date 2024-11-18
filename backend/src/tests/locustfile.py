from random import randint

from locust import HttpUser, task

from utils.utils import random_lower_string, random_start_end


class UserBehavior(HttpUser):
    def on_start(self):
        self.login()

    def login(self):
        headers = {
            'User-Agent': 'sitename.app',
            'referer': 'http://localhost:8090',
        }
        response = self.client.post(
            '/api/v1/users/access-token',
            {'username': 'user@q.q', 'password': 'qwertyqw'},
            headers=headers,
        )
        self.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}

    @task(6)
    def index(self):
        self.client.get('/api/v1/anime', headers=self.headers)

    @task(6)
    def start_end_list(self):
        self.client.get('/api/v1/anime/start-end-list', headers=self.headers)

    @task(1)
    def create_anime(self):
        s = random_lower_string()
        self.client.post(
            '/api/v1/anime/create',
            json={
                "name": s,
                "rate": randint(1, 10),
                "start_end": random_start_end(randint(1, 2)),
                "review": s,
            },
            headers=self.headers,
        )
