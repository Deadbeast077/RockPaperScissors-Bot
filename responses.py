import random
import time

# Welcome and help messages with supercool captions
START_MESSAGE = """
<b>🎲 WELCOME TO THE ARENA! 🎲</b>

Hey, {}! 👋 Prepare for the ultimate battle of wits and strategy! 💥

🔥 <b>RockPaperScissors Bot</b> (@RPLSLBot) 🔥
The legendary battleground where legends are forged!

🎮 <b>PLAY MODES:</b>
• Solo - Test your skills against the bot!
• Multiplayer - Challenge your friends in epic group battles!

🛡️ <b>COMMAND YOUR DESTINY:</b>
/play - Enter solo combat against the bot
/multiplayer - Summon friends for an epic group battle
/join - Enter a multiplayer arena in your group
/stats - Reveal your legendary battle record
/wallet - View your coin treasury for betting
/history - Browse your recent battle chronicles
/help - Discover the ancient rules of combat

💰 <b>RICHES AND GLORY:</b>
• Earn coins with each victory
• Bet on multiplayer matches
• Track your epic combat history

<b>ARE YOU READY TO CLAIM VICTORY?</b> ⚔️
"""

HELP_MESSAGE = """
<b>🌟 ULTIMATE ROCK PAPER SCISSORS GUIDE 🌟</b>
(@RPLSLBot)

<b>⚔️ RULES OF ENGAGEMENT:</b>
🪨 <b>ROCK</b> - Crushes scissors with devastating force!
📄 <b>PAPER</b> - Envelops rock in a strategic embrace!
✂️ <b>SCISSORS</b> - Slice through paper with precision!

<b>👑 SOLO COMBAT:</b>
/play - Face the bot in one-on-one combat

<b>🔥 MULTIPLAYER WARFARE:</b>
/multiplayer - Create an epic battle arena
/join - Enter an existing multiplayer battle (starts automatically with 2+ players)
/leave - Withdraw from a multiplayer battle (before it starts)

<b>📊 BATTLE STATISTICS:</b>
/stats - View your own battle record
/stats [username] - View another warrior's battle record
/stats [username] solo - View solo stats only
/stats [username] multiplayer - View multiplayer stats only
• Reply to a player's message with /stats to see their legend

<b>💰 TREASURY AND HISTORY:</b>
/wallet - Check your coin balance for betting
/history - View your recent battle chronicles 

<b>🛡️ SPECIAL FEATURES:</b>
• One-game restriction: Warriors can only battle in one arena at a time
• Quick-join: Players can make choices even without private messaging the bot first
• Betting system: Place wagers on multiplayer battles to win more coins
• Virtual currency: Earn coins in battles - winners get rewards, losers lose bets
• Game history: Track your last 10 epic encounters

<b>🛡️ GENERAL COMMANDS:</b>
/help - Display this sacred scroll of knowledge

<b>MAY FORTUNE FAVOR THE BOLD!</b> 🎭
"""

# Play messages - Supercool edition
def play_message():
    messages = [
        "⚡ CHOOSE YOUR WEAPON OF DESTINY! ⚡ Rock, Paper, or Scissors?",
        "🔥 THE MOMENT OF TRUTH ARRIVES! 🔥 Rock, Paper, or Scissors?",
        "⚔️ READY YOUR ARSENAL! ⚔️ What will you wield in battle?",
        "🌪️ UNLEASH YOUR POWER! 🌪️ Rock, Paper, or Scissors?",
        "💫 THE STARS ALIGN FOR BATTLE! 💫 Make your legendary choice!",
        "⭐ DESTINY AWAITS YOUR COMMAND! ⭐ Rock? Paper? Scissors?",
        "🔮 THE ORACLE AWAITS YOUR DECISION! 🔮 What shall it be?",
        "🏆 CHAMPIONS CHOOSE WISELY! 🏆 Rock, Paper, or Scissors?",
    ]
    return random.choice(messages)

