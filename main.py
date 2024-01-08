import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
    try:
        creds = auth()
        [dates, times, calendar_id, location] = load_data('rota.json')
        service = build("calendar", "v3", credentials=creds)

        for date, code in dates.items():
            if code in times:
                event = create_event(service, calendar_id, location, date, times[code]['start'], times[code]['end'])
                print('Event created: %s' % (event.get('htmlLink')))
            else:
                continue

    except Exception as e:
        print(f"An error occurred: {e}")


def create_event(service, cal_id, location, date, start, end):
    event = {
        'summary': 'Work',
        'location': location,
        'description': 'I\'m scared to delete this.',
        'start': {
            'dateTime': f'{date}T{start}',
            'timeZone': 'Europe/London',
        },
        'end': {
            'dateTime': f'{date}T{end}',
            'timeZone': 'Europe/London',
        }
    }

    return service.events().insert(calendarId=cal_id, body=event).execute()


def load_data(file):
    with open(file, 'r') as f:
        data = json.load(f)

    dates = data["times"]
    times = data["dates"]
    calendar_id = data["calendar_id"]

    return dates, times, calendar_id


def auth():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


if __name__ == "__main__":
    main()
