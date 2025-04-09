import random
import time

# Welcome and help messages with supercool captions
START_MESSAGE = """
*🎲 WELCOME TO THE ARENA! 🎲*

Hey, {}! 👋 Prepare for the ultimate battle of wits and strategy! 💥

🔥 *RockPaperScissors Bot* (@RPLSLBot) 🔥
The legendary battleground where legends are forged!

🎮 *PLAY MODES:*
• Solo - Test your skills against the bot!
• Multiplayer - Challenge your friends in epic group battles!

🛡️ *COMMAND YOUR DESTINY:*
/play - Enter solo combat against the bot
/multiplayer - Summon friends for an epic group battle
/join - Enter a multiplayer arena in your group
/stats - Reveal your legendary battle record
/stats [username] - View another warrior's legend
/help - Discover the ancient rules of combat
/cancel - Retreat from battle (but heroes never quit!)

*ARE YOU READY TO CLAIM VICTORY?* ⚔️
"""

HELP_MESSAGE = """
*🌟 ULTIMATE ROCK PAPER SCISSORS GUIDE 🌟*
(@RPLSLBot)

*⚔️ RULES OF ENGAGEMENT:*
🪨 *ROCK* - Crushes scissors with devastating force!
📄 *PAPER* - Envelops rock in a strategic embrace!
✂️ *SCISSORS* - Slice through paper with precision!

*👑 SOLO COMBAT:*
/play - Face the bot in one-on-one combat

*🔥 MULTIPLAYER WARFARE:*
/multiplayer - Create an epic battle arena
/join - Enter an existing multiplayer battle
/start_game - Begin the multiplayer showdown (creator only)
/leave - Withdraw from a multiplayer battle

*📊 BATTLE STATISTICS:*
/stats - View your own battle record
/stats [username] - View another warrior's battle record
/stats [username] solo - View solo stats only
/stats [username] multiplayer - View multiplayer stats only

*🛡️ SPECIAL FEATURES:*
• One-game restriction: Warriors can only battle in one arena at a time
• Quick-join: Players can make choices even without private messaging the bot first

*🛡️ GENERAL COMMANDS:*
/stats - View your legendary battle record
/help - Display this sacred scroll of knowledge
/cancel - Retreat from the current battle

*MAY FORTUNE FAVOR THE BOLD!* 🎭
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
    else:
        # Show combined stats
        wins = stats.get('wins', 0)
        losses = stats.get('losses', 0)
        draws = stats.get('draws', 0)
        total_games = stats.get('total_games', 0)
        win_percentage = stats.get('win_percentage', 0.0)
        current_streak = stats.get('current_streak', 0)
        best_streak = stats.get('best_streak', 0)
        
        message += f"<b>⚡ COMBINED BATTLE RECORD</b>\n"
    
    # Common stats section
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
    
    # If we're showing all stats, also include the breakdowns
    if not mode:
        solo_stats = stats.get('solo', {})
        multi_stats = stats.get('multiplayer', {})
        
        # Add solo stats summary if played any solo games
        if solo_stats.get('total_games', 0) > 0:
            message += f"\n<b>🎮 SOLO STATS:</b> {solo_stats.get('wins', 0)}W - {solo_stats.get('losses', 0)}L - {solo_stats.get('draws', 0)}D "
            message += f"({solo_stats.get('win_percentage', 0.0)}%)\n"
            
        # Add multiplayer stats summary if played any multiplayer games
        if multi_stats.get('total_games', 0) > 0:
            message += f"<b>👥 MULTIPLAYER STATS:</b> {multi_stats.get('wins', 0)}W - {multi_stats.get('losses', 0)}L - {multi_stats.get('draws', 0)}D "
            message += f"({multi_stats.get('win_percentage', 0.0)}%)\n"
    
    message += "\n"
    
    # Add a supercool comment based on stats
    if current_streak >= 5:
        message += "🌋 <b>GODLIKE!</b> Mere mortals tremble before your power! 🌋"
    elif current_streak >= 3:
        message += "⚡ <b>DOMINATING!</b> Your enemies fall before your might! ⚡"
    elif best_streak >= 5:
        message += "💫 <b>LEGENDARY STATUS!</b> Bards sing tales of your exploits! 💫"
    elif win_percentage >= 75:
        message += "👑 <b>SUPREME TACTICIAN!</b> Your strategic mind has no equal! 👑"
    elif win_percentage >= 50:
        message += "🔥 <b>RISING CHAMPION!</b> Your skill grows with each battle! 🔥"
    elif win_percentage >= 25:
        message += "⚔️ <b>BATTLE-HARDENED WARRIOR!</b> Experience is forging your legend! ⚔️"
    else:
        message += "🌟 <b>DESTINY AWAITS!</b> Every legend begins with perseverance! 🌟"
        
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
    
    if game.started:
        # Calculate remaining time if timer is active
        timer_msg = ""
        if game.timer_seconds > 0 and game.start_time:
            elapsed = time.time() - game.start_time
            remaining = max(0, game.timer_seconds - elapsed)
            
            if remaining > 0:
                minutes = int(remaining) // 60
                seconds = int(remaining) % 60
                
                if minutes > 0:
                    timer_msg = f"\n\n⏱️ <b>TIME REMAINING:</b> {minutes}m {seconds}s ⏱️"
                else:
                    timer_msg = f"\n\n⏱️ <b>TIME REMAINING:</b> {seconds}s ⏱️"
            else:
                timer_msg = "\n\n⏱️ <b>TIME'S ALMOST UP!</b> ⏱️"
        
        message = f"""
