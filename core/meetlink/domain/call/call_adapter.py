from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2


class CallOutputDTO :
    def __init__(self, call_uri):
        self.call_uri = call_uri


class CallAdapter() :
    def create_call() :
        pass


class GoogleMeetAdapter(CallAdapter):
    def __init__(self) :
        self.SCOPES = ['https://www.googleapis.com/auth/meetings.space.created']

    def create_call(self) :
        creds = None

        if os.path.exists('../.google/token.json'):
            creds = Credentials.from_authorized_user_file('../.google/token.json', self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '../.google/credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)

            with open('../.google/token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            client = meet_v2.SpacesServiceClient(credentials=creds)
            request = meet_v2.CreateSpaceRequest()
            response = client.create_space(request=request)
            print(f'Space created: {response.meeting_uri}')

            data = CallOutputDTO(response.meeting_uri)

            return data

        except Exception as error:
            print(f'An error occurred: {error}')