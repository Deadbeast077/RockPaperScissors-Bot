import random

# Welcome and help messages
START_MESSAGE = """
Hello, {}! 👋

Welcome to the RockPaperScissors Bot (@RPLSLBot)! 🎮
I'm ready to challenge you to the classic game of Rock, Paper, Scissors.

Type /play to start a game!
Type /help for instructions on how to play.
Type /stats to see your game statistics.
"""

HELP_MESSAGE = """
🎮 *ROCKPAPERSCISSORS BOT* 🎮
(@RPLSLBot)

*Game Rules*:
🪨 Rock crushes Scissors
📄 Paper covers Rock
✂️ Scissors cut Paper

*Commands*:
/play - Start a new game
/stats - View your game statistics
/help - Show this help message
/cancel - Cancel the current game

Have fun playing! 🎉
"""

# Play messages
def play_message():
    messages = [
        "Choose your weapon! Rock, Paper, or Scissors?",
        "Rock, Paper, or Scissors? What's your pick?",
        "Time to choose! What will it be?",
        "Let the battle begin! Choose your move:",
        "Ready? Choose your weapon!",
        "Rock? Paper? Scissors? The choice is yours!",
    ]
    return random.choice(messages)

# Win messages
def get_win_message():
    messages = [
        "Amazing! You've outsmarted me! 🎉",
        "Well played! You're really good at this! 👏",
        "You win this round! 🏆",
        "Victory is yours! 🌟",
        "You're on fire! Great move! 🔥",
        "I bow to your superior skills! 👑",
        "You're a rock-paper-scissors champion! 🥇",
        "Incredible strategy! You won! 🧠",
        "You've got some serious RPS skills! ✨",
        "I need to step up my game! You win! 🎮",
    ]
    return random.choice(messages)

# Lose messages
def get_lose_message():
    messages = [
        "Better luck next time! 🍀",
        "Oops! I got you this time! 😎",
        "Don't worry, you'll get me next round! 💪",
        "I win this one! Want to try again? 🎯",
        "Gotcha! But don't give up! 🌈",
        "Not your round, but keep trying! 🚀",
        "The RPS gods smiled on me this time! ⚡",
        "I've been practicing my RPS skills! 🏋️‍♂️",
        "My victory dance is happening right now! 💃",
        "I win this round! Rematch? 🔄",
    ]
    return random.choice(messages)

# Draw messages
def get_draw_message():
    messages = [
        "Great minds think alike! It's a draw! 🤝",
        "We made the same choice! Let's try again! 🔄",
        "It's a tie! Another round? 🎭",
        "We're evenly matched! It's a draw! 🎯",
        "No winner this time! Let's keep going! 🏁",
        "A perfect standoff! It's a draw! ⚖️",
        "Wow, we're in sync! Draw! 🧩",
        "A draw! The tension builds! 🎬",
        "Neither of us takes the win! Try again? 🎪",
        "Epic minds think alike! It's a tie! 🎪",
    ]
    return random.choice(messages)

# Stats message
def stats_message(stats):
    """
    Generate a formatted message with the user's statistics
    
    Args:
        stats (dict): The user's statistics
        
    Returns:
        str: A formatted message with the statistics
    """
    username = stats.get('username', 'Player')
    wins = stats.get('wins', 0)
    losses = stats.get('losses', 0)
    draws = stats.get('draws', 0)
    total_games = stats.get('total_games', 0)
    win_percentage = stats.get('win_percentage', 0.0)
    current_streak = stats.get('current_streak', 0)
    best_streak = stats.get('best_streak', 0)
    
    message = f"<b>🏆 Stats for {username} 🏆</b>\n\n"
    message += f"Games played: {total_games}\n"
    message += f"Wins: {wins} 🎉\n"
    message += f"Losses: {losses} 😔\n"
    message += f"Draws: {draws} 🤝\n"
    message += f"Win rate: {win_percentage}% 📊\n"
    
    # Add streak information
    if current_streak > 0:
        message += f"Current win streak: {current_streak} 🔥\n"
    
    if best_streak > 0:
        message += f"Best win streak: {best_streak} ⭐\n"
    
    message += "\n"
    
    # Add a fun comment based on stats
    if current_streak >= 3:
        message += "You're on fire! Can you keep the streak going? 🔥"
    elif best_streak >= 5:
        message += "Wow! That best streak is impressive! 🌟"
    elif win_percentage >= 75:
        message += "You're a Rock Paper Scissors master! 👑"
    elif win_percentage >= 50:
        message += "You're doing great! Keep it up! 💪"
    elif win_percentage >= 25:
        message += "Not bad! Practice makes perfect! 🌟"
    else:
        message += "Keep playing to improve your skills! 🚀"
        
    return message
