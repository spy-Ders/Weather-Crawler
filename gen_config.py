from modules import Json

async def gen_CONFIG():
    CONFIG: dict[str, dict] = {
        "BOT-TOKEN" : "",
        "BOT-SECRET" : "",
        "CWB-TOKEN" : "",
        "IMGUR-TOKEN" : ""
    }

    CONFIG["BOT-TOKEN"] = input("Your Line-bot TOKEN")
    CONFIG["BOT-SECRET"] = input("Your Line-bot SECRET")
    CONFIG["CWB-TOKEN"] = input("Your CWB-API TOKEN")
    CONFIG["IMGUR-TOKEN"] = input("Your IMGUR TOKEN")

    Json.dump_nowait("config.json", CONFIG)