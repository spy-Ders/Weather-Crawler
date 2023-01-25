from datetime import datetime
import requests
from bs4 import BeautifulSoup
from asyncio import new_event_loop, set_event_loop_policy, WindowsSelectorEventLoopPolicy
from aiofiles import open as aopen
from platform import system

import json
with open('config.json', 'r+', encoding='utf-8') as _file:
    _config = json.load(_file)



_mode = {}

url = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/{_mode}?Authorization=" + _config["TOKEN"]


async def main():

    from orjson import dumps, OPT_INDENT_2

    dt = datetime.now().strftime("%Y%m%d %H-%M-%S")
    _data = requests.get(url).json()

    async with aopen(f"results\\{dt} {_mode}__output.json", mode = "wb") as __file:
        await __file.write(dumps(_data, option=OPT_INDENT_2))

if __name__ == "__main__":
    if system() == "Windows":
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    loop = new_event_loop()
    loop.run_until_complete(main())
    loop.close()

'''
F-C0032-001
F-D0047-001
F-D0047-003
F-D0047-005
F-D0047-007
F-D0047-009
F-D0047-011
F-D0047-013
F-D0047-015
F-D0047-017
F-D0047-019
F-D0047-021
F-D0047-023
F-D0047-025
F-D0047-027
F-D0047-029
F-D0047-031
F-D0047-033
F-D0047-035
F-D0047-037
F-D0047-039
F-D0047-041
F-D0047-043
F-D0047-045
F-D0047-047
F-D0047-049
F-D0047-051
F-D0047-053
F-D0047-055
F-D0047-057
F-D0047-059
F-D0047-061
F-D0047-063
F-D0047-065
F-D0047-067
F-D0047-069
F-D0047-071
F-D0047-073
F-D0047-075
F-D0047-077
F-D0047-079
F-D0047-081
F-D0047-083
F-D0047-085
F-D0047-087
F-D0047-089
F-D0047-091
F-D0047-093
F-A0021-001
F-A0085-002
F-A0085-003
O-A0001-001
O-A0002-001
O-A0003-001
O-A0004-001
O-A0005-001
O-A0006-002
O-B0075-001
O-B0075-002
E-A0014-001
E-A0015-001
E-A0015-002
E-A0016-001
E-A0016-002
C-B0025-001
C-B0027-001
C-B0074-001
C-B0074-002
W-C0033-001
W-C0033-002
W-C0034-005
M-A0085-001
A-B0062-001
A-B0063-001
'''