import anyio
import asyncio
import websockets
import random
import time
from asyncio import Queue
import json
import sys
import os
import math
# import logging
from rich.pretty import pprint as print
from datetime import datetime

import gzip
import io
import ssl

class WS:
    def __init__(self, params):
        self.params = params

        self.queue = Queue()
        self.run = False
        self.tasks = []
        self.ws = None


    # Старт
    def start(self):
        if not self.run:
            self.run = True

            self.tasks.extend([
                asyncio.create_task(self.messages_to_queue()),
                asyncio.create_task(self.handle_session()),
            ])

    # Сообщение которые отправляется по интервалу
    def ping_msg(self):
        msg = '{"op":"ping","args":[' + str(int(time.time() * 1000)) + ']}'
        return msg
    
    async def handle_session(self):
        while self.run:
            try:
                message = await self.queue.get()
                
                with gzip.GzipFile(fileobj=io.BytesIO(message)) as f:
                    decompressed_data = f.read()
                # Теперь декодируем полученные данные в строку
                decoded_message = decompressed_data.decode('utf-8')
                decoded_message = json.loads(decoded_message)
                print(decoded_message)

            except Exception as e:
                print("error handle messages")
                print(e)
                continue
    
    async def messages_to_queue(self):
        while self.run:
            print(self.params)
            ssl_context = ssl._create_unverified_context()
            try:
                headers = json.loads(self.params['headers'])
                self.ws = await websockets.connect(
                    uri=self.params['wss'],
                    extra_headers=headers,
                    ssl=ssl_context
                )
                print(self.ws)
                await self.ws.send(self.params['test'])
                async for message in self.ws:
                    await self.queue.put(message)
            except ValueError as e:
                print("Ошибка ValueError")
                print(e)
                asyncio.create_task(self.stop("Ошибка при подключении к WebSocket"))
            except Exception as e:
                print("Ошибка WebSocket")
                print(e)
                asyncio.create_task(self.stop("Ошибка WebSocket"))
        asyncio.create_task(self.stop("Невозможно подключиться к серверу"))