import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
SHEET_NAME = "..."
WSHEET_NAME = "..."

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds/creds.json", scope)
client = gspread.authorize(creds)

gsheet = client.open(SHEET_NAME)  # Open the spreadhseet
sheet = gsheet.worksheet(WSHEET_NAME)


data = sheet.get_all_records()  # Get a list of all records

import pdb; pdb.set_trace()