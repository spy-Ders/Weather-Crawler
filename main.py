from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from asyncio import new_event_loop, set_event_loop_policy, WindowsSelectorEventLoopPolicy, run
from aiofiles import open as aopen
from platform import system

from flask_ngrok import run_with_ngrok
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler

from orjson import loads, dumps, OPT_INDENT_2

from modules import Json, crawler, bot

_config = Json.load("config.json")
cwb_URL = "https://www.cwb.gov.tw"

app = Flask(__name__)
line_bot_api = LineBotApi(_config["BOT-TOKEN"])
handler = WebhookHandler(_config["BOT-SECRET"])
dt = datetime.now().strftime("%Y%m%d %H-%M-%S")

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
        client = bot(dt = dt, kwd = _data['events'][0]['message']['text'],msg = None, img = None, rk = _token, TOKEN = _config["BOT-TOKEN"])
        global kwds_
        kwds_ = run(client.kwds_check())
        if (kwds_ != ""):
            _info = crawler(dt = dt, mode = kwds_)
            run(_info.crawl())
            __response = Json.load(f"results\\{dt} {kwds_}__output_.json")
            _response = __response["records"]["Earthquake"][0]["EarthquakeInfo"]
            msg = f"{_response['OriginTime'].replace(':', '-')}發生芮氏規模 {_response['EarthquakeMagnitude']['MagnitudeValue']} 的地震!\n>>>\n地點: {_response['Epicenter']['Location']}\n震源深度: {_response['FocalDepth']}\n>>>"
            img = __response["records"]["Earthquake"][0]["ReportImageURI"]
            client = bot(dt = dt, kwd = None, msg = msg, img = img, rk = _token, TOKEN = _config["BOT-TOKEN"])
            client.reply()

        kwds_ = -1
    
    return ">>>POST<<<"

if __name__ == "__main__":
    if system() == "Windows":
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    global kwds_
    kwds_ = ""
    run_with_ngrok(app)
    app.run()