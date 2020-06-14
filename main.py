from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service

def create_spreadsheet(title,columns):
    service = get_service()
    spreadsheet = {
        'properties': {
            'title': title
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                    fields='spreadsheetId').execute()

    spreadsheet_id = spreadsheet.get('spreadsheetId')
    print(f'Spreadsheet ID: {spreadsheet_id}'

    no_of_columns = len(columns)
    values = [columns]

    result = update_values(spreadsheet_id, 'A1', 'USER_ENTERED', values)

    return spreadsheet

def update_values(spreadsheet_id, range_name, value_input_option,
                  _values):
    service = get_service()

    values = _values
    # [END_EXCLUDE]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print(f"{result.get('updatedCells')} cells updated."
    # [END sheets_update_values]
    return result

def main():
    title = input("Enter the title of the spreadsheet :")
    columns = []
    while True:
        column = input()
        if column.strip() == 'done':
            break
        columns.append(column)

    create_spreadsheet(title,columns)

if __name__ == '__main__':
    main()
