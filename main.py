from Bot import sendMessage
from Message import Message
import asyncio
from loguru import logger
import sys
import signal

# Configure loguru to log to both console and file
logger.remove()  # This removes the default handler
logger.add(sys.stdout, format="{time} {level} {message}", level='DEBUG')

# set logging into file, size-limited to 10 MB (loguru will create a new file after reaching it)
# when the number of log files exceeds 10, the old one will be removed
logger.add("logs/log.log", format="{time} {level} {message}", level='WARNING', 
    rotation="10 MB", retention=10)
logger.bind(traceback=True)

def signal_handler(sig, frame):
    logger.info("Ctrl+C pressed. Exiting gracefully...")
    sys.exit(0)


async def main():
    while True:
        try:
            unsent_messages = await Message.extractUnsentMessages()
        except KeyboardInterrupt:
            break
        except:
            logger.opt(exception=True).error('Failed to extract unsent messages')
            continue
        
        logger.info(f'{len(unsent_messages)} new messages')

        # Send messages
        for msg in unsent_messages:
            try:
                await sendMessage(msg)
            except KeyboardInterrupt:
                break
            except:
                logger.opt(exception=True).error(f'Failed to send message {msg}')

        await asyncio.sleep(15)  # wait before checking again

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    asyncio.run(main())