import random

def play_game(user_choice):
    """
    Play a round of Rock Paper Scissors
    
    Args:
        user_choice (str): The user's choice ('rock', 'paper', or 'scissors')
        
    Returns:
        tuple: (result, bot_choice) where result is 'win', 'lose', or 'draw'
    """
    choices = ['rock', 'paper', 'scissors']
    bot_choice = random.choice(choices)
    
    # Determine the result
    if user_choice == bot_choice:
        result = "draw"
    elif (
        (user_choice == 'rock' and bot_choice == 'scissors') or
        (user_choice == 'paper' and bot_choice == 'rock') or
        (user_choice == 'scissors' and bot_choice == 'paper')
    ):
        result = "win"
    else:
        result = "lose"
        
    return result, bot_choice

def get_result_message(user_choice, bot_choice, result):
    """
    Generate a message describing the game result
    
    Args:
        user_choice (str): The user's choice
        bot_choice (str): The bot's choice
        result (str): The result of the game ('win', 'lose', or 'draw')
        
    Returns:
        str: A message describing the result
    """
    # Convert choices to emojis for display
    choice_emojis = {
        'rock': '🪨',
        'paper': '📄',
        'scissors': '✂️'
    }
    
    user_emoji = choice_emojis.get(user_choice, '')
    bot_emoji = choice_emojis.get(bot_choice, '')
    
    # Create the message
    message = f"You chose {user_choice} {user_emoji}\n"
    message += f"Bot chose {bot_choice} {bot_emoji}\n\n"
    
    if result == "win":
        message += "🎉 You win! 🎉"
    elif result == "lose":
        message += "😔 You lose! Better luck next time!"
    else:
        message += "🤝 It's a draw! 🤝"
        
    return message
