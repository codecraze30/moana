import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime  # For current date
import logging  # For logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Google Sheets setup
def setup_google_sheets():
    """
    Set up the Google Sheets client using credentials and return the sheet object.
    """
    try:
        # Load environment variables
        service_account_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', './credentials.json')
        sheet_id = os.getenv('SHEET_ID')

        if not service_account_file:
            raise ValueError("Environment variable 'GOOGLE_APPLICATION_CREDENTIALS' is not set.")
        if not sheet_id:
            raise ValueError("Environment variable 'SHEET_ID' is not set.")

        # Authenticate with Google APIs
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(service_account_file, scopes=scopes)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id)
        
        logging.info(f"Successfully connected to the Google Sheet: {sheet.title}")
        return sheet
    except Exception as e:
        logging.error("Failed to set up Google Sheets client. Check credentials and environment variables.")
        raise e

def get_or_create_worksheet(sheet, tab_name):
    """
    Get an existing worksheet by name or create a new one with default headers.
    """
    try:
        # Try to retrieve the existing worksheet
        worksheet = sheet.worksheet(tab_name)
        logging.info(f"Worksheet '{tab_name}' already exists.")
    except gspread.exceptions.WorksheetNotFound:
        # If it doesn't exist, create a new worksheet
        logging.warning(f"Worksheet '{tab_name}' not found. Creating a new one.")
        worksheet = sheet.add_worksheet(title=tab_name, rows=1000, cols=10)
        # Add headers to the new worksheet
        headers = [['Date', 'Title', 'Company', 'Pay', 'Job Type', 'Work Setting', 'URL']]
        worksheet.update('A1:G1', headers)
        logging.info(f"New worksheet '{tab_name}' created with headers: {headers[0]}")
    return worksheet

def save_to_google_sheet(worksheet, data):
    """
    Save data to the specified worksheet, appending rows with the current date.
    """
    try:
        # Prepare rows with the current date
        current_date = datetime.now().strftime('%Y-%m-%d')  # YYYY-MM-DD format
        rows = [[
            current_date,  # Insert current date in the first column
            job.get('title', ''), 
            job.get('company', ''), 
            job.get('pay', ''), 
            job.get('job_type', ''), 
            job.get('work_setting', ''), 
            job.get('url', '')
        ] for job in data]

        # Append rows to the worksheet
        worksheet.append_rows(rows)
        logging.info(f"Successfully saved data to '{worksheet.title}' worksheet.")
    except Exception as e:
        logging.error(f"Failed to save data to worksheet '{worksheet.title}': {e}")
        raise e