# Win messages - Epic edition
def get_win_message():
    messages = [
        "🏆 GLORIOUS VICTORY! 🏆 Your strategic brilliance knows no bounds!",
        "⚡ LEGENDARY MOVE! ⚡ You've outplayed me with your genius!",
        "🎇 SPECTACULAR TRIUMPH! 🎇 The crowd goes wild for your victory!",
        "🔥 UNSTOPPABLE FORCE! 🔥 Your tactical prowess is beyond compare!",
        "👑 BOW TO THE CHAMPION! 👑 Your mastery of RPS is supreme!",
        "🌟 STELLAR PERFORMANCE! 🌟 You're writing your name in the stars!",
        "🚀 COSMIC VICTORY! 🚀 Your skill transcends the ordinary!",
        "💎 FLAWLESS EXECUTION! 💎 You've claimed victory with style!",
        "⚔️ BATTLE MASTER! ⚔️ Your strategy has conquered the field!",
        "🏅 VICTORY ROYALE! 🏅 The glory of triumph is yours alone!",
    ]
    return random.choice(messages)

# Lose messages - Dramatic edition
def get_lose_message():
    messages = [
        "⚡ THE TIDES OF FATE HAVE TURNED! ⚡ But legends rise from defeat!",
        "🌪️ A TEMPORARY SETBACK! 🌪️ Great warriors learn from every battle!",
        "🔥 DEFEAT TODAY, GLORY TOMORROW! 🔥 Your comeback story begins now!",
        "🛡️ BATTLE LOST, WAR CONTINUES! 🛡️ Your fighting spirit remains unbroken!",
        "⚔️ A WORTHY CONTEST! ⚔️ Even champions face adversity!",
        "🌟 STARS MISALIGNED! 🌟 Fortune is fickle, but skill is forever!",
        "🏹 CLOSE BATTLE! 🏹 Victory was within an arrow's flight!",
        "💫 VALIANT EFFORT! 💫 Your tenacity impresses even in defeat!",
        "🔮 THE PROPHECY AWAITS FULFILLMENT! 🔮 Your time will come!",
        "🏰 STRONGHOLD BREACHED! 🏰 But your kingdom shall rise again!",
    ]
    return random.choice(messages)

# Draw messages - Epic standoff edition
def get_draw_message():
    messages = [
        "⚡ COSMIC FORCES BALANCED! ⚡ Great minds clash in perfect harmony!",
        "🔥 LEGENDARY STANDOFF! 🔥 Two titans locked in eternal battle!",
        "⚔️ EPIC DEADLOCK! ⚔️ Neither warrior yields in this fierce duel!",
        "🌪️ POWERS EQUALIZED! 🌪️ The universe itself holds its breath!",
        "💫 STARS ALIGN IN STALEMATE! 💫 A rare celestial convergence!",
        "⭐ DESTINY PAUSED! ⭐ The scrolls foretold this momentous draw!",
        "🛡️ SHIELDS MATCHED! 🛡️ Your defenses are perfectly aligned!",
        "🏆 GLORY SHARED! 🏆 Champions recognize each other's worth!",
        "🔮 MYSTIC EQUILIBRIUM! 🔮 The ancients speak of such rare events!",
        "🌟 PARALLEL BRILLIANCE! 🌟 Two legends thinking as one!",
    ]
    return random.choice(messages)

