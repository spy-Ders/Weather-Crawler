from modules import generator, Json
import requests
from orjson import loads, dumps, OPT_INDENT_2
from aiofiles import open as aopen

class bot:
    def __init__(self, kwd, dt, msg, img, rk, TOKEN):
        self.kwd = kwd
        self.dt = dt
        self.msg = msg
        self.img = img
        self.rk = rk
        self.TOKEN = TOKEN

    def reply(self):
        
        HEADERS = {'Authorization':f'Bearer {self.TOKEN}','Content-Type':'application/json'}
        
        # if recall official-site qrcode
        if self.img == "official":
            _img = generator(self.dt, "https://www.cwb.gov.tw", (255, 255, 255), (0, 0, 0), f"results\\")
            _img.generate()
            self.img = _img.upload()
        
        elif self.img.startswith("https") or self.img.startswith("www"):
            _img = generator(self.dt, self.img, (255, 255, 255), (0, 0, 0), f"results\\")
            _img.generate()
            self.img = _img.upload()

        if self.img != None:    
            BODY = {
            "replyToken" : self.rk,
            "messages" : [{
                    "type": "text",
                    "text": self.msg
                },
                {
                    "type" : "image", 
                    "originalContentUrl" : self.img,
                    "previewImageUrl" : self.img
                }]
            }
        else:
            BODY = {
            "replyToken" : self.rk,
            "messages" : [{
                    "type": "text",
                    "text": self.msg
                }]
            }

        response = requests.post(url = "https://api.line.me/v2/bot/message/reply", headers=HEADERS,data=dumps(BODY, option=OPT_INDENT_2))
        print(response.text)

    async def kwds_check(self):

        async with aopen("keywords.json", mode="r+", encoding="utf-8") as __kwds:

            _kwds = loads(await __kwds.read())
            for idx in _kwds:

                if _kwds[idx].find(self.kwd) != -1:
                    # global kwds_
                    kwds_ = idx
                    print(f">>>\n{kwds_}\n>>>")
                    return kwds_