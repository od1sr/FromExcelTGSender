'''
The main google sheet format:
|   A       | B       |     C      |          D        |        E      |          F        |            G           |
=====================================================================================================================
| Подрядчик | ID      | Сообщение  |	  Отправка     |	Время план |       Статус	   |      Время факт        |

Explanation:
 (ignored)   (Tg chat) (text to send) (do send(ignored))  (when to send)  (is sent (Да/Нет)) (when was acutally sent)

Example:
|  Иванов   | 123456  |   Привет!  |       Да          | 01.12.2025 10:00:00 |   Нет       |                        |
|  Петров   | 321321  |   Пока!    |       Да          | 01.12.2025 10:00:00 |   Да        |   01.12.2025 10:01:13  |
'''

from datetime import datetime
import gspread_asyncio
from google.oauth2.service_account import Credentials 
from config import GOOGLE_SHEETS_CREDENTIALS_FILE, MAIN_WORK_SHEET_ID, SPREADSHEET_ID
from gspread import exceptions as gExceptions
from loguru import logger
import re

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

# Authorizing credentials
credentials = Credentials.from_service_account_file(
    GOOGLE_SHEETS_CREDENTIALS_FILE, scopes=SCOPES)

# Creating google spreadsheets manager
gc_manager = gspread_asyncio.AsyncioGspreadClientManager(lambda: credentials)       

DENIAL_PATTERN = re.compile(r'нет?|не?|-', re.IGNORECASE)

async def _getAsyncioGspreadWorksheet(gc: gspread_asyncio.AsyncioGspreadClient
) -> gspread_asyncio.AsyncioGspreadWorksheet:
    '''
    Fetch the main worksheet from Google Sheets.
    If the worksheet doesn't exist, logs the error and raises exception.
    '''

    try:
        spreadsheet = await gc.open_by_key(SPREADSHEET_ID)
    except gExceptions.SpreadsheetNotFound:
        logger.error(f"Spreadsheet not found", exc_info=True)
        raise

    try: # try to open the main worksheet
        worksheet = await spreadsheet.get_worksheet(MAIN_WORK_SHEET_ID)
    except gExceptions.WorksheetNotFound:
        logger.error(f"Main worksheet not found", exc_info=True)
        raise

    return worksheet

async def getUnsentMessages() -> list[tuple[int, str, str, str]]:
    '''
    Fetches the rows where F(Статус) column is "Нет" (not sent)
    Returns a list of:
     - Number of row (from 0), where the message is stored
     - chat_id (column B)
     - message (column C)
     - due_date (column E)
    '''

    gc = await gc_manager.authorize()
    worksheet = await _getAsyncioGspreadWorksheet(gc)

    unsent_rows = await _getUnsentRows(worksheet)
    if not unsent_rows:
        return []
    
    rows = await worksheet.batch_get([f'B{i}:E{i}' for i in unsent_rows])

    result = []
    for i, r in zip(unsent_rows, rows):
        del r[0][2] # remove the D column (Отправка)
        result.append((int(i), *r[0]))
    
    return result

async def _getUnsentRows(worksheet: gspread_asyncio.AsyncioGspreadWorksheet) -> list[int]:
    '''
    Fetch the row indicies of unsent messages in the main worksheet.
    '''

    # Get the cells in the F column (Статус) where is_sent status is Fale ("Нет")
    cells = await worksheet.findall(DENIAL_PATTERN, in_column=6)

    # Extract row indices from the cells
    return [cell.row for cell in cells]


async def setMessageAsSent(row_id: int, sent_date: datetime):
    '''
    Marks the message in the given row as sent in the main worksheet and sets the date.
    Args:
     - row_id (int): The row index in the Google Sheets (from 1).
    '''

    gc = await gc_manager.authorize()
    worksheet = await _getAsyncioGspreadWorksheet(gc)
    
    cell_range = 'F{0}:G{0}'.format(row_id)
    values = [['Да', sent_date.strftime('%d.%m.%Y %H:%M:%S')]]

    await worksheet.update(values, cell_range)