# Stats message with epic styling
def format_game_history(history_items):
    """
    Format a player's game history into a readable message
    
    Args:
        history_items (list): List of game history records
        
    Returns:
        str: Formatted history message
    """
    if not history_items:
        return "<i>No battles recorded in the scrolls of history!</i>"
    
    message = ""
    
    for i, game in enumerate(history_items):
        # Convert timestamp to readable format
        timestamp = time.strftime("%d/%m/%Y %H:%M", time.localtime(game.get('timestamp', 0)))
        
        # Get basic game info
        result = game.get('result', '?').upper()
        mode = game.get('mode', 'solo')
        choice = game.get('choice', '?')
        opponent_choice = game.get('opponent_choice', '?')
        opponent = game.get('opponent', 'Bot')
        
        # Determine result emoji
        if result == 'WIN':
            result_emoji = '🌟'
        elif result == 'LOSE':
            result_emoji = '💔'
        else:  # draw
            result_emoji = '⚖️'
        
        # Format entry
        message += f"{i+1}. {timestamp} - {result_emoji} <b>{result}</b> vs {opponent}\n"
        message += f"   Mode: {mode.title()}, Your choice: {choice.title()}, Opponent: {opponent_choice.title()}\n"
        
        # Add betting info if present
        if 'bet' in game:
            bet = game.get('bet', 0)
            currency_change = game.get('currency_change', 0)
            if currency_change > 0:
                message += f"   💰 Bet: {bet} coins, Won: +{currency_change} coins\n"
            elif currency_change < 0:
                message += f"   💰 Bet: {bet} coins, Lost: {currency_change} coins\n"
            else:
                message += f"   💰 Bet: {bet} coins, Result: Draw (no change)\n"
        
        # Add separator except for last item
        if i < len(history_items) - 1:
            message += "   ──────────────\n"
    
    return message

def currency_message(currency):
    """
    Generate a formatted message about the user's virtual currency
    
    Args:
        currency (int): The user's currency balance
        
    Returns:
        str: Formatted currency message
    """
    message = "<b>💰 TREASURE VAULT 💰</b>\n"
    message += f"<b>Current Balance:</b> {currency} coins\n\n"
    
    # Add information about betting
    message += "<b>BETTING MECHANICS:</b>\n"
    message += "• Winners receive their bet plus a share of losers' bets\n"
    message += "• Winners without bets still earn 5 coins\n"
    message += "• Losers forfeit their bet to winners\n"
    message += "• Draws allow players to keep their bets\n\n"
    
    if currency <= 0:
        message += "<i>Your coffers are empty, brave warrior! Keep playing to earn more coins!</i>\n"
    elif currency < 50:
        message += "<i>A modest sum for a budding champion. Victory awaits to fill your coffers!</i>\n"
    elif currency < 200:
        message += "<i>A respectable treasure! Ready for high-stakes battles?</i>\n"
    else:
        message += "<i>A fortune fit for royalty! Your wealth is legendary!</i>\n"
    
    return message

