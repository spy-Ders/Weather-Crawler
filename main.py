from datetime import datetime
from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy, run
from aiofiles import open as aopen
from platform import system
from os.path import isdir
from os import makedirs

from flask_ngrok import run_with_ngrok
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler

from modules import Json, crawler, bot

# config檔案讀取
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
    
    # _id = _data['events'][0]['source']['userId']

    # with open("_data.json", mode="wb") as __data:
    #     __data.write(dumps(_data, option = OPT_INDENT_2))
    
    if "message" in _data["events"][0] and _data["events"][0]["message"]["type"] == "text":
        client = bot(dt = dt, kwd = _data['events'][0]['message']['text'],msg = None, img = None, rk = _token, TOKEN = _config["BOT-TOKEN"])
        global kwds_
        kwds_ = run(client.kwds_check())
        if kwds_ != "" or kwds_ != None:    
            _info = crawler(dt = dt, mode = kwds_)
            run(_info.crawl())
            __response = Json.load(f"results\\{dt} {kwds_}__output_.json")
            if kwds_ == "E-A0016-001":
                _response = __response["records"]["Earthquake"][0]["EarthquakeInfo"]
                msg = f"{_response['OriginTime'].replace(':', '-')}發生芮氏規模 {_response['EarthquakeMagnitude']['MagnitudeValue']} 的地震!\n>>>\n地點: {_response['Epicenter']['Location']}\n震源深度: {_response['FocalDepth']}\n>>>"
                img = __response["records"]["Earthquake"][0]["ReportImageURI"]
                client = bot(dt = dt, kwd = None, msg = msg, img = img, rk = _token, TOKEN = _config["BOT-TOKEN"])
                client.reply()

            # elif kwds_ == "E-A0014-001":
            #     client = bot(dt = dt, kwd = None, msg = f"找不到相關資訊喔 >\\\\\\< \n疑難排解:\n1.目前未提供該服務\n2.請參考中央氣象局官方網站獲取更多資訊\n{cwb_URL}", img = "https://hackmd.io", rk = _token, TOKEN = _config["BOT-TOKEN"])
            #     client.reply()
            
            else:

                client = bot(dt = dt, kwd = None, msg = f"找不到相關資訊喔 >\\\\\\< \n疑難排解:\n1.目前未提供該服務\n2.請參考中央氣象局官方網站獲取更多資訊\n{cwb_URL}", img = "official", rk = _token, TOKEN = _config["BOT-TOKEN"])
                client.reply()

        else:
            
            client = bot(dt = dt, kwd = None, msg = f"找不到相關資訊喔 >\\\\\\< \n疑難排解:\n1.目前未提供該服務\n2.請參考中央氣象局官方網站獲取更多資訊\n{cwb_URL}", img = "official", rk = _token, TOKEN = _config["BOT-TOKEN"])
            client.reply()

        kwds_ = -1
    
    return ">>>POST<<<"

if __name__ == "__main__":
    
    if system() == "Windows":
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    
    # kwds_ init
    global kwds_
    kwds_ = ""
    
    # 爬蟲結果資料夾存在 ? continue : 建立
    if not isdir("results"):
        makedirs("results")
    
    # 以ngrok執行
    run_with_ngrok(app)
    app.run()