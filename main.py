from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from asyncio import new_event_loop, set_event_loop_policy, WindowsSelectorEventLoopPolicy
from aiofiles import open as aopen
from platform import system

from flask_ngrok import run_with_ngrok
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler

from orjson import loads, dumps, OPT_INDENT_2

from modules import Json, generator

_config = Json.load("config.json")
cwb_URL = "https://www.cwb.gov.tw"

app = Flask(__name__)
line_bot_api = LineBotApi(_config["BOT-TOKEN"])
handler = WebhookHandler(_config["BOT-SECRET"])
dt = datetime.now().strftime("%Y%m%d %H-%M-%S")

async def kwds_check(msg):

    async with aopen("keywords.json", mode="r+", encoding="utf-8") as __kwds:

        _kwds = loads(await __kwds.read())
        for idx in _kwds:

            if _kwds[idx].find(msg) != -1:
                global kwds_
                kwds_ = idx
                print(f">>>\n{kwds_}\n>>>")
                return

def reply(msg, img, rk, TOKEN):
    
    HEADERS = {'Authorization':f'Bearer {TOKEN}','Content-Type':'application/json'}
    
    # if recall official-site qrcode
    if(img == "official"):
        _img = generator(dt, "https://www.cwb.gov.tw", (255, 255, 255), (0, 0, 0), f"results\\")
        _img.generate()
        img = _img.upload()
        
    BODY = {
    "replyToken" : rk,
    "messages" : [{
            "type": "text",
            "text": msg
        },
        {
            "type" : "image", 
            "originalContentUrl" : img,
            "previewImageUrl" : img
        }]
    }
    
    response = requests.post(url = "https://api.line.me/v2/bot/message/reply", headers=HEADERS,data=dumps(BODY, option=OPT_INDENT_2))
    print(response.text)

async def crawler(_mode):
    
    url = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/{_mode}?Authorization=" + _config["CWB-TOKEN"]
    _data = requests.get(url).json()
    print(f"Captured >>> {_mode}")
    async with aopen(f"results\\{dt} {_mode}__output_.json", mode = "wb") as __file:

        await __file.write(dumps(_data, option=OPT_INDENT_2))

@app.route("/", methods = ["GET", "POST"])
def linebot():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text = True)
    handler.handle(body, signature)
    _data = Json.loads(body)
    _token = _data['events'][0]['replyToken']    
    _id = _data['events'][0]['source']['userId']
    # with open("_data.json", mode="wb") as __data:
    #     __data.write(dumps(_data, option = OPT_INDENT_2))
    if "message" in _data["events"][0] and _data["events"][0]["message"]["type"] == "text":
        task = new_event_loop()
        task.run_until_complete(kwds_check(_data['events'][0]['message']['text']))
        task.close()
        global kwds_
        if (kwds_ != ""):
            loop = new_event_loop()
            loop.run_until_complete(crawler(kwds_))
            loop.close()
            __response = Json.load(f"results\\{dt} {kwds_}__output_.json")
            _response = __response["records"]["Earthquake"][0]["EarthquakeInfo"]
            msg = f"{_response['OriginTime'].replace(':', '-')}發生芮氏規模 {_response['EarthquakeMagnitude']['MagnitudeValue']} 的地震!\n>>>\n地點: {_response['Epicenter']['Location']}\n震源深度: {_response['FocalDepth']}\n>>>"
            img = __response["records"]["Earthquake"][0]["ReportImageURI"]
            reply(msg, img, _token, _config["BOT-TOKEN"])
            # reply(msg, "qrcode", _token, _config["BOT-TOKEN"])
        
        kwds_ = -1

    return ">>>POST<<<"

if __name__ == "__main__":
    if system() == "Windows":
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    global kwds_
    kwds_ = ""
    run_with_ngrok(app)
    app.run()