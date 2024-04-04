import requests
from typing import List, Dict
from player import Player
from faction import Faction, FactionLeaderboard
from rank import PlayerRank, Leaderboard, PlayerLeaderboard
import uuid

PALADIUM_API_URL = 'https://api.paladium-pvp.fr/'

class Paladium:
    def __init__(self, key: str = None):
        self.key = key
    
    """
    Represents the Paladium API.
    """
    @staticmethod
    def get_json(url: str) -> dict:
        """
        Fetches JSON data from the specified URL and returns it as a dictionary.
        Raises an exception if the HTTP request fails.
        """
        response = requests.get(f'{PALADIUM_API_URL}{url}')
        response.raise_for_status()
        return response.json()
    
    def get_player(self, username: str) -> 'Player':
        """
        Returns the player with the given username.
        """
        json_data = self.get_json(f'player/profile/{username}')
        return Player(json_data)
    
    def get_faction(self, name: str) -> 'Faction':
        """
        Returns the faction with the given name.
        """
        json_data = self.get_json(f'faction/profile/{name}')
        return Faction(json_data)
    
    def get_faction_leaderboard(self) -> List['FactionLeaderboard']:
        """
        Returns the top players on the faction leaderboard.
        """
        json_data = self.get_json(f'faction/leaderboard')
        return [FactionLeaderboard(faction) for faction in json_data]
    
    def get_player_ranks(self, uuid: uuid.UUID = None, player: Player = None) -> PlayerRank:
        """
        Returns the ranks of the player with the given UUID or Player instance.
        """
        if uuid is None and player is not None:
            uuid = player.get_uuid()

        json_data = self.get_json(f'ranking/position/{uuid}')
        return PlayerRank(json_data)
    
    def get_leaderboard(self, leaderboard: Leaderboard, page: int = 1) -> List[FactionLeaderboard]:
        """
        Returns the leaderboard.
        """
        json_data = self.get_json(f'ranking/leaderboard/{leaderboard.value}/{page}')
        return [PlayerLeaderboard(faction) for faction in json_data]