def stats_message(stats, mode=None):
    """
    Generate a formatted message with the user's statistics
    
    Args:
        stats (dict): The user's statistics
        mode (str, optional): Game mode to display specific stats ('solo', 'multiplayer', or None for all)
        
    Returns:
        str: A formatted message with the statistics
    """
    username = stats.get('username', 'Warrior')
    
    # Main header
    message = f"<b>🏆 LEGEND OF {username.upper()} 🏆</b>\n\n"
    
    # Check if we're showing a specific mode or all stats
    if mode and mode in ['solo', 'multiplayer']:
        # Show mode-specific stats
        mode_stats = stats.get(mode, {})
        wins = mode_stats.get('wins', 0)
        losses = mode_stats.get('losses', 0)
        draws = mode_stats.get('draws', 0)
        total_games = mode_stats.get('total_games', 0)
        win_percentage = mode_stats.get('win_percentage', 0.0)
        current_streak = mode_stats.get('current_streak', 0)
        best_streak = mode_stats.get('best_streak', 0)
        
        mode_title = "🎮 SOLO BATTLES" if mode == 'solo' else "🔥 MULTIPLAYER BATTLES"
        message += f"<b>{mode_title}</b>\n"
        
        # Mode-specific stats
        message += f"<b>⚔️ BATTLES FOUGHT:</b> {total_games}\n"
        message += f"<b>🌟 VICTORIES:</b> {wins}\n"
        message += f"<b>💔 DEFEATS:</b> {losses}\n"
        message += f"<b>⚖️ STANDOFFS:</b> {draws}\n"
        message += f"<b>📊 TRIUMPH RATE:</b> {win_percentage}%\n"
        
        # Add streak information with epic styling
        if current_streak > 0:
            message += f"<b>🔥 CURRENT STREAK:</b> {current_streak} (Unstoppable!)\n"
        
        if best_streak > 0:
            message += f"<b>👑 LEGENDARY STREAK:</b> {best_streak}\n"
    else:
        # Get both types of stats
        solo_stats = stats.get('solo', {})
        multi_stats = stats.get('multiplayer', {})
        
        # Solo stats section
        solo_total = solo_stats.get('total_games', 0)
        if solo_total > 0:
            message += f"<b>🎮 SOLO BATTLE RECORD</b>\n"
            message += f"<b>⚔️ BATTLES FOUGHT:</b> {solo_total}\n"
            message += f"<b>🌟 VICTORIES:</b> {solo_stats.get('wins', 0)}\n"
            message += f"<b>💔 DEFEATS:</b> {solo_stats.get('losses', 0)}\n"
            message += f"<b>⚖️ STANDOFFS:</b> {solo_stats.get('draws', 0)}\n"
            message += f"<b>📊 TRIUMPH RATE:</b> {solo_stats.get('win_percentage', 0.0)}%\n"
            
            # Add streak information
            if solo_stats.get('current_streak', 0) > 0:
                message += f"<b>🔥 CURRENT STREAK:</b> {solo_stats.get('current_streak', 0)} (Unstoppable!)\n"
            
            if solo_stats.get('best_streak', 0) > 0:
                message += f"<b>👑 LEGENDARY STREAK:</b> {solo_stats.get('best_streak', 0)}\n"
        
        # Add multiplayer stats section
        multi_total = multi_stats.get('total_games', 0)
        if multi_total > 0:
            # Add a separator if we showed solo stats
            if solo_total > 0:
                message += f"\n<b>━━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
                
            message += f"<b>🔥 MULTIPLAYER BATTLE RECORD</b>\n"
            message += f"<b>⚔️ BATTLES FOUGHT:</b> {multi_total}\n"
            message += f"<b>🌟 VICTORIES:</b> {multi_stats.get('wins', 0)}\n"
            message += f"<b>💔 DEFEATS:</b> {multi_stats.get('losses', 0)}\n"
            message += f"<b>⚖️ STANDOFFS:</b> {multi_stats.get('draws', 0)}\n"
            message += f"<b>📊 TRIUMPH RATE:</b> {multi_stats.get('win_percentage', 0.0)}%\n"
            
            # Add streak information
            if multi_stats.get('current_streak', 0) > 0:
                message += f"<b>🔥 CURRENT STREAK:</b> {multi_stats.get('current_streak', 0)} (Unstoppable!)\n"
            
            if multi_stats.get('best_streak', 0) > 0:
                message += f"<b>👑 LEGENDARY STREAK:</b> {multi_stats.get('best_streak', 0)}\n"
        
        # If neither stats exist, show a message
        if solo_total == 0 and multi_total == 0:
            message += "<b>⚔️ NO BATTLES FOUGHT YET!</b>\n"
            message += "This warrior has yet to prove their mettle in the arena!\n"
    
    message += "\n"
    
    # Get current stats for the epic comment (from most recent section displayed)
    if mode and mode in ['solo', 'multiplayer']:
        mode_stats = stats.get(mode, {})
        comment_streak = mode_stats.get('current_streak', 0)
        comment_best_streak = mode_stats.get('best_streak', 0)
        comment_win_rate = mode_stats.get('win_percentage', 0)
    else:
        # In the default view, use whichever mode has better stats for the comment
        solo_stats = stats.get('solo', {})
        multi_stats = stats.get('multiplayer', {})
        
        # Choose the better streak between solo and multiplayer for the comment
        solo_current = solo_stats.get('current_streak', 0)
        multi_current = multi_stats.get('current_streak', 0)
        comment_streak = max(solo_current, multi_current)
        
        solo_best = solo_stats.get('best_streak', 0)
        multi_best = multi_stats.get('best_streak', 0)
        comment_best_streak = max(solo_best, multi_best)
        
        # Use the better win rate for the comment
        solo_win_rate = solo_stats.get('win_percentage', 0)
        multi_win_rate = multi_stats.get('win_percentage', 0)
        comment_win_rate = max(solo_win_rate, multi_win_rate)
    
    # Add a supercool comment based on stats
    if comment_streak >= 5:
        message += "🌋 <b>GODLIKE!</b> Mere mortals tremble before your power! 🌋"
    elif comment_streak >= 3:
        message += "⚡ <b>DOMINATING!</b> Your enemies fall before your might! ⚡"
    elif comment_best_streak >= 5:
        message += "💫 <b>LEGENDARY STATUS!</b> Bards sing tales of your exploits! 💫"
    elif comment_win_rate >= 75:
        message += "👑 <b>SUPREME TACTICIAN!</b> Your strategic mind has no equal! 👑"
    elif comment_win_rate >= 50:
        message += "🔥 <b>RISING CHAMPION!</b> Your skill grows with each battle! 🔥"
    elif comment_win_rate >= 25:
        message += "⚔️ <b>BATTLE-HARDENED WARRIOR!</b> Experience is forging your legend! ⚔️"
    else:
        message += "🌟 <b>DESTINY AWAITS!</b> Every legend begins with perseverance! 🌟"
    
    # Import the needed functions if this is not the stats for a queried user
    from stats import get_user_currency, get_user_history
    
    # If there's a user_id in the stats, this is the user's own stats
    if 'user_id' in stats:
        user_id = stats['user_id']
        
        # Add currency information
        message += f"\n\n<b>━━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        message += currency_message(get_user_currency(user_id))
        
        # Add game history section
        message += f"\n<b>━━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        message += f"<b>🏹 RECENT BATTLE CHRONICLES 🏹</b>\n\n"
        
        # Get history items limited to 5
        history_items = get_user_history(user_id, limit=5)
        history_text = format_game_history(history_items)
        message += history_text
        
    return message

