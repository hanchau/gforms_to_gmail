import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client.service_account import ServiceAccountCredentials
# If modifying these scopes, delete the file token.pickle.
from tests.gsheet_test import *


SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def authenticate():
    # import pdb; pdb.set_trace()
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'creds/creds.json', scopes=SCOPES)

    service = build('drive', 'v3', credentials=creds)

    return service


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """

    service = authenticate()

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()