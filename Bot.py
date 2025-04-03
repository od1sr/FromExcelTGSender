from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from config import BOT_TOKEN
from Message import Message
from loguru import logger
from datetime import datetime
import re

bot = Bot(BOT_TOKEN)

async def sendMessage(msg: Message):
    """
    This function sends a message to the specified Telegram chat using the aiogram Bot.
    Firstly it checks if the due_date of message is not after currrent moment. If it is then bot doesn't send the message.
    If the message has not been sent yet, it attempts to send the message using the bot's send_message method.
    If an exception occurs it handles it and logs.
    After the message has been sent, it`s being set as that in google sheet.

    Args:
     - msg (Message): The Message object containing the chat_id and message to be sent.

    Returns: None
    """

    if datetime.now() < msg.due_date:
        return
    

    chat = msg.chat 
    message = msg.message

    actual_date = None

    if not msg.is_sent and msg.message:
        try:
            sent_message = await bot.send_message(chat, text=message, parse_mode='markdown')
            actual_date = sent_message.date
        except TelegramBadRequest as e:
            if 'chat not found' in e.message:
                logger.info(f'Chat {chat} not found')
                await msg.markChatAsNotFound()
            else:
                logger.opt(exception=True).error('Failed to send a message')
            return
    else:
        logger.info(f'Message {message} has already been sent')

    try:
        await msg.setAsSent(actual_date)
    except:
        logger.opt(exception=True).error('Failed to set message as sent')