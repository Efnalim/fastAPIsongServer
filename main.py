# main.py
from fastapi import Body, FastAPI, HTTPException
from bson import ObjectId
from repository import db
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

FE_DEV_URL = os.getenv("FE_DEV_URL")
FE_PROD_AZURE_URL = os.getenv("FE_PROD_AZURE_URL")
FE_PROD_RENDER_URL = os.getenv("FE_PROD_RENDER_URL")

app = FastAPI()

origins = [
    FE_DEV_URL,       
    FE_PROD_AZURE_URL,
    FE_PROD_RENDER_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],            # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],            # Allow all headers (Authorization, Content-Type, etc.)
)

# Helper to convert MongoDB documents to JSON-friendly dicts
def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.get("/hymns")
async def get_users():
    hymns = await db.hymns.find().to_list()  # 'hymns' is your MongoDB collection
    return [serialize_doc(hymn) for hymn in hymns]

@app.get("/songs")
async def get_users():
    songs = await db.songs.find().to_list()
    return [serialize_doc(song) for song in songs]

@app.put("/hymns")
async def update_hymn(hymn = Body(...)):
    """Update an existing hymn by its ID."""
    update_data = {k: v for k, v in hymn.items() if v is not None and k != "_id"}
    result = await db.hymns.update_one({"_id": ObjectId(hymn["_id"])}, {"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Hymn not found")

    hymns = await db.hymns.find().to_list()
    return [serialize_doc(hymn) for hymn in hymns]

@app.put("/songs")
async def update_song(song = Body(...)):
    """Update an existing hymn by its ID."""
    update_data = {k: v for k, v in song.items() if v is not None and k != "_id"}
    result = await db.songs.update_one({"_id": ObjectId(song["_id"])}, {"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Song not found")

    songs = await db.songs.find().to_list()
    return [serialize_doc(song) for song in songs]

@app.post("/songs")
async def create_song(song = Body(...)):
    """Update an existing hymn by its ID."""
    # create_data = {k: v for k, v in song.items() if v is not None}
    result = await db.songs.insert_one(song)

    if result.acknowledged is False:
        raise HTTPException(status_code=404, detail="Song not created")

    songs = await db.songs.find().to_list()
    return [serialize_doc(song) for song in songs]

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        return serialize_doc(user)
    return {"error": "User not found"}
