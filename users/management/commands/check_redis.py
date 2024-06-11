import redis
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Check if Redis server is running'

    def handle(self, *args, **kwargs):
        try:
            # Attempt to connect to Redis server
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.ping()
            self.stdout.write(self.style.SUCCESS('Redis server is running'))
        except redis.ConnectionError:
            self.stdout.write(self.style.ERROR('Redis server is not running'))
