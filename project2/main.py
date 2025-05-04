import os, psycopg, uvicorn
from datetime import datetime
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")

#print(DB_URL)
# Create DB connection
conn = psycopg.connect(DB_URL, autocommit=True, row_factory=dict_row)

PORT=8335

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


class MyTodo(BaseModel):
    title: str
    category_id: int


class MyTodoUpdate(BaseModel):
    title: Optional[str] = None
    category_id: Optional[int] = None
    done: Optional[datetime] = None   


# Funktion för att validera API-key.    
def user_validate_key(api_key: str = ""):
    if not api_key:
        raise HTTPException(status_code=401, detail={"error": "API key missing!"})
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM todo_users WHERE api_key = %s""", [api_key])
        user = cur.fetchone()
        if not user:
            raise HTTPException(status_code=401, detail={"error": "Bad API key!"})
        return user


#Hello
@app.get("/")
def hello():
    return { "message": "Hello FastAPI" }



#get
@app.get("/todos")
def get_todo_notes(user: dict = Depends(user_validate_key)):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT tn.id, tn.title, tn.done, tn.created_at, tc.category_name
            FROM todo_notes tn
            JOIN todo_categori tc ON tn.category_id = tc.id
            WHERE tn.user_id = %s
            ORDER BY tn.created_at DESC
        """, [user["id"]])
        notes = cur.fetchall()
        return notes
    


#post (create)
@app.post("/todos")
def create_todo_note(todo: MyTodo, user: dict = Depends(user_validate_key)):
    now = datetime.utcnow()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO todo_notes (user_id, category_id, title, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
        """, [user["id"], todo.category_id, todo.title, now, now])
    return {"msg": "Note created!"}


#delete
@app.delete("/todos/{id}")
def delete_todo_note(id: int, user: dict = Depends(user_validate_key)):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM todo_notes WHERE id = %s AND user_id = %s", [id, user["id"]])
    return {"msg": "Note deleted!"}


#put (update)
@app.put("/todos/{id}")
def update_todo_note(id: int, todo: MyTodoUpdate, user: dict = Depends(user_validate_key)):
    fields = []
    values = []

    if todo.title is not None:
        fields.append("title = %s")
        values.append(todo.title)
    if todo.category_id is not None:
        fields.append("category_id = %s")
        values.append(todo.category_id)
    if todo.done is not None:
        fields.append("done = %s")
        values.append(todo.done)

    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    fields.append("updated_at = now()")
    values.extend([id, user["id"]])

    query = f"""
        UPDATE todo_notes SET {', '.join(fields)}
        WHERE id = %s AND user_id = %s
    """

    with conn.cursor() as cur:
        cur.execute(query, values)

    return {"msg": "Note updated!"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        ssl_keyfile="/etc/letsencrypt/privkey.pem",
        ssl_certfile="/etc/letsencrypt/fullchain.pem",
    )