from dataclasses import dataclass
from typing import List


"""
    Mapping from Riot API responses

    Not using pip8 to make mapping more simple

    Where comments do not exist or are empty - it's because
    the Riot API documentation has nothing written
"""


@dataclass
class SummonerDTO:
    accountId: str = None
    """ Encrypted account ID. Max length 56 characters. """
    profileIconId: int = None
    """ ID of the summoner icon associated with the summoner. """
    revisionDate: int = None
    """ Date summoner was last modified specified as epoch milliseconds.
        The following events will update this timestamp: summoner name change, 
        summoner level change, or profile icon change. """
    name: str = None
    """mSummoner name. """
    id: str = None
    """ Encrypted summoner ID. Max length 63 characters. """
    puuid: str = None
    """ Encrypted PUUID. Exact length of 78 characters. """
    summonerLevel: int = None
    """ Summoner level associated with the summoner. """


@dataclass
class MiniSeriesDTO:
    losses: int = None
    progress: str = None
    target: int = None
    wins: int = None


@dataclass
class LeagueEntryDTO:
    leagueId: str = None
    """ """
    summonerId: str = None
    """ Player's encrypted summonerId. """
    summonerName: str = None
    """ """
    queueType: str = None
    """ """
    tier: str = None
    """ """
    rank: str = None
    """ The player's division within a tier. """
    leaguePoints: int = None
    """ """
    wins: int = None
    """ Winning team on Summoners Rift. """
    losses: int = None
    """ Losing team on Summoners Rift. """
    hotStreak: bool = None
    """ """
    veteran: bool = None
    """ """
    freshBlood: bool = None
    """ """
    inactive: bool = None
    """ """
    miniSeries: MiniSeriesDTO = MiniSeriesDTO()
    """ """

@dataclass
class BannedChampion:
    pickturn: int = None
    """ The turn during which the champion was banned """
    championId: int = None
    """ The ID of the banned champion """
    teamId: int = None
    """ The ID of the team that banned the champion """


@dataclass
class Observer:
    encryptionKey: str = None
    """ Key used to decrypt the spectator grid game data for playback """


@dataclass
class Perks:
    perkIds: List[int] = None
    """ IDs of the perks/runes assigned. """
    perkStyle: int = None
    """ Primary runes path """
    perkSubStyle: int = None
    """ Secondary runes path """


@dataclass
class GameCustomizationObject:
    category: str = None
    """ Category identifier for Game Customization """
    content: str = None
    """ Game Customization content  """


@dataclass
class CurrentGameParticipant:
    championId: int = None
    """ The ID of the champion played by this participant """
    perks: Perks = None
    """ Perks/Runes Reforged Information """
    profileIconId: int = None
    """ The ID of the profile icon used by this participant """
    bot: bool = None
    """ Flag indicating whether or not this participant is a bot """
    teamId: int = None
    """ The team ID of this participant, indicating the participant's team """
    summonerName: str = None
    """ The summoner name of this participant """
    summonerId: str = None
    """ The encrypted summoner ID of this participant """
    spell1Id: int = None
    """ The ID of the first summoner spell used by this participant """
    spell2Id: int = None
    """ The ID of the second summoner spell used by this participant """
    gameCustomizationObjects: List[GameCustomizationObject] = None
    """ List of Game Customizations """


@dataclass
class CurrentGameInfo:
    gameId: int = None
    """ The ID of the game """
    gameType: str = None
    """ The game type """
    gameStartTime: int = None
    """ The game start time represented in epoch milliseconds """
    mapId: int = None
    """ The ID of the map """
    gameLength: int = None
    """ The amount of time in seconds that has passed since the game started """
    platformId: str = None
    """ The ID of the platform on which the game is being played """
    gameMode: str = None
    """ The game mode """
    bannedChampions: List[BannedChampion] = None
    """ Banned champion information """
    gameQueueConfigId: int = None
    """ The queue type (queue types are documented on the Game Constants page) """
    observers: Observer = None
    """ The observer information """
    participants: List[CurrentGameParticipant] = None
    """ The participant information """