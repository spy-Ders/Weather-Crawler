import requests
from aiofiles import open as aopen
from orjson import dumps, OPT_INDENT_2
from modules import Json
from asyncio import sleep as asleep
# from async_class import AsyncClass

_config = Json.load("config.json")

class crawler():
    def __init__(self, dt, mode):
        self.dt = dt
        self.mode = mode
        return None

    async def crawl(self):
        
        url = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/{self.mode}?Authorization=" + _config["CWB-TOKEN"]
        _data = requests.get(url).json()
        # print(_data)
        # await asleep(1)

        async with aopen(f"results\\{self.dt} {self.mode}__output_.json", mode = "wb") as __file:
            await __file.write(dumps(_data, option=OPT_INDENT_2))
        
        print(f"Captured >>> {self.mode}") 
        return