# Multiplayer game messages
def create_multiplayer_game_message(creator_name):
    return f"""
🔥 <b>MULTIPLAYER ARENA CREATED!</b> 🔥

<b>{creator_name}</b> has opened the gates to an <b>EPIC BATTLE ROYALE!</b>

⚔️ <b>WHO DARES TO ENTER?</b> ⚔️

Use /join to accept the challenge and prove your worth!
    """

def multiplayer_game_status(game):
    players = game.get_players_string()
    
    # Calculate total bets for the game
    total_bets = sum(player_data.get("bet", 0) for player_id, player_data in game.players.items())
    betting_info = f"\n\n💰 <b>TREASURY POOL:</b> {total_bets} coins" if total_bets > 0 else ""
    
    # Calculate timer information for games that aren't started yet
    if not game.started and hasattr(game, 'last_player_join_time') and hasattr(game, 'timer_seconds'):
        import time
        current_time = time.time()
        elapsed_time = current_time - game.last_player_join_time
        remaining_time = max(0, game.timer_seconds - elapsed_time)
        
        # Format the time remaining nicely
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        
        # Add the timer message
        timer_msg = f"\n\n⏱️ <b>ARENA CLOSES IN:</b> {minutes}m {seconds}s if no one joins!"
    else:
        timer_msg = ""
    
    if game.started:
        message = f"""
🏟️ <b>BATTLE IN PROGRESS!</b> 🏟️

<b>WARRIORS IN THE ARENA:</b>
{players}{betting_info}{timer_msg}

<i>The clash of titans intensifies as choices are made...</i>
        """
    else:
        message = f"""
⚔️ <b>WARRIORS ASSEMBLING!</b> ⚔️

<b>CURRENT CHALLENGERS:</b>
{players}{betting_info}{timer_msg}

<i>The battle begins automatically when another player joins!
Use /join to enter the arena!</i>
        """
    
    return message

