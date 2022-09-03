from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from anyio import from_thread, to_thread, create_task_group
from os import environ
from riot import RiotRequest
from riot.riot_responses import CurrentGameInfo
from api_responses import User
import logging
import stats
import config
import datetime
import asyncio
import urllib.parse


app = FastAPI()
# log = logging.getLogger(__name__).setLevel(logging.INFO) # logging doesn't work in async funcs
usernames = [("Hide on bush", "kr"), ("Nightblue3", "na1")]


async def fetch_user(server: str, name:str ) -> User:
    global app, log
    riot_req = RiotRequest(config.api_key)
    summoner = await riot_req.summoner_by_name(server, name)

    if summoner:
        # app.logger.info(f"Fetched summoner {server}:{name}")

        results = await asyncio.gather(
            riot_req.entries_by_summoner(server, summoner.id),
            riot_req.activate_game(server, summoner.id),
            return_exceptions=True
        )

        ranked = results[0]
        current_game = results[1]

        if ranked:
            # app.logger.info(f"Fetched summoner ranked {server}:{name}")
            # app.logger.debug(list(map(lambda row: row.miniSeries, ranked)))
            solo = next(filter(lambda row: row.queueType == 'RANKED_SOLO_5x5', ranked), None)
            flex = next(filter(lambda row: row.queueType == 'RANKED_FLEX_SR', ranked), None)
            in_game = current_game.gameId > 0 if current_game else False # may or may not be correct


            if solo:
                solo = await to_thread.run_sync(stats.summary, solo)
            else:
                solo = "Unranked"

            if flex:
                flex = await to_thread.run_sync(stats.summary, flex)
            else:
                flex = "Unranked"

            return User(
                username=summoner.name,
                level=summoner.summonerLevel,
                revisionDate=summoner.revisionDate,
                id=summoner.id,
                solo=solo,
                flex=flex,
                profileIconId=f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/{summoner.profileIconId}.jpg",
                server=server,
                utc=await to_thread.run_sync(datetime.datetime.utcfromtimestamp, summoner.revisionDate / 1000),
                ingame=in_game
            )

    status_code = riot_req.last_failure.status_code if riot_req.last_failure else "unknown"
    # app.logger.error(f"Failed {status_code} fetching summoner/ranked {server}:{name}")

    
async def fetchData():
    global usernames, app, server, name
    # riot_req = RiotRequest(config.api_key)
    return await asyncio.gather(
        *list(map(lambda us: fetch_user(us[1], us[0]), usernames)),
        return_exceptions=True
    )


@app.route('/')
@app.route('/list')  # w/e endpoint u want
async def forcedlist(gg):
    results = await fetchData()
    return JSONResponse(content=jsonable_encoder(results))
