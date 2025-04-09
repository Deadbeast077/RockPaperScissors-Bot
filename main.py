import os
import logging
from bot import start_bot

# Set up logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# The app variable is needed for Gunicorn
def app(environ, start_response):
    data = b"Rock Paper Scissors Telegram Bot"
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return [data]

if __name__ == '__main__':
    # Start the bot
    logger.info("Starting Telegram Bot")
    start_bot()
