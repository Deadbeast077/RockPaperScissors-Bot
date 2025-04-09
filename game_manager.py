import logging
import time
import random
from typing import Dict, List, Optional, Tuple, Set

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MultiplayerGame:
    """Represents a multiplayer game instance in a specific chat"""
    
    def __init__(self, chat_id: int, creator_id: int, creator_name: str):
        self.chat_id = chat_id
        self.creator_id = creator_id
        self.creator_name = creator_name
        self.players: Dict[int, Dict] = {}  # user_id -> {name, choice}
        self.started = False
        self.creation_time = time.time()
        self.start_time = None  # When the game was started
        self.message_id = None  # For updating the game message
        self.group_message_id = None  # For updating status in group
        
    def add_player(self, user_id: int, username: str) -> bool:
        """Add a player to the game. Returns True if player was added."""
        # If game already started, only allow adding players in very specific cases
        if self.started:
            # If player is already in the game but needs to be updated (e.g., they didn't have a username before)
            if user_id in self.players:
                # Update username if provided and different
                if username and self.players[user_id]["name"] != username:
                    self.players[user_id]["name"] = username
                return True
            # We don't allow adding completely new players to started games
            return False
            
        # Game hasn't started yet, add the player
        if user_id not in self.players:
            self.players[user_id] = {
                "name": username,
                "choice": None
            }
            return True
        # Player already exists but we'll count it as success
        return True
            
    def remove_player(self, user_id: int) -> bool:
        """Remove a player from the game. Returns True if player was removed."""
        if user_id in self.players and not self.started:
            del self.players[user_id]
            return True
        return False
            
    def start_game(self) -> bool:
        """Start the game if there are at least 2 players"""
        if len(self.players) >= 2 and not self.started:
            self.started = True
            self.start_time = time.time()
            return True
        return False
            
    def is_timer_expired(self) -> bool:
        """Check if the game timer has expired - always returns False since we removed timers"""
        return False
            
    def make_choice(self, user_id: int, choice: str) -> bool:
        """Record a player's choice. Returns True if all players have made choices."""
        if not self.started or user_id not in self.players:
            return False
            
        self.players[user_id]["choice"] = choice
        
        # Check if all players have made their choices
        return all(player["choice"] is not None for player in self.players.values())
            
    def get_results(self) -> Dict:
        """Calculate and return the results of the game."""
        results = {
            "players": len(self.players),
            "choices": {},
            "winners": [],
            "losers": [],
            "tied": []
        }
        
        # Group players by their choices
        choices = {"rock": [], "paper": [], "scissors": []}
        for player_id, player_data in self.players.items():
            player_choice = player_data["choice"]
            if player_choice:
                choices[player_choice].append(player_id)
                results["choices"][player_id] = {
                    "name": player_data["name"],
                    "choice": player_choice
                }
        
        # Check for a tie (everyone chooses the same)
        if len([c for c in choices.values() if c]) == 1:
            for choice_list in choices.values():
                results["tied"].extend(choice_list)
            return results
        
        # Rock beats scissors
        if choices["rock"] and choices["scissors"]:
            results["winners"].extend(choices["rock"])
            results["losers"].extend(choices["scissors"])
            
        # Paper beats rock
        if choices["paper"] and choices["rock"]:
            results["winners"].extend(choices["paper"])
            results["losers"].extend(choices["rock"])
            
        # Scissors beats paper
        if choices["scissors"] and choices["paper"]:
            results["winners"].extend(choices["scissors"])
            results["losers"].extend(choices["paper"])
            
        # Anyone not in winners or losers is tied
        all_players = set(self.players.keys())
        decided_players = set(results["winners"] + results["losers"])
        results["tied"] = list(all_players - decided_players)
            
        return results

    def get_players_string(self) -> str:
        """Return a formatted string listing all players in the game."""
        if not self.players:
            return "No players have joined yet!"
            
        player_list = []
        for user_id, player_data in self.players.items():
            status = "✓" if self.started and player_data["choice"] else "⏳"
            player_list.append(f"{status} {player_data['name']}")
            
        return "\n".join(player_list)

    def is_expired(self, max_age_seconds: int = 300) -> bool:
        """Check if this game has expired (been inactive too long)"""
        return time.time() - self.creation_time > max_age_seconds


