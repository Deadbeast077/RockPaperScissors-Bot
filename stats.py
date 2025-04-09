# In-memory storage for user statistics
user_stats = {}

def get_user_stats(user_id):
    """
    Get the statistics for a user
    
    Args:
        user_id (int): The user's Telegram ID
        
    Returns:
        dict: The user's statistics
    """
    if user_id not in user_stats:
        # Initialize stats for new users
        user_stats[user_id] = {
            'username': 'Player',
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'total_games': 0
        }
    
    return user_stats[user_id]

def update_user_stats(user_id, username, result):
    """
    Update the statistics for a user after a game
    
    Args:
        user_id (int): The user's Telegram ID
        username (str): The user's username or first name
        result (str): The result of the game ('win', 'lose', or 'draw')
    """
    stats = get_user_stats(user_id)
    
    # Update the stats
    stats['username'] = username
    stats['total_games'] += 1
    
    if result == "win":
        stats['wins'] += 1
    elif result == "lose":
        stats['losses'] += 1
    else:
        stats['draws'] += 1
        
    # Calculate win percentage
    if stats['total_games'] > 0:
        stats['win_percentage'] = round((stats['wins'] / stats['total_games']) * 100, 1)
    else:
        stats['win_percentage'] = 0.0
        
    # Update the user stats dictionary
    user_stats[user_id] = stats
