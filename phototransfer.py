from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import base64
import websockets
import uvicorn
import os

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing) to allow requests from different origins
origins = [
    "http://localhost",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

connected_clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_bytes()
            await broadcast_image(data)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        await broadcast_message("A client has disconnected.")

async def broadcast_image(image_data: bytes):
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{image_base64}"
    for client in connected_clients:
        try:
            await client.send_text(image_url)
        except WebSocketDisconnect:
            connected_clients.remove(client)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    # Perform any processing or save the image data as needed
    # For this example, we'll broadcast the image data to connected WebSocket clients
    await broadcast_image(contents)
    return JSONResponse(content={"message": "Image uploaded and broadcasted to all clients"})

@app.get("/")
async def send_message():
    return {"message": "Hello world"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