def multiplayer_result_message(results, game):
    message = f"🏆 <b>BATTLE CONCLUDED!</b> 🏆\n\n"
    
    # Show all player choices and bets
    message += "<b>WARRIOR CHOICES:</b>\n"
    for player_id, choice_data in results["choices"].items():
        player_name = choice_data["name"]
        choice = choice_data["choice"]
        bet_amount = game.players[player_id].get("bet", 0)
        
        if choice == "rock":
            emoji = "🪨"
        elif choice == "paper":
            emoji = "📄"
        else:
            emoji = "✂️"
        
        # Add bet information if any
        bet_info = f" [BET: {bet_amount} coins]" if bet_amount > 0 else ""
        message += f"{player_name}: {choice.upper()} {emoji}{bet_info}\n"
    
    message += "\n"
    
    # Show winners and their winnings
    if results["winners"]:
        winner_names = [game.players[player_id]["name"] for player_id in results["winners"]]
        if len(winner_names) == 1:
            message += f"🌟 <b>CHAMPION OF THE ARENA:</b> {winner_names[0]} 🌟\n"
        else:
            winners_text = ", ".join(winner_names)
            message += f"🌟 <b>VICTORIOUS ALLIANCE:</b> {winners_text} 🌟\n"
        
        # Show betting results if there were any bets
        total_bets = sum(game.players[player_id].get("bet", 0) for player_id in game.players)
        if total_bets > 0:
            message += "\n💰 <b>TREASURY RESULTS:</b>\n"
            
            # Calculate losers' total bets
            loser_bet_total = sum(game.players[loser_id].get("bet", 0) 
                              for loser_id in game.players 
                              if loser_id not in results["winners"] and loser_id not in results["tied"])
            
            # Show each winner and their winnings
            for winner_id in results["winners"]:
                winner_name = game.players[winner_id]["name"]
                winner_bet = game.players[winner_id].get("bet", 0)
                
                if winner_bet > 0:
                    # Calculate their share of the pot based on their bet
                    winner_bet_total = sum(game.players[w_id].get("bet", 0) for w_id in results["winners"])
                    winner_share = winner_bet / winner_bet_total if winner_bet_total > 0 else 0
                    winnings = int(loser_bet_total * winner_share) + 10  # +10 is the base win reward
                    message += f"{winner_name} gains {winnings} coins (bet: {winner_bet})\n"
                else:
                    message += f"{winner_name} gains 5 coins (no bet placed)\n"
            
            # Show losers
            for loser_id in game.players:
                if loser_id not in results["winners"] and loser_id not in results["tied"]:
                    loser_name = game.players[loser_id]["name"]
                    loser_bet = game.players[loser_id].get("bet", 0)
                    if loser_bet > 0:
                        message += f"{loser_name} loses {loser_bet} coins\n"
    
    # Show tied players if any
    if results["tied"] and len(results["tied"]) == len(game.players):
        message += "\n⚖️ <b>COSMIC STANDOFF!</b> All warriors have reached perfect equilibrium! ⚖️"
    elif results["tied"]:
        tied_names = [game.players[player_id]["name"] for player_id in results["tied"]]
        tied_text = ", ".join(tied_names)
        message += f"\n⚖️ <b>BALANCED FORCES:</b> {tied_text} ⚖️"
        
        # Show that tied players keep their bets
        for tied_id in results["tied"]:
            tied_bet = game.players[tied_id].get("bet", 0)
            if tied_bet > 0:
                tied_name = game.players[tied_id]["name"]
                message += f"\n{tied_name} keeps their bet of {tied_bet} coins"
    
    message += "\n\n<i>The arena awaits new challengers! Use /multiplayer to create a new battle.</i>"
    
    return message

