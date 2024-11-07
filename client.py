from config import *
from ws import WS
import copy
from rich.pretty import pprint as print
import anyio
import json


async def main():
    params = {
        'wss' : url,
        'headers' : headers,
        'test' : start_msg
    }

    client = WS(params)

    client.start()

    try:
        while True:
            await anyio.sleep(1)
    except:
        exit("def main close")

        
if __name__ == "__main__":
    anyio.run(main)