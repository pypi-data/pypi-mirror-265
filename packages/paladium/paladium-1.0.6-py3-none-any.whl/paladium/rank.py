from enum import Enum
import uuid

class Leaderboard(Enum):
    MONEY = 'money'
    JOB_ALCHEMIST = 'job.alchemist'
    JOB_FARMER = 'job.farmer'
    JOB_HUNTER = 'job.hunter'
    JOB_MINER = 'job.miner'
    BOSS = 'boss'
    END = 'end'
    KOTH = 'koth'
    CHORUS = 'chorus'
    EGGHUNT = 'egghunt'

class PlayerRank:
    """
    Represents a faction in the leaderboard.
    """
    def __init__(self, json_data: dict):
        self.boss = json_data.get('boss')
        self.money = json_data.get('money')
        self.job_farmer = json_data.get('job-farmer')
        self.job_miner = json_data.get('job-miner')
        self.job_hunter = json_data.get('job-hunter')
        self.job_alchemist = json_data.get('job-alchemist')
        self.end = json_data.get('end')
        self.koth = json_data.get('koth')
        self.chorus = json_data.get('chorus')
        self.egghunt = json_data.get('egghunt')

    def __str__(self):
        return f'Boss: {self.boss}, Money: {self.money}, Farmer: {self.job_farmer}, Miner: {self.job_miner}, ' + \
                f'Hunter: {self.job_hunter}, Alchemist: {self.job_alchemist}, End: {self.end}, Koth: {self.koth},' + \
                f'Chorus: {self.chorus}, Egghunt: {self.egghunt}'
    
    def get_boss(self) -> int:
        """
        Returns the position in the boss leaderboard.
        """
        return self.boss
    
    def get_money(self) -> int:
        """
        Returns the position in the money leaderboard.
        """
        return self.money
    
    def get_job_farmer(self) -> int:
        """
        Returns the position in the farmer leaderboard.
        """
        return self.job_farmer
    
    def get_job_miner(self) -> int:
        """
        Returns the position in the miner leaderboard.
        """
        return self.job_miner
    
    def get_job_hunter(self) -> int:
        """
        Returns the position in the hunter leaderboard.
        """
        return self.job_hunter
    
    def get_job_alchemist(self) -> int:
        """
        Returns the position in the alchemist leaderboard.
        """
        return self.job_alchemist
    
    def get_end(self) -> int:
        """
        Returns the position in the end leaderboard.
        """
        return self.end
    
    def get_koth(self) -> int:
        """
        Returns the position in the koth leaderboard.
        """
        return self.koth

    def get_chorus(self) -> int:
        """
        Returns the position in the chorus leaderboard.
        """
        return self.chorus
    
    def get_egghunt(self) -> int:
        """
        Returns the position in the egghunt leaderboard.
        """
        return self.egghunt

class PlayerLeaderboard:
    """
    Represents a player in a leaderboard.
    """
    def __init__(self, json_data: dict):
        self.uuid = uuid.UUID(json_data.get('uuid'))
        self.username = json_data.get('username')
        self.faction_name = json_data.get('factionName')
        self.position = json_data.get('position')
        self.value = json_data.get('value')

    def __str__(self):
        return f'{self.username} ({self.faction_name}) - {self.position} - {self.value}'
    
    def get_uuid(self) -> uuid.UUID:
        """
        Returns the UUID of the player.
        """
        return self.uuid
    
    def get_username(self) -> str:
        """
        Returns the username of the player.
        """
        return self.username
    
    def get_faction_name(self) -> str:
        """
        Returns the name of the faction the player is in.
        """
        return self.faction_name
    
    def get_position(self) -> int:
        """
        Returns the player's position in the leaderboard.
        """
        return self.position
    
    def get_value(self) -> int:
        """
        Returns the value in the leaderboard.
        """
        return self.value
