# In-memory storage for user statistics and username mapping
user_stats = {}
username_to_id = {}  # Map usernames to user IDs for lookup

def get_user_stats(user_id, mode=None):
    """
    Get the statistics for a user
    
    Args:
        user_id (int): The user's Telegram ID
        mode (str, optional): The game mode to get stats for ('solo', 'multiplayer', or None for combined)
        
    Returns:
        dict: The user's statistics
    """
    if user_id not in user_stats:
        # Initialize stats for new users
        user_stats[user_id] = {
            'username': 'Player',
            'user_id': user_id,  # Store the user_id in the stats for reference
            # Combined stats
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'total_games': 0,
            'current_streak': 0,
            'best_streak': 0,
            'last_result': None,
            # Solo mode stats
            'solo': {
                'wins': 0,
                'losses': 0,
                'draws': 0,
                'total_games': 0,
                'current_streak': 0,
                'best_streak': 0,
                'last_result': None,
                'win_percentage': 0.0
            },
            # Multiplayer mode stats
            'multiplayer': {
                'wins': 0,
                'losses': 0,
                'draws': 0,
                'total_games': 0,
                'current_streak': 0,
                'best_streak': 0,
                'last_result': None,
                'win_percentage': 0.0
            }
        }
    
    if mode and mode in ['solo', 'multiplayer']:
        # Return mode-specific stats
        return user_stats[user_id][mode]
    else:
        # Return combined stats
        return user_stats[user_id]

def find_user_by_username(username):
    """
    Find a user ID by their username or part of their username
    
    Args:
        username (str): The username to search for
        
    Returns:
        tuple: (user_id, username) if found, otherwise (None, None)
    """
    username = username.lower().strip('@')  # Normalize username and remove @ if present
    
    # Check for exact match first
    if username in username_to_id:
        user_id = username_to_id[username]
        return user_id, user_stats[user_id]['username']
    
    # Check for partial matches
    partial_matches = []
    for user_id, stats in user_stats.items():
        stored_username = stats.get('username', '').lower()
        if username in stored_username:
            partial_matches.append((user_id, stats['username']))
    
    if len(partial_matches) == 1:
        # Return the only match
        return partial_matches[0]
    elif len(partial_matches) > 1:
        # Multiple matches found, return the first one with a note
        # We'll handle this in the calling function
        return partial_matches[0][0], partial_matches[0][1] + " (multiple matches found)"
    
    # No matches found
    return None, None

def get_all_players():
    """
    Get a list of all players who have played the game
    
    Returns:
        list: List of (user_id, username) tuples
    """
    return [(user_id, stats['username']) for user_id, stats in user_stats.items()]

def update_user_stats(user_id, username, result, mode='solo'):
    """
    Update the statistics for a user after a game
    
    Args:
        user_id (int): The user's Telegram ID
        username (str): The user's username or first name
        result (str): The result of the game ('win', 'lose', or 'draw')
        mode (str): The game mode ('solo' or 'multiplayer')
    """
    # Make sure the mode is valid
    if mode not in ['solo', 'multiplayer']:
        mode = 'solo'  # Default to solo mode if invalid
    
    # Get the user's overall stats
    stats = get_user_stats(user_id)
    
    # Get the mode-specific stats
    mode_stats = stats[mode]
    
    # Update the username
    stats['username'] = username
    
    # Update username to ID mapping for user lookup
    if username and username.strip():
        username_clean = username.lower().strip('@')
        username_to_id[username_clean] = user_id
    
    # Update the overall stats
    stats['total_games'] += 1
    
    # Update the mode-specific stats
    mode_stats['total_games'] += 1
    
    # Update result counts for both overall and mode-specific
    if result == "win":
        stats['wins'] += 1
        mode_stats['wins'] += 1
    elif result == "lose":
        stats['losses'] += 1
        mode_stats['losses'] += 1
    else:  # draw
        stats['draws'] += 1
        mode_stats['draws'] += 1
    
    # Update streak information for overall stats
    if result == "win":
        if stats['last_result'] == "win":
            stats['current_streak'] += 1
        else:
            stats['current_streak'] = 1
            
        # Update best streak if current is better
        if stats['current_streak'] > stats['best_streak']:
            stats['best_streak'] = stats['current_streak']
    else:
        # Reset streak on non-wins
        stats['current_streak'] = 0
    
    # Update streak information for mode-specific stats
    if result == "win":
        if mode_stats['last_result'] == "win":
            mode_stats['current_streak'] += 1
        else:
            mode_stats['current_streak'] = 1
            
        # Update best streak if current is better
        if mode_stats['current_streak'] > mode_stats['best_streak']:
            mode_stats['best_streak'] = mode_stats['current_streak']
    else:
        # Reset streak on non-wins
        mode_stats['current_streak'] = 0
        
    # Store the last result for both
    stats['last_result'] = result
    mode_stats['last_result'] = result
        
    # Calculate win percentage for overall stats
    if stats['total_games'] > 0:
        stats['win_percentage'] = round((stats['wins'] / stats['total_games']) * 100, 1)
    else:
        stats['win_percentage'] = 0.0
        
    # Calculate win percentage for mode-specific stats
    if mode_stats['total_games'] > 0:
        mode_stats['win_percentage'] = round((mode_stats['wins'] / mode_stats['total_games']) * 100, 1)
    else:
        mode_stats['win_percentage'] = 0.0
        
    # Update the user stats dictionary
    user_stats[user_id] = stats
