# calendar_plugin.py
from fastapi import Depends, FastAPI, HTTPException, Header
from pydantic import BaseModel
from calendarService import CalendarService
import string, random

#generate a strong token for the API_TOKEN variable below
def generate_random_string():
    SECRET = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
    with open(".well-known/secrets", "w") as f:
        f.write(SECRET)
    return SECRET

API_TOKEN = generate_random_string()
print(f"Your API token is: {API_TOKEN}")

app = FastAPI()

class EventRequest(BaseModel):
    summary: str
    title: str
    description: str
    location: str
    start_time: str
    end_time: str

def verify_token(Authorization: str = Header(...)):
  if Authorization != f"Bearer {API_TOKEN}":
    raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/events")
def list_events(token: str = Depends(verify_token)):
    return {"events": CalendarService.getEvents()}  # make sure getEvents returns JSON-serializable data

@app.post("/events")
def create_event(event: EventRequest, token: str = Depends(verify_token)):
    url = CalendarService.makeEvent(**event.dict())
    return {"message": "Event created", "event_url": url}
