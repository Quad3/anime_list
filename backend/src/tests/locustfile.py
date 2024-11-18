from locust import HttpUser, task


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

    @task(1)
    def index(self):
        self.client.get('/api/v1/anime', headers=self.headers)

    @task(2)
    def start_end_list(self):
        self.client.get('/api/v1/anime/start-end-list', headers=self.headers)
