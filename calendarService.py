import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class CalendarService():
    def getService():
      SCOPES = ["https://www.googleapis.com/auth/calendar"]
      creds = None

      # Token file stores the user's access/refresh tokens
      if os.path.exists("token.json"):
        # using API KEY to access calendar
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

      # If no valid creds available, let user log in.
      if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
        else:
          flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
          creds = flow.run_local_server(port=0)

        # Save the creds for the next run
        with open("token.json", "w") as token:
          token.write(creds.to_json())

        # Connect to Google Calendar API
      service = build("calendar", "v3", credentials=creds)
      return service

    def getEvents():
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z';
        #now = datetime.datetime.now(datetime.timezone.utc).isoformat() + 'Z';

        service = CalendarService.getService()
        s = service.events().list(
            calendarId="primary", timeMin=now, maxResults=10, singleEvents=True, orderBy="startTime"
        ).execute()

        event_list = []
        for event in s["items"]:
           event_list.append({
            "id": event.get("id"),
            "summary": event.get("summary"),
            "description": event.get("description"),
            "location": event.get("location"),
            "start": event.get("start", {}).get("dateTime", event.get("start", {}).get("date")),
            "end": event.get("end", {}).get("dateTime", event.get("end", {}).get("date")),
            "htmlLink": event.get("htmlLink")
            })


        print(event_list)
        return event_list

    def makeEvent(summary, title, description, location, start_time, end_time):
       service = CalendarService.getService()

       # Create the event
       event = {
          "summary": summary,
          "start": {"dateTime": start_time},
          "end": {"dateTime": end_time},
          "description": description,
          "location": location,
       }
       # Insert the event into the calendar
       event = service.events().insert(calendarId="primary", body=event).execute()
       print(f"Event created: {event.get('htmlLink')}") 
