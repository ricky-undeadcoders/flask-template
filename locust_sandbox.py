from locust import HttpLocust, TaskSet
import subprocess
import os


def index(l):
    l.client.get("/")


class UserBehavior(TaskSet):
    tasks = {index: 2}


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 50
    max_wait = 9000


if __name__ == "__main__":
    host = 'http://35.192.19.198'
    subprocess.call('locust -f {} --host={}'.format(__file__, host))
