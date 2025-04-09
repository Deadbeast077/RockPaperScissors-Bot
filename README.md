# ⚔️ RockPaperScissors Bot (@RPLSLBot) ⚔️

An epic Telegram bot that lets users engage in legendary Rock Paper Scissors battles with stunning visuals, interactive buttons, epic multiplayer modes, and detailed statistics tracking!

## ✨ Epic Features

- 🎮 **Solo Combat**: Challenge the bot to test your skills in one-on-one battles!
- 🔥 **Multiplayer Arena**: Create epic group battles and challenge your friends!
- 💰 **Virtual Currency**: Place bets on multiplayer matches to earn more coins!
- 📊 **Battle Statistics**: Track your victories, defeats, and legendary win streaks!
- 🌟 **Epic Messages**: Enjoy dramatic, supercool messages that make every battle feel legendary!
- ⏱️ **Auto-Timeout**: Games automatically end after 3 minutes if no one joins
- 🏆 **Fair Competition**: Everyone gets one game at a time to ensure balanced gameplay
- 🚀 **Group Integration**: Works perfectly in both private chats and group conversations

## 📜 Command Your Destiny

### Solo Commands
- `/start` - Begin your journey and see the welcome message
- `/help` - Discover the sacred rules and commands
- `/play` - Enter solo combat against the bot
- `/stats` - View your legendary battle record (can be used with [username] and [mode])
- `/history` - View your recent battle history
- `/wallet` - Check your virtual currency balance

### Multiplayer Commands
- `/multiplayer` - Create an epic battle arena in your group
- `/join` - Enter an existing multiplayer battle (games auto-start when a second player joins)
- `/leave` - Withdraw from a multiplayer battle (only before the game starts)

## 🛡️ Setup Instructions

1. **Create a Telegram Bot**:
   - Start a chat with [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` command
   - Set the name to "RockPaperScissors Bot"
   - Set the username to a unique username of your choice
   - Copy the API token provided by BotFather

2. **Install Dependencies**:
   - See the [dependencies.md](dependencies.md) file for required packages
   - Install them using pip:
     ```bash
     pip install "python-telegram-bot[job-queue]>=20.7" apscheduler>=3.10.4 pytz>=2023.3 tzlocal>=5.0.1 python-dotenv>=1.0.0
     ```

3. **Set up Environment Variable** (Two Options):

   **Option A: Direct Environment Variable:**
   - Set the `TELEGRAM_TOKEN` environment variable to your bot token:
     ```bash
     # For Linux/macOS
     export TELEGRAM_TOKEN="your_bot_token_here"
     
     # For Windows Command Prompt
     set TELEGRAM_TOKEN=your_bot_token_here
     
     # For Windows PowerShell
     $env:TELEGRAM_TOKEN="your_bot_token_here"
     ```

   **Option B: Using .env File (Recommended):**
   - Install python-dotenv: `pip install python-dotenv`
   - Create a `.env` file in the project root with your token:
     ```
     TELEGRAM_TOKEN=your_bot_token_here
     DEBUG=True
     ```
   - The bot automatically loads this file using python-dotenv
   
   - For deployment on hosting platforms, set this as a secret environment variable or use a .env file

4. **Run the Bot**:
   - Execute `python main.py` to start the bot
   - The bot will run and connect to the Telegram API
   - You should see logs indicating successful connection

## 📁 Project Structure

- `bot.py` - Core bot functionality and command handlers for both solo and multiplayer modes
- `game_manager.py` - Manages multiplayer game instances, player tracking, and results
- `game.py` - Rock Paper Scissors game logic for solo battles
- `stats.py` - User statistics tracking system with streaks
- `responses.py` - Epic message templates and dramatic response variations
- `main.py` - Entry point for the application with process management

## Requirements

- Python 3.7+
- python-telegram-bot v20.7+

## ⚔️ How to Play

### Solo Combat
1. Start a chat with your bot on Telegram
2. Send the `/play` command
3. Select Rock, Paper, or Scissors using the inline buttons
4. View your result and play again!
5. Check your stats with the `/stats` command

### Multiplayer Warfare
1. Add the bot to a Telegram group with your friends
2. Create a new game with `/multiplayer`
3. Have your friends join with `/join` (game starts automatically when a second player joins)
4. Each player will receive a private message to place bets and make their choices
5. Results will be announced in the group chat with epic details and prize distributions!
6. Check your updated stats and wallet with `/stats` and `/wallet`
7. Games automatically time out after 3 minutes if no one joins

## 🧙‍♂️ Customize Your Legend

Shape your own destiny by modifying these aspects of the bot:

- 📜 **Epic Messaging**: Modify or add your own dramatic messages in `responses.py`
- ⚔️ **Battle Mechanics**: Customize game logic in `game.py` and `game_manager.py`
- 📊 **Glory System**: Enhance the statistics system in `stats.py`
- 🎭 **New Features**: Add new game modes or special powers for true legends!

---

### 🌟 PREPARE FOR EPIC BATTLES! 🌟

May your rock crush mightily, your paper envelop strategically, and your scissors cut with precision! Enter the arena, challenge your friends, and forge your legend in the ultimate test of wit and strategy!

*Glory awaits the champions of RockPaperScissors Bot!* ⚔️