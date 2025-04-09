import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    ContextTypes, ConversationHandler
)

from game import play_game, get_result_message
from stats import get_user_stats, update_user_stats
from responses import (
    START_MESSAGE, HELP_MESSAGE, 
    play_message, stats_message,
    get_win_message, get_lose_message, get_draw_message
)

# Get token from environment variable
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")

# Bot Configuration
# Note: When creating the bot in BotFather, set the following:
# - Bot name: RockPaperScissors Bot
# - Bot username: @RPLSLBot

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define states for conversation handler
PLAYING = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        START_MESSAGE.format(user.first_name)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await update.message.reply_text(HELP_MESSAGE)

async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a game when the command /play is issued."""
    keyboard = [
        [
            InlineKeyboardButton("Rock 🪨", callback_data="rock"),
            InlineKeyboardButton("Paper 📄", callback_data="paper"),
            InlineKeyboardButton("Scissors ✂️", callback_data="scissors"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(play_message(), reply_markup=reply_markup)
    return PLAYING

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the button press."""
    query = update.callback_query
    await query.answer()
    
    user_choice = query.data
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    
    # Play the game and get result
    result, bot_choice = play_game(user_choice)
    
    # Update user stats
    update_user_stats(user_id, username, result)
    
    # Generate appropriate response based on result
    if result == "win":
        result_message = get_win_message()
    elif result == "lose":
        result_message = get_lose_message()
    else:
        result_message = get_draw_message()
    
    # Send result message
    result_text = get_result_message(user_choice, bot_choice, result)
    await query.edit_message_text(
        text=f"{result_text}\n\n{result_message}"
    )
    
    # Offer to play again
    keyboard = [
        [
            InlineKeyboardButton("Play Again 🎮", callback_data="play_again"),
            InlineKeyboardButton("Show Stats 📊", callback_data="show_stats"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="What would you like to do next?",
        reply_markup=reply_markup
    )
    return PLAYING

async def play_again_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the play again button."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("Rock 🪨", callback_data="rock"),
            InlineKeyboardButton("Paper 📄", callback_data="paper"),
            InlineKeyboardButton("Scissors ✂️", callback_data="scissors"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=play_message(),
        reply_markup=reply_markup
    )
    return PLAYING

async def show_stats_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the show stats button."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    stats = get_user_stats(user_id)
    
    await query.edit_message_text(
        text=stats_message(stats),
        parse_mode="HTML"
    )
    
    # Offer to play again
    keyboard = [
        [
            InlineKeyboardButton("Play Again 🎮", callback_data="play_again"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ready for another round?",
        reply_markup=reply_markup
    )
    return PLAYING

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user stats when the command /stats is issued."""
    user_id = update.effective_user.id
    stats = get_user_stats(user_id)
    
    await update.message.reply_text(
        stats_message(stats),
        parse_mode="HTML"
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel and end the conversation."""
    await update.message.reply_text("Game cancelled. Type /play to start a new game!")
    return ConversationHandler.END

def create_application():
    """Create the application instance."""
    if not TELEGRAM_TOKEN:
        logger.error("No Telegram token provided. Please set the TELEGRAM_TOKEN environment variable.")
        logger.info("To create a bot, use BotFather in Telegram and set:")
        logger.info("- Bot name: RockPaperScissors Bot")
        logger.info("- Bot username: @RPLSLBot")
        return None
    
    # Create application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add conversation handler for game
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("play", play_command)],
        states={
            PLAYING: [
                CallbackQueryHandler(button_callback, pattern='^(rock|paper|scissors)$'),
                CallbackQueryHandler(play_again_callback, pattern='^play_again$'),
                CallbackQueryHandler(show_stats_callback, pattern='^show_stats$'),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(conv_handler)
    
    return application

def start_bot():
    """Start the bot."""
    # Create the application
    application = create_application()
    if not application:
        return
    
    # Start the Bot
    logger.info("Starting Telegram Bot")
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")

async def start_bot_async():
    """Start the bot asynchronously."""
    # Create the application
    application = create_application()
    if not application:
        return
    
    # Start the Bot asynchronously
    logger.info("Starting Telegram Bot asynchronously")
    try:
        await application.initialize()
        await application.start()
        await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Error starting bot asynchronously: {e}")

if __name__ == "__main__":
    start_bot()
