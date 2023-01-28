from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from asyncio import new_event_loop, set_event_loop_policy, WindowsSelectorEventLoopPolicy, run
from aiofiles import open as aopen
from platform import system

from flask_ngrok import run_with_ngrok
from flask import Flask, request, abort, current_app
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage

import json
with open('config.json', 'r+', encoding='utf-8') as _file:
    _config = json.load(_file)

async def kwds_check(msg):
    async with aopen("keywords.txt", mode="r+", encoding="utf-8") as __kwds:
        for _kwds in __kwds:
            if msg == _kwds[:-1]:
                print(_kwds)
                return True
        else:
            return False

# url = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/{_mode}?Authorization=" + _config["TOKEN"]

app = Flask(__name__, template_folder="templates")

line_bot_api = LineBotApi(_config["BOT-TOKEN"])
handler = WebhookHandler(_config["BOT-SECRET"])

def reply_msg(msg, rk, TOKEN):
    HEADERS = {'Authorization':f'Bearer {TOKEN}','Content-Type':'application/json'}
    BODY = {
    "replyToken" : rk,
    "messages" : [{
            "type": "text",
            "text": msg
        }]
    }
    response = requests.post(url = "https://api.line.me/v2/bot/message/reply", headers=HEADERS,data=json.dumps(BODY).encode("utf-8"))
    print(response.text)

def reply_img(img, rk, TOKEN):
    HEADERS = {'Authorization':f'Bearer {TOKEN}','Content-Type':'application/json'}
    BODY = {
        "replyToken" : rk,
        "messages" : [{
            "type" : "image", 
            "originalContentUrl" : img,
            "previewImageUrl" : img
        }]
    }
    response = requests.post(url = "https://api.line.me/v2/bot/message/reply", headers=HEADERS,data=json.dumps(BODY).encode("utf-8"))
    print(response.text)

def filter(msg):
    if "地震" in msg:
        return 

async def main():

    from orjson import dumps, OPT_INDENT_2

    dt = datetime.now().strftime("%Y%m%d %H-%M-%S")
    async with aopen("mode.txt", mode="r+", encoding="utf-8") as __mode:
        async for _mode in __mode:
            url = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/{_mode[:-1]}?Authorization=" + _config["TOKEN"]
            _data = requests.get(url).json()
            print(f"Capture >>> {_mode[:-1]}")
            async with aopen(f"results\\{dt} {_mode[:-1]}__output_.json", mode = "wb") as __file:
                await __file.write(dumps(_data, option=OPT_INDENT_2))

@app.route("/", methods = ["GET", "POST"])
def linebot():
    signature = request.headers["X-Line-Signature"]
    # signature = requests.get("http://127.0.0.1:5050").headers["X-Line-Signature"]
    body = request.get_data(as_text = True)
    handler.handle(body, signature)
    _data = json.loads(body)
    _token = _data['events'][0]['replyToken']    
    _id = _data['events'][0]['source']['userId']
    # print(f">>>\n{_data}\n>>>")

    if "message" in _data["events"][0] and _data["events"][0]["message"]["type"] == "text":
        if (kwds_check(_data['events'][0]['message']['text'])):
            loop = new_event_loop()
            loop.run_until_complete(main())
            loop.close()
            reply_msg(_data['events'][0]['message']['text'], _token, _config["BOT-TOKEN"])

    return ">>>POST<<<"

if __name__ == "__main__":
    if system() == "Windows":
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    run_with_ngrok(app)
    app.run()