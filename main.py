import os
import logging
from flask import Flask
from threading import Thread
from bot import start_bot

# Set up logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

@app.route('/')
def home():
    return "RPS Telegram Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Start the bot in a separate thread
    bot_thread = Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Run the Flask app in the main thread
    logger.info("Starting Flask web server")
    run_flask()
