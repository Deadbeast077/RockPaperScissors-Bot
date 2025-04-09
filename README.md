# RockPaperScissors Bot (@RPLSLBot)

A fun Telegram bot that lets users play Rock Paper Scissors with interactive buttons and tracks statistics.

## Features

- Play Rock Paper Scissors with simple button interface
- Track game statistics (wins, losses, draws, streaks)
- Engaging and varied response messages
- Easy to set up and deploy

## Commands

- `/start` - Start the bot and get a welcome message
- `/help` - Show help information and game rules
- `/play` - Start a new game
- `/stats` - View your game statistics
- `/cancel` - Cancel the current game

## Setup Instructions

1. **Create a Telegram Bot**:
   - Start a chat with [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` command
   - Set the name to "RockPaperScissors Bot"
   - Set the username to "@RPLSLBot" (or another available username)
   - Copy the API token provided by BotFather

2. **Set up Environment Variable**:
   - Set the `TELEGRAM_TOKEN` environment variable to your bot token:
     ```
     export TELEGRAM_TOKEN="your_bot_token_here"
     ```

3. **Run the Bot**:
   - Execute `python main.py` to start the bot
   - The bot will run and connect to the Telegram API

## Project Structure

- `bot.py` - Core bot functionality and command handlers
- `game.py` - Rock Paper Scissors game logic
- `stats.py` - User statistics tracking
- `responses.py` - Message templates and response variations
- `main.py` - Entry point for the application

## Requirements

- Python 3.7+
- python-telegram-bot v20.7+

## How to Play

1. Start a chat with your bot on Telegram
2. Send the `/play` command
3. Select Rock, Paper, or Scissors using the inline buttons
4. View your result and play again!
5. Check your stats with the `/stats` command

## Customization

You can customize the bot by modifying the following:
- Response messages in `responses.py` 
- Game logic in `game.py`
- Statistics tracking in `stats.py`

Enjoy playing Rock Paper Scissors with your Telegram bot!