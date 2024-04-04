import uuid
from datetime import datetime, timedelta
from typing import List, Dict

class Friend:
    """
    Represents a player's friend.
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def get_name(self) -> str:
        return self.name
    
class PlayerJob:
    """
    Represents a player's job.
    """

    def __init__(self, name: str, level: int, xp: float):
        self.name = name
        self.level = level
        self.xp = xp

    @classmethod
    def from_dict(cls, name: str, job: dict) -> 'PlayerJob':
        """
        Creates a PlayerJob instance from a dictionary.
        """
        return cls(name, job.get('level'), job.get('xp'))

    def __str__(self):
        return f'{self.name} (lvl {self.level})'
    
    def get_name(self) -> str:
        return self.name
    
    def get_level(self) -> int:
        return self.level
    
    def get_xp(self) -> float:
        return self.xp

class Player:
    """
    Represents a player.
    """

    def __init__(self, json_data):
        self.username = json_data.get('username')
        self.uuid = uuid.UUID(json_data.get('uuid'))
        self.faction = json_data.get('faction')
        self.first_join = datetime.fromtimestamp(json_data.get('firstJoin') / 1000)
        self.friends = [Friend(friend) for friend in json_data.get('friends')]
        self.money = json_data.get('money')
        self.time_played = timedelta(minutes=json_data.get('timePlayed'))
        self.jobs = {job: PlayerJob.from_dict(job, json_data.get('jobs').get(job)) for job in json_data.get('jobs')}

    def __str__(self):
        return f'Player: {self.username}, UUID: {self.uuid}, Faction: {self.faction}, Time Played: {self.time_played}'

    @staticmethod
    def from_uuid(id: str) -> 'Player':
        """
        Creates a Player instance from a UUID.
        Raises a ValueError if the UUID format is invalid.
        """
        try:
            uuid.uuid4(id)
        except ValueError:
            raise ValueError("Invalid UUID format")
        return Player(id)

    @staticmethod
    def from_name(name: str) -> 'Player':
        """
        Creates a Player instance from a name.
        """
        return Player(name)

    def get_username(self) -> str:
        """
        Returns the username of the player.
        """
        return self.username
    
    def get_uuid(self) -> uuid:
        """
        Returns the UUID of the player.
        """
        return self.uuid
    
    def get_faction(self) -> str:
        """
        Returns the faction of the player.
        """
        return self.faction
    
    def get_first_join(self) -> datetime:
        """
        Returns the datetime when the player first joined.
        """
        return self.first_join
    
    def get_friends(self) -> List[Friend]:
        """
        Returns a list of friends of the player.
        """
        return self.friends
    
    def get_money(self) -> int:
        """
        Returns the money of the player.
        """
        return self.money
    
    def get_time_played(self) -> timedelta:
        """
        Returns the time played by the player.
        """
        return self.time_played
    
    def get_jobs(self) -> Dict[str, PlayerJob]:
        """
        Returns a dictionary of jobs of the player.
        """
        return self.jobs
