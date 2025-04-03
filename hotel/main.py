import os, psycopg, uvicorn
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date

PORT=8331

#Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")

#print(DB_URL)
conn = psycopg.connect(DB_URL, autocommit=True, row_factory=dict_row)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# datamodell som ska valideras
class Booking(BaseModel):
    guest_id: int
    room_id: int
    datefrom: date
    dateto: date

#if-sats i python
@app.get("/if/{user_input}")
def if_test(user_input: str):
    message = None #None är samma som null i andra språk
    if user_input == "hello" or user_input == "hi": 
         message = "hello yourself!"
    elif user_input == "goodbye":
         message = "bye bye"
    else:
         message = "I do not understand!"

    return {"msg": user_input}



@app.get("/temp")
def temp():
    with conn.cursor() as cur:
         cur.execute("SELECT * FROM messages")
         messages = cur.fetchall()
    return {"msg": "Hello"}


@app.get("/temp/{}")
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
def get_rooms():
    with conn.cursor() as cur:
         cur.execute("""SELECT * FROM hotel_rooms ORDER BY room_number""")
         rooms = cur.fetchall()
    return rooms



@app.get("/rooms/{id}")
def get_one_room(id: int):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hotel_rooms WHERE id = %s", [id])
         #cur.execute("SELECT * FROM hotel_rooms WHERE id = %s", (id,)) #tuple
        #cur.execute("SELECT * FROM hotel_rooms WHERE id = %(id)s", {"id: id"})
        room = cur.fetchone()
        if not room:
            return {"msg": "Room not found"}
    return room



@app.post("/bookings")
def create_booking(booking: Booking):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO hotel_bookings (guest_id, room_id) VALUES (%s, %s, %s, %s) RETURNING id""", [booking.guest_id, booking.room_id, booking.datefrom, booking.dateto])
        new_id = cur.fetchone()['id']
    return {"msg": "booking created!", "id": new_id}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        ssl_keyfile="/etc/letsencrypt/privkey.pem",
        ssl_certfile="/etc/letsencrypt/fullchain.pem",
    )