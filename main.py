from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

app = FastAPI()
connected_clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await broadcast_message(data)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        await broadcast_message("A client has disconnected.")

async def broadcast_message(message: str):
    for client in connected_clients:
        try:
            await client.send_text(message)
        except WebSocketDisconnect:
            connected_clients.remove(client)

@app.post("/send_message/")
async def send_message(message: str):
    await broadcast_message(message)
    return {"message": "Message sent to all clients"}


@app.get("/")
async def send_message():
    return {"message": "Hello world"}    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)