def player_already_in_game_message(is_group=False, other_chat_id=None):
    if is_group:
        base_msg = "⚠️ <b>WARRIOR ENGAGED!</b> You're already in a fierce battle! Complete your current duel before seeking new challenges!"
    else:
        base_msg = "⚠️ <b>WARRIOR OCCUPIED!</b> You're already locked in combat! Finish your current battle before beginning anew!"
        
    # If we know which chat the user is already in, add that information
    if other_chat_id:
        base_msg += f"\n\n<i>You are currently in battle in chat ID: {other_chat_id}</i>"
        
    return base_msg

def no_game_in_chat_message():
    return "⚠️ <b>EMPTY ARENA!</b> No battle has been arranged here yet! Use /multiplayer to create an epic showdown!"
    
def player_not_found_message(username=None):
    if username:
        return f"⚠️ <b>WARRIOR UNKNOWN!</b> The legend of {username} has not yet been written in our scrolls. They must battle to create their tale!"
    else:
        return "⚠️ <b>WARRIOR UNKNOWN!</b> No such warrior found in the chronicles of battle!"

def multiple_matches_message(matches):
    message = "⚠️ <b>MULTIPLE HEROES FOUND!</b> The name echoes across many warriors:\n\n"
    for user_id, username in matches:
        message += f"• {username}\n"
    message += "\nPlease specify a more unique name to view their legend!"
    return message

def game_already_exists_message():
    return "⚠️ <b>ARENA OCCUPIED!</b> A battle is already underway! Join with /join or wait for it to conclude!"

def game_started_message():
    return "🔥 <b>LET THE BATTLE COMMENCE!</b> 🔥\n\nBrave warriors, choose your weapons with wisdom and courage!"

def not_enough_players_message():
    return "⚠️ <b>NEED MORE CHALLENGERS!</b> At least 2 brave souls must enter the arena before battle can begin!"

def not_creator_message():
    return "⚠️ <b>UNAUTHORIZED COMMAND!</b> Only the creator of this epic battle can start the contest!"

def successfully_left_message():
    return "🚪 <b>HONORABLE DEPARTURE!</b> You have withdrawn from the battlefield with dignity!"

def not_in_game_message():
    return "⚠️ <b>OUTSIDE THE ARENA!</b> You cannot leave a battle you haven't joined!"

def game_already_started_message():
    return "⚠️ <b>BATTLE UNDERWAY!</b> The clash has already begun - no retreat is possible now!"

def game_timeout_message(creator_name):
    return f"<b>⏰ GAME TIMEOUT! ⏰</b>\n\nNo one joined {creator_name}'s game for 3 minutes, so the arena has closed. Try creating a new game when more players are available!"

def choose_move_message():
    messages = [
        "⚡ <b>MOMENT OF TRUTH!</b> ⚡ Choose your weapon of destiny!",
        "🔥 <b>DESTINY CALLS!</b> 🔥 What power will you unleash?",
        "⚔️ <b>BATTLE PHASE INITIATED!</b> ⚔️ Select your tactical strike!",
        "🌪️ <b>CHOOSE WISELY, WARRIOR!</b> 🌪️ Your fate hangs in the balance!",
        "💫 <b>THE COSMOS WATCHES!</b> 💫 Make your legendary choice!"
    ]
    return random.choice(messages)

def betting_message():
    messages = [
        "💰 <b>PLACE YOUR WAGER!</b> 💰 How many coins will you risk for glory?",
        "💎 <b>TREASURY DECISION!</b> 💎 Stake your fortune on this clash!",
        "🏆 <b>FORTUNE FAVORS THE BOLD!</b> 🏆 What riches will you risk?",
        "⚖️ <b>WEIGH YOUR WEALTH!</b> ⚖️ How much of your treasure will you gamble?",
        "🔮 <b>FATE AND FORTUNE!</b> 🔮 The size of your bet determines your reward!"
    ]
    return random.choice(messages)
