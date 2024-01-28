from datetime import datetime, timedelta
import os

import google_auth_httplib2
import httplib2
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

class BaseAPI(object):
    API_SECRET_FILE_NAME = 'old/credentials.json'
    TOKEN_FILE_NAME = ''
    TOKEN_SCOPES = []

    SERVICE_NAME = ''
    API_VERSION = ''

    PROXY_HOST = '127.0.0.1'
    PROXY_PORT = 8080

    def __init__(self, use_proxy=False):
        self.use_proxy = use_proxy
        self.api = self.init_api()

    def init_api(self):
        creds = None

        # Check if a token file exists already
        if os.path.exists(self.TOKEN_FILE_NAME):
            creds = Credentials.from_authorized_user_file(self.TOKEN_FILE_NAME, self.TOKEN_SCOPES)

        # If no creds or creds are invalid
        if not creds or not creds.valid:
            # Refresh
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.API_SECRET_FILE_NAME):
                    print(f'[!] API token not find, download it and name it {self.API_SECRET_FILE_NAME}')
                    exit()

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.API_SECRET_FILE_NAME, self.TOKEN_SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(self.TOKEN_FILE_NAME, "w") as token:
                token.write(creds.to_json())

        # Optionally a proxy
        if self.use_proxy:
            http = httplib2.Http(proxy_info=httplib2.ProxyInfo(
                3, self.PROXY_HOST, self.PROXY_PORT
            ), disable_ssl_certificate_validation=True)
            authorized_http = google_auth_httplib2.AuthorizedHttp(creds, http=http)
            return build(self.SERVICE_NAME, self.API_VERSION, http=authorized_http)
        else:
            return build(self.SERVICE_NAME, self.API_VERSION, credentials=creds)
