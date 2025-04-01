import os, psycopg, uvicorn
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

PORT=8331

#Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")

print(DB_URL)
conn = psycopg.connect(DB_URL, autocommit=True, row_factory=dict_row)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/temp")
def temp():
    with conn.cursor() as cur:
         cur.execute("SELECT * FROM messages")
         messages = cur.fetchall()
    return {"msg": "Hello"}


# "List of dicts" i python är ungefär samma som en "array of objects" (i JS)
rooms = [
    { "number": 103, "type": "single", "price": 89.9 },
    { "number": 204, "type": "double", "price": 120.5 },
    { "number": 305, "type": "family", "price": 150.8 }
]

@app.get("/rooms")
def getRooms(request: Request):
    return rooms


@app.get("/rooms/{id}")
def getRooms(id: int):
    try:
        return rooms[id]
    except:
            return { "error": "Room not found"}

@app.post("/bookings")
def create_booking(request: Request):
    return {"msg": "booking created!"}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        ssl_keyfile="/etc/letsencrypt/privkey.pem",
        ssl_certfile="/etc/letsencrypt/fullchain.pem",
    )