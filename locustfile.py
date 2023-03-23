import random
import time
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def root(self):
        self.client.get('/')

    @task(2)
    def skip(self):
        self.client.get('/skip')

    @task(4)
    def item(self):
        item = 'item-{}'.format(
            random.randint(10,20)
        )
        self.client.get('/{}'.format(item))

    