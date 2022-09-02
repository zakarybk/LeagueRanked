from dataclasses import dataclass
from datetime import datetime
from riot.riot_responses import LeagueEntryDTO


@dataclass
class User:
    username: str
    level: int
    revisionDate: int
    id: str
    solo: LeagueEntryDTO
    flex: LeagueEntryDTO
    profileIconId: str
    server: str
    utc: datetime
    ingame: bool