🏟️ <b>BATTLE IN PROGRESS!</b> 🏟️

<b>WARRIORS IN THE ARENA:</b>
{players}{timer_msg}

<i>The clash of titans intensifies as choices are made...</i>
        """
    else:
        # Show timer if set
        timer_msg = ""
        if game.timer_seconds > 0:
            minutes = game.timer_seconds // 60
            seconds = game.timer_seconds % 60
            
            if minutes > 0:
                timer_msg = f"\n\n⏱️ <b>BATTLE TIMER:</b> {minutes}m {seconds}s ⏱️"
            else:
                timer_msg = f"\n\n⏱️ <b>BATTLE TIMER:</b> {seconds}s ⏱️"
        
        message = f"""
⚔️ <b>WARRIORS ASSEMBLING!</b> ⚔️

<b>CURRENT CHALLENGERS:</b>
{players}{timer_msg}

<i>The creator can start the battle with /start_game
Others can join with /join</i>
        """
    
    return message

def multiplayer_result_message(results, game):
    message = f"🏆 <b>BATTLE CONCLUDED!</b> 🏆\n\n"
    
    # Show all player choices
    message += "<b>WARRIOR CHOICES:</b>\n"
    for player_id, choice_data in results["choices"].items():
        player_name = choice_data["name"]
        choice = choice_data["choice"]
        
        if choice == "rock":
            emoji = "🪨"
        elif choice == "paper":
            emoji = "📄"
        else:
            emoji = "✂️"
            
        message += f"{player_name}: {choice.upper()} {emoji}\n"
    
    message += "\n"
    
    # Show winners
    if results["winners"]:
        winner_names = [game.players[player_id]["name"] for player_id in results["winners"]]
        if len(winner_names) == 1:
            message += f"🌟 <b>CHAMPION OF THE ARENA:</b> {winner_names[0]} 🌟\n"
        else:
            winners_text = ", ".join(winner_names)
            message += f"🌟 <b>VICTORIOUS ALLIANCE:</b> {winners_text} 🌟\n"
    
    # Show tied players if any
    if results["tied"] and len(results["tied"]) == len(game.players):
        message += "\n⚖️ <b>COSMIC STANDOFF!</b> All warriors have reached perfect equilibrium! ⚖️"
    elif results["tied"]:
        tied_names = [game.players[player_id]["name"] for player_id in results["tied"]]
        tied_text = ", ".join(tied_names)
        message += f"\n⚖️ <b>BALANCED FORCES:</b> {tied_text} ⚖️"
    
    message += "\n\n<i>The arena awaits new challengers! Use /multiplayer to create a new battle.</i>"
    
    return message

def player_already_in_game_message(is_group=False):
    if is_group:
        return "⚠️ <b>WARRIOR ENGAGED!</b> You're already in a fierce battle in this group! Complete your current duel before seeking new challenges!"
    else:
        return "⚠️ <b>WARRIOR OCCUPIED!</b> You're already locked in combat! Finish your current battle before beginning anew!"

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

def choose_move_message():
    messages = [
        "⚡ <b>MOMENT OF TRUTH!</b> ⚡ Choose your weapon of destiny!",
        "🔥 <b>DESTINY CALLS!</b> 🔥 What power will you unleash?",
        "⚔️ <b>BATTLE PHASE INITIATED!</b> ⚔️ Select your tactical strike!",
        "🌪️ <b>CHOOSE WISELY, WARRIOR!</b> 🌪️ Your fate hangs in the balance!",
        "💫 <b>THE COSMOS WATCHES!</b> 💫 Make your legendary choice!"
    ]
    return random.choice(messages)
