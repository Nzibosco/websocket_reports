import asyncio
import ssl

import websockets
import datetime

async def client():
    #uri = "ws://localhost:8765" # The address the websocket server is running on

    # Using tls for encryption
    uri = "wss://localhost:8765"
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.check_hostname = False
    ssl_context.load_verify_locations('server.crt')

    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        while True:
            message = input("Enter your message (type 'exit' to quit): ")

            if message.lower() == 'exit':
                break

            await websocket.send(message)
            print(f"[{datetime.datetime.now()}] Sent message: {message}")

            response = await websocket.recv()
            print(f"[{datetime.datetime.now()}] Received message: {response}")

asyncio.get_event_loop().run_until_complete(client())
