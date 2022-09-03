from os import environ
import dataclasses
import httpx
from anyio import to_thread
from typing import List
from riot.riot_responses import *
from riot.riot_url import RiotUrl


class RiotRequest:
    last_failure = None


    def __init__(self, api_key, session=None):
        self.api_key = api_key
        self.riot_url = RiotUrl(api_key)
        self.session = httpx.AsyncClient() if session is None else session
        if api_key is None or api_key=="":
            raise ValueError("No API key specified!")


    def _load_into_response(self, response_class, data) -> RiotResponseType | None:
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


    async def summoner_by_name(self, server, name) -> SummonerDTO | None:
        endpoint = await to_thread.run_sync(self.riot_url.summoner_by_name, server, name)
        response = await self.session.get(endpoint)

        if response.status_code == httpx.codes.OK:
            return await to_thread.run_sync(self._load_into_response, SummonerDTO, response.json())
        else:
            self.last_failure = response


    async def entries_by_summoner(self, server, summoner_id) -> List[LeagueEntryDTO] | None:
        endpoint = await to_thread.run_sync(self.riot_url.entries_by_summoner, server, summoner_id)
        response = await self.session.get(endpoint)

        if response.status_code == httpx.codes.OK:
            return await to_thread.run_sync(self._load_into_response, LeagueEntryDTO, response.json())
        else:
            self.last_failure = response

    
    async def activate_game(self, server, summoner_id) -> CurrentGameInfo | None:
        endpoint = await to_thread.run_sync(self.riot_url.activate_game, server, summoner_id)
        response = await self.session.get(endpoint)

        if response.status_code == httpx.codes.OK:
            return await to_thread.run_sync(self._load_into_response, CurrentGameInfo, response.json())
        else:
            self.last_failure = response