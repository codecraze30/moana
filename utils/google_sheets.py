import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime  # Import datetime for current date

# Google Sheets setup
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', './credentials.json')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

SHEET_ID = os.getenv('SHEET_ID')
sheet = client.open_by_key(SHEET_ID)

def get_or_create_worksheet(tab_name):
    try:
        # Try to retrieve the existing worksheet
        worksheet = sheet.worksheet(tab_name)
        print(f"Worksheet '{tab_name}' already exists.")
    except gspread.exceptions.WorksheetNotFound:
        # If it doesn't exist, create a new worksheet
        print(f"Worksheet '{tab_name}' not found. Creating a new one.")
        worksheet = sheet.add_worksheet(title=tab_name, rows=1000, cols=10)
        # Add headers to the new worksheet
        worksheet.update('A1:G1', [['Date', 'Title', 'Company', 'Pay', 'Job Type', 'Work Setting', 'URL']])
    return worksheet

def save_to_google_sheet(worksheet, data):
    current_date = datetime.now().strftime('%Y-%m-%d')  # Get the current date in YYYY-MM-DD format
    rows = [[
        current_date,  # Insert current date in the first column
        job['title'], 
        job['company'], 
        job['pay'], 
        job['job_type'], 
        job['work_setting'], 
        job['url']
    ] for job in data]
    worksheet.append_rows(rows)
    print(f"Data saved to '{worksheet.title}' tab.")
