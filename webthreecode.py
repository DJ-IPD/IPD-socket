from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any


app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",  # Replace with your frontend's URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# from pydantic import BaseModel



@app.post("/send-public-key")
def send_public_key(payload: Dict[Any, Any]):
    print(payload)
    # public_key = request.publicKey
    # Handle the public key data
    return {"message": "Public key received successfully"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
