from __future__ import annotations

__doc__ = '''This is a module that configures the basic Message model.
'''
from pydantic import BaseModel, field_validator
from datetime import datetime
import GoogleSheets as gsh
from loguru import logger
import re

class Message(BaseModel):
    '''Messages are stored in Google Spreadsheet.
    It consists of:
    - RowId (int) - The row in Google Spreadsheet that contains the message (from 1)
    - chat (str) - TG ID or username of the chat to where bot should send messages.
    - message (str) - The message to be sent.
    - due_date (datetime) - The date and time when the message should be sent.
    - is_sent (bool) - whether the message is sent
    '''

    row_id: int
    chat: str
    message: str
    due_date: str
    is_sent: bool

    @field_validator('due_date')
    def validate_due_date(cls, value: str|int) -> datetime:
        if isinstance(value, str):
            try:
                return datetime.strptime(value, '%d.%m.%y %H:%M:%S')
            except:
                return datetime.strptime(value, '%d.%m.%Y %H:%M:%S')
        elif isinstance(value, int):
            return datetime.fromtimestamp(value)

    @field_validator('chat')
    def validate_chat(cls, value: str|int) -> str:
        if isinstance(value, str):
            if value[0] == '-' and value[1:].isdigit(): # -100\d+
                if not value.startswith('-100'):
                    raise ValueError(f'Invalid chat_id: {value}')
                    
                return value
        
            if value.isdigit(): #\d+
                return f'-100{value}'

            chat = re.findall(r'@\w+', value) # nickname
            if chat:
                return chat[0]
            
            # extract chat nickname from url
            chat = re.findall(r'(?:https://)?(?:t\.me/)([\w\d]+)', value)
            if chat:
                return '@' + chat[0]
            
            return f'@{value}'
        
        if isinstance(value, int):
            if value <= 0:
                v = str(value)
                
                if not v.startswith('-100'):
                    raise ValueError(f'Invalid chat_id: {value}')
                
                return v
            
            return f'-100{value}'
        
        raise ValueError(f'Invalid chat: {value}. Must be str or int')

    async def extractUnsentMessages() -> list[Message]:
        unsent_messages = await gsh.getUnsentMessages()

        result = []
        for row_id, chat_id, message, due_date in unsent_messages:
            try:
                result.append(Message(
                    row_id=row_id, chat=chat_id, message=message, due_date=due_date, is_sent=False)
                )
            except Exception as e:
                logger.opt(exception=True).error("Failed to create Message")            
            
        return result
        
    async def setAsSent(self, sent_date: datetime|None):
        self.is_sent = True
        self.due_date = sent_date if sent_date else datetime.now()

        await gsh.setMessageAsSent(self.row_id, self.due_date)

    async def markChatAsNotFound(self):
        await gsh.markChatAsNotFound(self.row_id)

    def __str__(self):
        return f'Message(row_id={self.row_id}, chat_id={self.chat}, message="{self.message}", '\
            f'due_date={self.due_date}, is_sent={self.is_sent})'