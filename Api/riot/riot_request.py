from os import environ
import dataclasses
import requests
from typing import List
from riot.riot_responses import *
from riot.riot_url import RiotUrl


class RiotRequest:
    last_failure = None


    def __init__(self, api_key, session=requests):
        self.api_key = api_key
        self.riot_url = RiotUrl(api_key)
        self.session = session
        if api_key is None or api_key=="":
            raise ValueError("No API key specified!")


    def _load_into_response(self, response_class, data):
        if isinstance(data, list):
            fn = lambda row: self._load_into_response(response_class, row)
            return list(map(fn, data))

        kwargs = {}
        for field in dataclasses.fields(response_class):
            if dataclasses.is_dataclass(field.type):
                kwargs[field.name] = self._load_into_response(field.type, data.get(field.name, {}))
            else:
                kwargs[field.name] = data.get(field.name, field.default)
        return response_class(**kwargs)


    def summoner_by_name(self, server, name) -> SummonerDTO:
        endpoint = self.riot_url.summoner_by_name(server, name)
        response = self.session.get(endpoint)

        if response.status_code == self.session.codes.ok:
            return self._load_into_response(SummonerDTO, response.json())
        else:
            self.last_failure = response


    def entries_by_summoner(self, server, summoner_id) -> List[LeagueEntryDTO]:
        endpoint = self.riot_url.entries_by_summoner(server, summoner_id)
        response = self.session.get(endpoint)

        if response.status_code == self.session.codes.ok:
            return self._load_into_response(LeagueEntryDTO, response.json())
        else:
            self.last_failure = response

    
    def activate_game(self, server, summoner_id) -> CurrentGameInfo:
        endpoint = self.riot_url.activate_game(server, summoner_id)
        response = self.session.get(endpoint)

        if response.status_code == self.session.codes.ok:
            return self._load_into_response(CurrentGameInfo, response.json())
        else:
            self.last_failure = response