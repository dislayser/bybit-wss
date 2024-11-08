import asyncio
import websockets
import time
from asyncio import Queue
from rich.pretty import pprint as print
import json
import gzip
import io
import ssl

class WS:
    def __init__(self, url, headers = '[]', ssl = None):
        self.url = url
        self.headers = json.loads(headers)
        self.ssl = ssl
        self.ws = None

        self.run = False

        self.queue = Queue()
        self.tasks = []

    async def connect(self):
        while self.run:
            if not self.ssl:
                self.ssl = ssl._create_unverified_context()
            try:
                self.ws = await websockets.connect(
                    uri=self.url,
                    extra_headers=self.headers,
                    ssl=self.ssl
                )
            except Exception as e:
                print("Ошибка WebSocket")
                print(e)
                asyncio.create_task(self.stop("Ошибка WebSocket"))
