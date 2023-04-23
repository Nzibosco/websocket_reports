import asyncio
import websockets
import datetime

async def client():
    uri = "ws://localhost:8765" # The address the websocket server is running on
    async with websockets.connect(uri) as websocket:
        while True:
            message = input("Enter your message (type 'exit' to quit): ")

            if message.lower() == 'exit':
                break

            await websocket.send(message)
            print(f"[{datetime.datetime.now()}] Sent message: {message}")

            response = await websocket.recv()
            print(f"[{datetime.datetime.now()}] Received message: {response}")

asyncio.get_event_loop().run_until_complete(client())
