from modules import generator, Json
import requests
from orjson import dumps, OPT_INDENT_2

class bot:
    def __init__(self, dt, msg, img, rk, TOKEN):
        self.dt = dt
        self.msg = msg
        self.img = img
        self.rk = rk
        self.TOKEN = TOKEN

    def reply(self):
        
        HEADERS = {'Authorization':f'Bearer {self.TOKEN}','Content-Type':'application/json'}
        
        # if recall official-site qrcode
        if(self.img == "official"):
            _img = generator(self.dt, "https://www.cwb.gov.tw", (255, 255, 255), (0, 0, 0), f"results\\")
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