"""
title: GCal
author: binchick-in
author_url: billben.net
git_url: https://github.com/binchick-in/ai-stack
description: This tool does google calendar things
required_open_webui_version: 0.4.0
requirements: google-api-python-client, google-auth-oauthlib, pytz
version: 0.4.0
licence: MIT
"""
from typing import Literal
from typing import TypeAlias
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz

REFRESH_TOKEN = None  # Fill this in!
SCOPES = ["https://mail.google.com/"]
GoogleAPIName: TypeAlias = Literal["gmail"]


def _build_service(api_name: GoogleAPIName, api_version: str):
    """Build and return Gmail API service object."""
    creds = Credentials.from_authorized_user_info(REFRESH_TOKEN, SCOPES)
    return build(api_name, api_version, credentials=creds)


class GoogleClient:
    api_name: GoogleAPIName
    api_version: str

    def __init__(self):
        self._google_service = _build_service(self.api_name, self.api_version)


class GoogleCalendarClient(GoogleClient):
    """
    Docs: https://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html
    """
    api_name = "calendar"
    api_version = "v3"

    def fetch_events_next_10_days(self):
        """Fetch events for the next 10 days from the primary calendar."""

        now = datetime.now(pytz.timezone('America/Los_Angeles'))
        time_min = now.isoformat()
        time_max = (now + timedelta(days=10)).isoformat()

        events_result = self._google_service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        return [{'summary': event.get('summary'), 'start': event.get('start'), 'end': event.get('end')} for event in events]


class Tools:
    def get_upcoming_calendar_events(self) -> str:
        """Get upcoming calednar events.
        """
        gcal_client = GoogleCalendarClient()
        return gcal_client.fetch_events_next_10_days()