class GameManager:
    """Manages all ongoing games across different chats"""
    
    def __init__(self):
        # Maps chat_id -> game object 
        self.games: Dict[int, MultiplayerGame] = {}
        # Maps user_id -> set of chat_ids (to track which games a user is in)
        self.user_games: Dict[int, Set[int]] = {}
        
    def create_game(self, chat_id: int, user_id: int, username: str) -> Optional[MultiplayerGame]:
        """Create a new game in a chat. Returns the game object or None if creation fails."""
        # If there's already a game in this chat, return None
        if chat_id in self.games:
            logger.warning(f"Game already exists in chat {chat_id}")
            return self.games[chat_id]  # Return existing game instead of None
            
        # End all other games this user might be in
        self.remove_user_from_all_games(user_id)
            
        game = MultiplayerGame(chat_id, user_id, username)
        game.add_player(user_id, username)  # Creator joins automatically
        
        self.games[chat_id] = game
        
        # Track that this user is in this game
        if user_id not in self.user_games:
            self.user_games[user_id] = set()
        self.user_games[user_id].add(chat_id)
        
        return game
        
    def remove_user_from_all_games(self, user_id: int) -> None:
        """Remove a user from all games they're currently in."""
        if user_id not in self.user_games:
            return
            
        # Copy the set to avoid modifying during iteration
        chat_ids = list(self.user_games[user_id])
        
        for chat_id in chat_ids:
            self.leave_game(chat_id, user_id)
        
    def join_game(self, chat_id: int, user_id: int, username: str) -> Tuple[bool, Optional[MultiplayerGame]]:
        """Join an existing game. Returns (success, game)."""
        if chat_id not in self.games:
            return False, None
        
        # First remove user from any other games they might be in
        self.remove_user_from_all_games(user_id)
            
        game = self.games[chat_id]
        success = game.add_player(user_id, username)
        
        if success:
            # Track that this user is in this game
            if user_id not in self.user_games:
                self.user_games[user_id] = set()
            self.user_games[user_id].add(chat_id)
            
        return success, game
        
    def leave_game(self, chat_id: int, user_id: int) -> Tuple[bool, Optional[MultiplayerGame]]:
        """Leave a game. Returns (success, updated_game)."""
        if chat_id not in self.games:
            return False, None
            
        game = self.games[chat_id]
        success = game.remove_player(user_id)
        
        if success:
            # If this was the last player, remove the game
            if not game.players:
                self.end_game(chat_id)
                return success, None
                
            # Remove this chat from user's games
            if user_id in self.user_games:
                self.user_games[user_id].discard(chat_id)
                # Clean up if user has no more games
                if not self.user_games[user_id]:
                    del self.user_games[user_id]
                    
        return success, game
        
    def start_game(self, chat_id: int) -> Tuple[bool, Optional[MultiplayerGame]]:
        """Start a game in a specific chat. Returns (success, game)."""
        if chat_id not in self.games:
            return False, None
            
        game = self.games[chat_id]
        success = game.start_game()
        return success, game
        
    def make_choice(self, chat_id: int, user_id: int, choice: str) -> Tuple[bool, Optional[MultiplayerGame], bool]:
        """
        Record a player's choice. 
        Returns (success, game, all_chosen) where all_chosen indicates if all players have made choices.
        """
        if chat_id not in self.games:
            return False, None, False
            
        game = self.games[chat_id]
        if user_id not in game.players:
            return False, game, False
            
        all_chosen = game.make_choice(user_id, choice)
        return True, game, all_chosen
        
    def get_game(self, chat_id: int) -> Optional[MultiplayerGame]:
        """Get the game for a specific chat."""
        return self.games.get(chat_id)
        
    def end_game(self, chat_id: int) -> bool:
        """End a game and clean up references. Returns success."""
        if chat_id not in self.games:
            return False
            
        # Remove all player references to this game
        game = self.games[chat_id]
        for user_id in game.players:
            if user_id in self.user_games:
                self.user_games[user_id].discard(chat_id)
                # Clean up if user has no more games
                if not self.user_games[user_id]:
                    del self.user_games[user_id]
                    
        # Remove the game
        del self.games[chat_id]
        return True
        
    def is_user_in_game(self, user_id: int, chat_id: Optional[int] = None) -> bool:
        """
        Check if a user is in a game.
        If chat_id is None, checks if user is in any game.
        If chat_id is provided, checks if user is in that specific game.
        """
        if chat_id is None:
            return user_id in self.user_games and bool(self.user_games[user_id])
        
        return (user_id in self.user_games and 
                chat_id in self.user_games[user_id] and
                chat_id in self.games and 
                user_id in self.games[chat_id].players)
                
    def clean_up_expired_games(self, max_age_seconds: int = 300) -> int:
        """Remove expired games. Returns the number of games removed."""
        expired_chats = []
        
        for chat_id, game in self.games.items():
            if game.is_expired(max_age_seconds):
                expired_chats.append(chat_id)
                
        for chat_id in expired_chats:
            self.end_game(chat_id)
            
        return len(expired_chats)


# Singleton instance of the game manager
_game_manager = None

def get_game_manager() -> GameManager:
    """Get the global game manager instance."""
    global _game_manager
    if _game_manager is None:
        _game_manager = GameManager()
    return _game_manager