import dotenv
import os

dotenv.load_dotenv()

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
BOT_TOKEN = os.getenv('BOT_TOKEN')
MAIN_WORK_SHEET_ID = int(os.getenv('MAIN_WORK_SHEET_ID'))

GOOGLE_SHEETS_CREDENTIALS_FILE = 'keys.json'