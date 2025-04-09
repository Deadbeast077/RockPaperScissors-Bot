import os
import logging
import asyncio
import threading
import subprocess
from bot import start_bot

# Set up logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Start the bot directly in a separate process
def start_bot_process():
    logger.info("Starting Telegram Bot as a separate process")
    try:
        # Run the bot script directly
        subprocess.Popen(["python", "bot.py"])
        return "Bot started as a separate process"
    except Exception as e:
        logger.error(f"Error starting bot process: {e}")
        return f"Failed to start bot: {e}"

# Start the bot when this module is imported
bot_status = start_bot_process()

# The app variable is needed for Gunicorn
def app(environ, start_response):
    data = f"Rock Paper Scissors Telegram Bot (@RPLSLBot) - {bot_status}".encode('utf-8')
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return [data]

if __name__ == '__main__':
    # If running directly, just start the bot (no web server)
    logger.info("Starting Telegram Bot directly")
    start_bot()
