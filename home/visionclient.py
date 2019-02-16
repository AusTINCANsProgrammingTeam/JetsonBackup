#!/usr/bin/env python

# WS client example

import asyncio
import websockets

async def hello():
    async with websockets.connect(
            'ws://10.21.58.18:2158') as websocket:
        #name = input("What's your name? ")
        await websocket.send("begin")
        while True:
          websocket.send("X3")
          greeting = await websocket.recv()
          print(greeting)

asyncio.get_event_loop().run_until_complete(hello())
