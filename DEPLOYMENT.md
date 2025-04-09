# Deployment Guide for RockPaperScissors Bot

This guide explains how to deploy your Rock Paper Scissors Telegram Bot on a VPS using the dotenv method for environment variables.

## Prerequisites

- A VPS with Ubuntu/Debian (or similar Linux distribution)
- Python 3.7+ installed
- Git installed
- A Telegram bot token from BotFather

## Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/RockPaperScissors-Bot.git
cd RockPaperScissors-Bot
```

## Step 2: Create a Virtual Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
# Install required packages
pip install python-telegram-bot[job-queue] apscheduler python-dotenv
```

You can also use the requirements listed in dependencies.md:

```bash
pip install "python-telegram-bot[job-queue]>=20.7" apscheduler>=3.10.4 pytz>=2023.3 tzlocal>=5.0.1 python-dotenv>=1.0.0
```

## Step 4: Set Up Environment Variables

Create a .env file based on the .env.example template:

```bash
# Create .env file
cp .env.example .env

# Edit the .env file with your actual token
nano .env
```

Replace the placeholder with your actual Telegram bot token in the .env file:

```
TELEGRAM_TOKEN=your_actual_token_from_botfather
```

## Step 5: Test Run the Bot

```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Run the bot
python main.py
```

If everything works correctly, you should see logs indicating the bot has started.

## Step 6: Set Up as a Systemd Service

Create a systemd service to run the bot as a background service that automatically starts on boot.

```bash
# Copy the service file to systemd directory
sudo cp rockpaperscissors-bot.service /etc/systemd/system/

# Edit the service file to update the paths and username
sudo nano /etc/systemd/system/rockpaperscissors-bot.service
```

Update the service file with your actual username and paths:
- Replace `your_username` with your system username
- Replace `/path/to/RockPaperScissors-Bot` with the actual path
- Replace `/path/to/python3` with the path to your virtual environment's Python (typically `/home/your_username/RockPaperScissors-Bot/venv/bin/python3`)

Enable and start the service:

```bash
# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable rockpaperscissors-bot.service

# Start the service
sudo systemctl start rockpaperscissors-bot.service

# Check the status
sudo systemctl status rockpaperscissors-bot.service
```

## Step 7: Monitor the Logs

To view the bot's logs:

```bash
# View the logs
sudo journalctl -u rockpaperscissors-bot.service

# Follow the logs in real-time
sudo journalctl -u rockpaperscissors-bot.service -f
```

## Troubleshooting

### Bot not starting
- Check the logs: `sudo journalctl -u rockpaperscissors-bot.service`
- Verify your token is correct in the .env file
- Make sure all dependencies are installed
- Check file permissions on the main.py file

### Token issues
- Make sure your .env file is in the correct directory
- Verify the format is exactly: `TELEGRAM_TOKEN=your_token_here` (no quotes needed)
- Try running the bot manually to see detailed error messages

### Restarting the bot after changes
```bash
sudo systemctl restart rockpaperscissors-bot.service
```

## Security Notes

- Never commit your .env file to version control
- Make sure your .env file is readable only by your user: `chmod 600 .env`
- Consider using a dedicated user account for running the bot