import os
import logging
from typing import Dict, Set, Optional, List, Tuple
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    ContextTypes, ConversationHandler, filters
)

from game import play_game, get_result_message
from stats import get_user_stats, update_user_stats, find_user_by_username, get_all_players, user_stats
from game_manager import get_game_manager
from responses import (
    START_MESSAGE, HELP_MESSAGE, 
    play_message, stats_message,
    get_win_message, get_lose_message, get_draw_message,
    create_multiplayer_game_message, multiplayer_game_status, 
    multiplayer_result_message, player_already_in_game_message,
    no_game_in_chat_message, game_already_exists_message,
    game_started_message, not_enough_players_message,
    not_creator_message, successfully_left_message,
    not_in_game_message, game_already_started_message,
    choose_move_message, player_not_found_message, multiple_matches_message
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
MULTIPLAYER_CHOOSING = 2

# Get the game manager
game_manager = get_game_manager()

# Helper functions for multiplayer games
def is_group_chat(update: Update) -> bool:
    """Check if the message is from a group chat."""
    return update.effective_chat.type in ["group", "supergroup"]

async def get_chat_member_count(context: ContextTypes.DEFAULT_TYPE, chat_id: int) -> int:
    """Get the number of members in a chat."""
    try:
        count = await context.bot.get_chat_member_count(chat_id)
        return count
    except Exception as e:
        logger.error(f"Error getting chat member count: {e}")
        return 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        START_MESSAGE.format(user.first_name),
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await update.message.reply_text(HELP_MESSAGE, parse_mode="Markdown")

async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a solo game when the command /play is issued."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # Check if the user is already in a multiplayer game in this chat
    if game_manager.is_user_in_game(user_id, chat_id):
        await update.message.reply_text(
            player_already_in_game_message(is_group=is_group_chat(update)),
            parse_mode="HTML"
        )
        return ConversationHandler.END
        
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
    """Handle the button press for solo game."""
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
    """Handle the play again button for solo game."""
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
    mode = None
    
    # Get the targeted username if provided
    if context.args:
        # User wants to see someone else's stats
        username = ' '.join(context.args)
        
        # Check if they want to see specific mode stats
        if username.lower().endswith(' solo'):
            # Solo mode stats requested
            username = username[:-5].strip()
            mode = 'solo'
        elif username.lower().endswith(' multiplayer'):
            # Multiplayer mode stats requested
            username = username[:-12].strip()
            mode = 'multiplayer'
        
        # Find the user ID from username
        found_user_id, found_username = find_user_by_username(username)
        
        if found_user_id:
            # Check if the username has "(multiple matches found)" suffix
            if "multiple matches found" in found_username:
                # There are multiple matches, find them all
                matches = []
                search_term = username.lower()
                for uid, stats in user_stats.items():
                    stored_username = stats.get('username', '').lower()
                    if search_term in stored_username:
                        matches.append((uid, stats['username']))
                
                # Show the list of matching users
                await update.message.reply_text(
                    multiple_matches_message(matches),
                    parse_mode="HTML"
                )
                return
            
            # Show stats for the found user
            stats = get_user_stats(found_user_id, mode)
            await update.message.reply_text(
                stats_message(stats, mode),
                parse_mode="HTML"
            )
        else:
            # User not found
            await update.message.reply_text(
                player_not_found_message(username),
                parse_mode="HTML"
            )
    else:
        # Show requester's own stats
        stats = get_user_stats(user_id, mode)
        await update.message.reply_text(
            stats_message(stats, mode),
            parse_mode="HTML"
        )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel and end the conversation."""
    await update.message.reply_text("Game cancelled. Type /play to start a new game!")
    return ConversationHandler.END

# Multiplayer game commands
async def multiplayer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create a multiplayer game in a group."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    
    # Check if this is a group chat
    if not is_group_chat(update):
        await update.message.reply_text(
            "⚠️ <b>SOLO WARRIOR!</b> Multiplayer battles can only be arranged in group chats! Invite your friends to a group and challenge them there!",
            parse_mode="HTML"
        )
        return ConversationHandler.END
    
    # Check if there's already a game in this chat
    if game_manager.get_game(chat_id):
        await update.message.reply_text(
            game_already_exists_message(),
            parse_mode="HTML"
        )
        return ConversationHandler.END
    
    # Create a new multiplayer game
    game = game_manager.create_game(chat_id, user_id, username)
    
    # Send the game creation message
    message = await update.message.reply_text(
        create_multiplayer_game_message(username),
        parse_mode="HTML"
    )
    
    # Store the message ID for updates
    if game is not None and message is not None:
        game.message_id = message.message_id
    
    # Send game status
    status_msg = await context.bot.send_message(
        chat_id=chat_id,
        text=multiplayer_game_status(game),
        parse_mode="HTML"
    )
    
    # Store the status message ID for updates
    if game is not None and status_msg is not None:
        game.group_message_id = status_msg.message_id
    
    return ConversationHandler.END

async def join_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Join a multiplayer game."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    
    # Check if there's a game in this chat
    game = game_manager.get_game(chat_id)
    if not game:
        await update.message.reply_text(
            no_game_in_chat_message(),
            parse_mode="HTML"
        )
        return ConversationHandler.END
    
    # Check if the game has already started
    if game.started:
        await update.message.reply_text(
            game_already_started_message(),
            parse_mode="HTML"
        )
        return ConversationHandler.END
    
    # If the user is already in this game, just confirm it
    if game_manager.is_user_in_game(user_id, chat_id):
        await update.message.reply_text(
            f"✓ <b>ALREADY ENLISTED!</b> You're already part of this epic battle, {username}!",
            parse_mode="HTML"
        )
        return ConversationHandler.END
        
    # If the user is in other games, they'll be automatically removed due to the one-game-per-user rule
    if game_manager.is_user_in_game(user_id):
        await update.message.reply_text(
            f"⚠️ <b>ATTENTION WARRIOR!</b> You were in another battle, but have been withdrawn from it to join this epic contest!",
            parse_mode="HTML"
        )
    
    # Join the game
    success, game = game_manager.join_game(chat_id, user_id, username)
    
    if success and game:
        # Send confirmation message
        await update.message.reply_text(
            f"🎭 <b>JOINED THE BATTLE!</b> {username} has entered the arena! Prepare for glory!",
            parse_mode="HTML"
        )
        
        # Auto-start the game if we have at least 2 players
        if len(game.players) >= 2 and not game.started:
            # Start the game automatically
            success, game = game_manager.start_game(chat_id)
            
            if success:
                # Notify that the game has started
                status_msg = await update.message.reply_text(
                    game_started_message(),
                    parse_mode="HTML"
                )
                
                # Store the status message ID
                if game is not None and status_msg is not None:
                    game.group_message_id = status_msg.message_id
                
                # Send individual messages to each player to make their choices
                for player_id, player_data in game.players.items():
                    keyboard = [
                        [
                            InlineKeyboardButton("Rock 🪨", callback_data=f"mp_rock_{chat_id}"),
                            InlineKeyboardButton("Paper 📄", callback_data=f"mp_paper_{chat_id}"),
                            InlineKeyboardButton("Scissors ✂️", callback_data=f"mp_scissors_{chat_id}"),
                        ]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    
                    try:
                        await context.bot.send_message(
                            chat_id=player_id,
                            text=choose_move_message(),
                            reply_markup=reply_markup,
                            parse_mode="HTML"
                        )
                    except Exception as e:
                        logger.error(f"Error sending message to player {player_id}: {e}")
                        # Let the group know that a player might not have received their choice buttons
                        await context.bot.send_message(
                            chat_id=chat_id,
                            text=f"⚠️ <b>WARNING:</b> Could not send choice message to {player_data['name']}. They may need to start the bot in private chat first.",
                            parse_mode="HTML"
                        )
                
                # Send updated game status
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=multiplayer_game_status(game),
                    parse_mode="HTML"
                )
            return ConversationHandler.END
                
        # If the game didn't auto-start, just update status
        try:
            if game is not None and hasattr(game, 'group_message_id') and game.group_message_id:
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=game.group_message_id,
                    text=multiplayer_game_status(game),
                    parse_mode="HTML"
                )
            else:
                status_msg = await context.bot.send_message(
                    chat_id=chat_id,
                    text=multiplayer_game_status(game),
                    parse_mode="HTML"
                )
                if game is not None and status_msg is not None:
                    game.group_message_id = status_msg.message_id
        except Exception as e:
            logger.error(f"Error updating game status: {e}")
            # If editing fails, send a new message
            await context.bot.send_message(
                chat_id=chat_id,
                text=multiplayer_game_status(game),
                parse_mode="HTML"
            )
    
    return ConversationHandler.END

async def start_game_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a multiplayer game."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # Check if there's a game in this chat
    game = game_manager.get_game(chat_id)
    if not game:
        await update.message.reply_text(
            no_game_in_chat_message(),
            parse_mode="HTML"
        )
        return ConversationHandler.END
    
    # Check if the user is the creator
    if game.creator_id != user_id:
        await update.message.reply_text(
            not_creator_message(),
            parse_mode="HTML"
        )
        return ConversationHandler.END
    
    # Check if there are enough players
    if len(game.players) < 2:
        await update.message.reply_text(
            not_enough_players_message(),
            parse_mode="HTML"
        )
        return ConversationHandler.END
    
    # Start the game
    success, _ = game_manager.start_game(chat_id)
    
    if success:
        # Notify that the game has started
        status_msg = await update.message.reply_text(
            game_started_message(),
            parse_mode="HTML"
        )
        
        # Store the status message ID
        if game is not None and status_msg is not None:
            game.group_message_id = status_msg.message_id
        
        # Send individual messages to each player to make their choices
        for player_id, player_data in game.players.items():
            keyboard = [
                [
                    InlineKeyboardButton("Rock 🪨", callback_data=f"mp_rock_{chat_id}"),
                    InlineKeyboardButton("Paper 📄", callback_data=f"mp_paper_{chat_id}"),
                    InlineKeyboardButton("Scissors ✂️", callback_data=f"mp_scissors_{chat_id}"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            try:
                await context.bot.send_message(
                    chat_id=player_id,
                    text=choose_move_message(),
                    reply_markup=reply_markup,
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Error sending message to player {player_id}: {e}")
                # Let the group know that a player might not have received their choice buttons
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"⚠️ <b>WARNING:</b> Could not send choice message to {player_data['name']}. They may need to start the bot in private chat first.",
                    parse_mode="HTML"
                )
        
        # Send updated game status
        await context.bot.send_message(
            chat_id=chat_id,
            text=multiplayer_game_status(game),
            parse_mode="HTML"
        )
    
    return ConversationHandler.END

async def leave_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Leave a multiplayer game."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # Check if there's a game in this chat
    game = game_manager.get_game(chat_id)
    if not game:
        await update.message.reply_text(
            no_game_in_chat_message(),
            parse_mode="HTML"
        )
        return ConversationHandler.END
    
    # Check if the user is in the game
    if not game_manager.is_user_in_game(user_id, chat_id):
        await update.message.reply_text(
            not_in_game_message(),
            parse_mode="HTML"
        )
        return ConversationHandler.END
    
    # Check if the game has already started
    if game.started:
        await update.message.reply_text(
            game_already_started_message(),
            parse_mode="HTML"
        )
        return ConversationHandler.END
    
    # Leave the game
    success, updated_game = game_manager.leave_game(chat_id, user_id)
    
    if success:
        await update.message.reply_text(
            successfully_left_message(),
            parse_mode="HTML"
        )
        
        # If the game still exists (not all players left), send updated status
        if updated_game:
            await context.bot.send_message(
                chat_id=chat_id,
                text=multiplayer_game_status(updated_game),
                parse_mode="HTML"
            )
    
    return ConversationHandler.END

async def multiplayer_choice_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle multiplayer game choices."""
    query = update.callback_query
    await query.answer()
    
    # Parse the callback data: mp_{choice}_{chat_id}
    parts = query.data.split('_')
    if len(parts) != 3:
        return
        
    choice = parts[1]
    chat_id = int(parts[2])
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    
    # Check if there's a game in this chat
    game = game_manager.get_game(chat_id)
    if not game or not game.started:
        await query.edit_message_text(
            "⚠️ <b>GAME NOT FOUND!</b> This battle no longer exists or hasn't started yet!",
            parse_mode="HTML"
        )
        return
    
    # Check if the user is in the game - if not, try to join them (handle bot not started in private)
    if not game_manager.is_user_in_game(user_id, chat_id):
        # Try to add user to player list (game already started)
        if user_id in game.players:
            # User exists but maybe wasn't properly tracked
            if user_id not in game_manager.user_games:
                game_manager.user_games[user_id] = set([chat_id])
            else:
                game_manager.user_games[user_id].add(chat_id)
        else:
            # User not in this game at all - they can't join now
            await query.edit_message_text(
                "⚠️ <b>NOT IN BATTLE!</b> You are not part of this epic contest!",
                parse_mode="HTML"
            )
            return
    
    # We removed timer expiry logic since we're eliminating timers
    # Timer check is now a no-op that always returns false due to our changes
    
    # Record the player's choice
    success, game, all_chosen = game_manager.make_choice(chat_id, user_id, choice)
    
    if success:
        # Confirm the choice to the player
        await query.edit_message_text(
            f"<b>CHOICE LOCKED IN!</b> You selected <b>{choice.upper()}</b>!\n\nYour fate is now in the hands of the gods... 🔮",
            parse_mode="HTML"
        )
        
        # If all players have made their choices, calculate and announce results
        if all_chosen and game:
            # Get the results
            results = game.get_results()
            
            # Send the results to the group chat
            await context.bot.send_message(
                chat_id=chat_id,
                text=multiplayer_result_message(results, game),
                parse_mode="HTML"
            )
            
            # Update stats for all players
            for player_id in game.players:
                username = game.players[player_id]["name"]
                result = "win" if player_id in results["winners"] else "lose"
                if player_id in results["tied"]:
                    result = "draw"
                update_user_stats(player_id, username, result)
            
            # End the game
            game_manager.end_game(chat_id)
        else:
            # Update the game status in the group by editing the status message
            try:
                if game is not None and hasattr(game, 'group_message_id') and game.group_message_id:
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=game.group_message_id,
                        text=multiplayer_game_status(game),
                        parse_mode="HTML"
                    )
                else:
                    # If no stored message ID, send a new message
                    status_msg = await context.bot.send_message(
                        chat_id=chat_id,
                        text=multiplayer_game_status(game),
                        parse_mode="HTML"
                    )
                    if game is not None and status_msg is not None:
                        game.group_message_id = status_msg.message_id
            except Exception as e:
                logger.error(f"Error updating game status: {e}")
                # If editing fails, send a new message
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=multiplayer_game_status(game),
                    parse_mode="HTML"
                )
    
    return

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
    
    # Add conversation handler for solo game
    solo_game_handler = ConversationHandler(
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
    
    # Add command handlers for core functionality
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(solo_game_handler)
    
    # Add multiplayer game command handlers
    application.add_handler(CommandHandler("multiplayer", multiplayer_command))
    application.add_handler(CommandHandler("join", join_command))
    application.add_handler(CommandHandler("start_game", start_game_command))
    application.add_handler(CommandHandler("leave", leave_command))
    
    # Add multiplayer game callback handler
    application.add_handler(CallbackQueryHandler(multiplayer_choice_callback, pattern='^mp_'))
    
    # Clean up expired games every minute
    # This would be done with job queue in a production bot
    
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