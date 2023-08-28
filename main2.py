# ///////////////////send data only to specific user


from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

app = FastAPI()
connected_clients = {}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    connected_clients[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            await send_message_to_user(data, user_id)
    except WebSocketDisconnect:
        del connected_clients[user_id]
        await send_message_to_all("User has disconnected.", excluded_user_id=user_id)

async def send_message_to_user(message: str, user_id: int):
    websocket = connected_clients.get(user_id)
    if websocket:
        await websocket.send_text(message)

async def send_message_to_all(message: str, excluded_user_id: int = None):
    for user_id, websocket in connected_clients.items():
        if user_id != excluded_user_id:
            await websocket.send_text(message)
@app.post("/send_message/{user_id}")
async def send_message(user_id: int, message: str):
    await send_message_to_user(message, user_id)
    return {"message": f"Message sent to user {user_id}"}

@app.get("/")
async def send_message():
    return {"message": "Hello world"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)