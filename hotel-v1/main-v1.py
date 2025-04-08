import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

PORT=8331

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# "List of dicts" i python är ungefär samma som en "array of objects" (i JS)
rooms = [
    { "number": 103, "type": "single", "price": 89.9 },
    { "number": 204, "type": "double", "price": 120.5 },
    { "number": 305, "type": "family", "price": 150.8 }
]


# Get all rooms
@app.get("/rooms")
def get_rooms():
    return rooms

# Get one room
@app.get("/rooms/{id}")
def get_one_room(id: int):
    try:
        return rooms[id]
    except:
        return { "error": "Room not found" }

# Create booking
@app.post("/bookings")
def create_booking(request: Request):
    return { "msg": "booking created!"}



if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        ssl_keyfile="/etc/letsencrypt/privkey.pem",
        ssl_certfile="/etc/letsencrypt/fullchain.pem",
    )