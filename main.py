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

# Use a file lock to ensure only one bot process runs at a time
bot_lock_file = "bot.lock"
bot_process = None

# Start the bot directly in a separate process
def start_bot_process():
    global bot_process
    logger.info("Starting Telegram Bot as a separate process")
    
    # Check if the bot process is already running
    if os.path.exists(bot_lock_file):
        logger.info("Bot is already running (lock file exists)")
        return "Bot is already running"
    
    try:
        # Create lock file
        with open(bot_lock_file, 'w') as f:
            f.write(str(os.getpid()))
        
        # Run the bot script directly
        bot_process = subprocess.Popen(["python", "-c", 
            "from bot import start_bot; start_bot()"])
        return "Bot started as a separate process"
    except Exception as e:
        # Clean up lock file if startup fails
        if os.path.exists(bot_lock_file):
            os.remove(bot_lock_file)
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

# Clean up when the process exits
def cleanup():
    global bot_process
    logger.info("Cleaning up bot process")
    
    # Terminate the bot process if it's running
    if bot_process is not None:
        try:
            bot_process.terminate()
            bot_process.wait(timeout=5)
        except Exception as e:
            logger.error(f"Error terminating bot process: {e}")
    
    # Remove the lock file
    if os.path.exists(bot_lock_file):
        try:
            os.remove(bot_lock_file)
            logger.info("Removed bot lock file")
        except Exception as e:
            logger.error(f"Error removing lock file: {e}")

# Register cleanup on exit
import atexit
atexit.register(cleanup)

# Handle keyboard interrupts
import signal
def signal_handler(sig, frame):
    logger.info("Received signal to shut down")
    cleanup()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    # If running directly, just start the bot (no web server)
    logger.info("Starting Telegram Bot directly")
    try:
        start_bot()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down")
    finally:
        cleanup()
