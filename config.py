import dotenv
import os

dotenv.load_dotenv()

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SHEET_ID = os.getenv('SHEET_ID')
BOT_TOKEN = os.getenv('BOT_TOKEN')
GOOGLE_SHEETS_CREDENTIALS_FILE = 'keys.json'