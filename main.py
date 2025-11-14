# main.py
from fastapi import Body, FastAPI, HTTPException
from bson import ObjectId
from repository import db
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import requests
from ics import Calendar
from datetime import datetime, timedelta, timezone

load_dotenv()

FE_DEV_URL = os.getenv("FE_DEV_URL")
FE_PROD_AZURE_URL = os.getenv("FE_PROD_AZURE_URL")
FE_PROD_RENDER_URL = os.getenv("FE_PROD_RENDER_URL")
ICAL_URL = os.getenv("ICAL_URL")

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

@app.get("/events")
def get_calendar_events():
    try:
        response = requests.get(ICAL_URL)
        response.raise_for_status()
        calendar = Calendar(response.text)

        # 🕕 Define your date range: today 06:00 → one month ahead
        now = datetime.now(timezone.utc)
        today_6am = now.replace(hour=6, minute=0, second=0, microsecond=0)
        if now.hour < 6:
            # If it's before 6AM now, we still want "today 6AM" from this morning
            today_6am = today_6am - timedelta(days=1)
        one_month_later = today_6am + timedelta(days=30)

        events = []
        for event in calendar.events:
            if not event.begin:
                continue

            start = event.begin.datetime
            end = event.end.datetime if event.end else None

            # ✅ Include events starting from today 6:00 up to 30 days ahead
            if today_6am <= start <= one_month_later and event.description != "Narozeniny":
                events.append({
                    "summary": event.name or "(No title)",
                    "description": event.description or "",
                    "start": start.isoformat(),
                    "end": end.isoformat() if end else None,
                    "location": event.location or "",
                })

        # Sort chronologically
        events.sort(key=lambda e: e["start"])
        return events

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/birthdays")
def get_calendar_events():
    try:
        response = requests.get(ICAL_URL)
        response.raise_for_status()
        calendar = Calendar(response.text)

        now = datetime.now(timezone.utc)
        today_6am = now.replace(hour=6, minute=0, second=0, microsecond=0)
        if now.hour < 6:
            today_6am = today_6am - timedelta(days=1)
        one_week_later = today_6am + timedelta(days=6)

        events = []
        for event in calendar.events:
            if not event.begin:
                continue

            start = event.begin.datetime
            end = event.end.datetime if event.end else None

            if today_6am <= end <= one_week_later and event.description == "Narozeniny":
                events.append({
                    "summary": event.name or "(No title)",
                    "description": event.description or "",
                    "start": start.isoformat(),
                    "end": end.isoformat() if end else None,
                    "location": event.location or "",
                })

        events.sort(key=lambda e: e["start"])
        return events

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
