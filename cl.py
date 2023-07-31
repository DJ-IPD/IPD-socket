import asyncio
import websockets

async def send_message():
    uri = "ws://127.0.0.1:8000/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            message = "Hello, all servers!"
            # await websocket.send(message)
            # print(f"Sent message: {message}")
            response = await websocket.recv()
            print(f"Received response: {response}")

            # Add a delay of 1 second between messages
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_message())
