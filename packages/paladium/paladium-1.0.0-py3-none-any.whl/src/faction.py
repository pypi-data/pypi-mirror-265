import uuid
from datetime import datetime
from enum import Enum

class FactionLevel:
    """
    Represents the level of a factioFn.
    """
    def __init__(self, level: int, xp: int):
        self.level = level
        self.xp = xp

    @classmethod
    def from_dict(cls, level: dict) -> 'FactionLevel':
        """
        Creates a FactionLevel instance from a dictionary.
        """
        return cls(level.get('level'), level.get('xp'))

    def __str__(self):
        return f'Level: {self.level}, XP: {self.xp}'

class FactionEmblem:
    """
    Represents the emblem of a faction.
    """
    def __init__(self, background_color: int, background_id: int, border_color: int, 
                 forced_texture: str, foreground_color: int, foreground_id: int, icon_border_color: int,
                 icon_color: int, icon_id: int):
        self.background_color = background_color
        self.background_id = background_id
        self.border_color = border_color
        self.forced_texture = forced_texture
        self.foreground_color = foreground_color
        self.foreground_id = foreground_id
        self.icon_border_color = icon_border_color
        self.icon_color = icon_color
        self.icon_id = icon_id

    @classmethod
    def from_dict(cls, emblem: dict) -> 'FactionEmblem':
        """
        Creates a FactionEmblem instance from a dictionary.
        """
        return cls(emblem.get('backgroundColor'), emblem.get('backgroundId'), emblem.get('borderColor'),
                   emblem.get('forcedTexture'), emblem.get('foregroundColor'), emblem.get('foregroundId'),
                   emblem.get('iconBorderColor'), emblem.get('iconColor'), emblem.get('iconId'))

class FactionMember:
    """
    Represents a member of a faction.
    """
    def __init__(self, uuid: uuid, username: str, group: str, joined_at: datetime):
        self.uuid = uuid
        self.username = username
        self.group = group
        self.joined_at = joined_at

    @classmethod
    def from_dict(cls, member: dict) -> 'FactionMember':
        """
        Creates a FactionMember instance from a dictionary.
        """
        return cls(member.get('uuid'), member.get('username'), member.get('group'), datetime.fromtimestamp(member.get('joinedAt') / 1000))
    
    def __str__(self):
        """
        Returns a string representation of the faction member (username and group).
        """
        return f'{self.username} ({self.group})'
    
    def get_uuid(self) -> uuid:
        """
        Returns the UUID of the faction member.
        """
        return self.uuid
    
    def get_username(self) -> str:
        """
        Returns the username of the faction member.
        """
        return self.username
    
    def get_group(self) -> str:
        """
        Returns the group of the faction member.
        """
        return self.group
    
    def get_joined_at(self) -> datetime:
        """
        Returns the datetime when the faction member joined.
        """
        return self.joined_at

class Faction:
    def __init__(self, json_data: dict):
        self.uuid = json_data.get('uuid')
        self.name = json_data.get('name')
        self.description = json_data.get('description')
        self.created_at = datetime.fromtimestamp(json_data.get('createdAt') / 1000)
        self.level = FactionLevel.from_dict(json_data.get('level'))
        self.emblem = FactionEmblem.from_dict(json_data.get('emblem'))
        self.players = [FactionMember.from_dict(member) for member in json_data.get('players')]

    @classmethod
    def from_name(cls, name: str) -> 'Faction':
        """
        Creates a Faction instance from a name.
        """
        return cls(name)
    
    def __str__(self):
        return f'Faction: {self.name}, UUID: {self.uuid}, {self.level}'
    
    def get_uuid(self) -> uuid:
        """
        Returns the UUID of the faction.
        """
        return self.uuid
    
    def get_name(self) -> str:
        """
        Returns the name of the faction.
        """
        return self.name
    
    def get_description(self) -> str:
        """
        Returns the description of the faction.
        """
        return self.description
    
    def get_created_at(self) -> datetime:
        """
        Returns the datetime when the faction was created.
        """
        return self.created_at
    
    def get_level(self) -> FactionLevel:
        """
        Returns the level of the faction.
        """
        return self.level
    
    def get_emblem(self) -> FactionEmblem:
        """
        Returns the emblem of the faction.
        """
        return self.emblem
    
    def get_players(self) -> list:
        """
        Returns the list of players in the faction.
        """
        return self.players
    
    def get_player(self, username: str) -> FactionMember:
        """
        Returns the player in the faction with the given username.
        """
        return next((player for player in self.players if player.get_username() == username), None)
    
    def get_player_by_uuid(self, uuid: uuid) -> FactionMember:
        """
        Returns the player in the faction with the given UUID.
        """
        return next((player for player in self.players if player.get_uuid() == uuid), None)
    
    def get_player_count(self) -> int:
        """
        Returns the number of players in the faction.
        """
        return len(self.players)
    
class FactionLeaderboardTrend(Enum):
    """
    Represents the trend of a faction in the leaderboard.
    """
    UPWARD = 'UPWARD'
    DOWNWARD = 'DOWNWARD'
    NONE = 'NONE'

class FactionLeaderboard:
    """
    Represents a faction in the leaderboard.
    """
    def __init__(self, json_data: dict):
        self.name = json_data.get('name')
        self.position = json_data.get('position')
        self.trend = FactionLeaderboardTrend(json_data.get('trend'))
        self.diff = json_data.get('diff')
        self.elo = json_data.get('elo')
        self.emblem = FactionEmblem.from_dict(json_data.get('emblem'))
        
    @classmethod
    def from_name(cls, name: str) -> 'FactionLeaderboard':
        """
        Creates a FactionLeaderboard instance from a name.
        """
        return cls(name)
    
    def __str__(self):
        return f'Faction: {self.name}, Position: {self.position}, Elo: {self.elo}'
    
    def get_name(self) -> str:
        """
        Returns the name of the faction.
        """
        return self.name
    
    def get_position(self) -> int:
        """
        Returns the position of the faction.
        """
        return self.position
    
    def get_trend(self) -> FactionLeaderboardTrend:
        """
        Returns the trend of the faction in the leaderboard.
        """
        return self.trend
    
    def get_diff(self) -> int:
        """
        Returns the difference in the leaderboard position from the previous update.
        """
        return self.diff
    
    def get_elo(self) -> int:
        """
        Returns the Elo count of the faction.
        """
        return self.elo
    
    def get_emblem(self) -> FactionEmblem:
        """
        Returns the emblem of the faction.
        """
        return self.emblem