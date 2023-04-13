import ssl, time, json, threading, requests, os, shutil
from websocket import WebSocketApp
from yaml import safe_load
from plyer import notification
from colorama import init, Fore 
init(True,True)
class console:
    def banner():
        os.system("cls")
        print(Fore.LIGHTBLUE_EX+"   ____                      _  __             ".center(shutil.get_terminal_size().columns))
        print(Fore.LIGHTBLUE_EX+"  / __/_ _____  ___ ________/ |/ /__ _  _____ _".center(shutil.get_terminal_size().columns))
        print(Fore.LIGHTBLUE_EX+" _\ \/ // / _ \/ -_) __/___/    / _ \ |/ / _ `/".center(shutil.get_terminal_size().columns))
        print(Fore.LIGHTBLUE_EX+"/___/\_,_/ .__/\__/_/     /_/|_/\___/___/\_,_/ ".center(shutil.get_terminal_size().columns))
        print(Fore.LIGHTBLUE_EX+"        /_/                                    ".center(shutil.get_terminal_size().columns))
        print(Fore.CYAN+"Bloxflip Rain Notifier. By: Mouad#7314".center(shutil.get_terminal_size().columns))
        print("\n")
    def information(text):
        print(
            f"({Fore.LIGHTCYAN_EX}~{Fore.RESET}) {Fore.LIGHTBLUE_EX}{text}"
        )
    def rain(text,content=None):
        print(
            f"({Fore.LIGHTGREEN_EX}${Fore.RESET}) {text}{' > '+content if content else ''}"
        )
    def error(text,content=None):
        print(
            f"({Fore.LIGHTRED_EX}-{Fore.RESET}) {Fore.LIGHTRED_EX}{text}{Fore.RED}{' > '+content if content else ''}"
        )
config = safe_load(open("config.yml"))
def notify(rain_data,_type="active"):
    if _type == "active":
        message = f"**Robux**: {rain_data['prize']}\n**Time Left**: {round(rain_data['timeLeft']/1000)}s\nHost:{rain_data['host']}"
        if config["notification"]["active"] == True:
            notification.notify(
                title = 'Bloxflip Rain Notifier',
                message = message,
                app_icon = None,
                timeout = config["notification"]["timeout"],
            )
        if config["webhook"]["active"] == True:
            _config = config["webhook"]
            role_id = _config["role id"]
            payload = {
                "content": (role_id if role_id != 0 else "@everyone"),
                "embeds": [{
                    "description": message,
                    "color": 62975,
                    "author": {"name": "Bloxflip Rain Notifier","url": "https://bloxflip.com/a/methods"},
                    "footer": {"text":"Mouad#7314","icon_url":"https://cdn.discordapp.com/attachments/1094813464037429310/1095701806811725866/M_Profile_Picture.png"}
                }],
                "username": _config["username"],
                "avatar_url": _config["avatar url"],
                "attachments": []
            }
            requests.post(_config["url"],json=payload)
        elif _type == "ended":
            message = "Rain ended."
            if config["notification"]["active"] == True:
                notification.notify(
                    title = 'Bloxflip Rain Notifier',
                    message = message,
                    app_icon = None,
                    timeout = config["notification"]["timeout"],
                )
            if config["webhook"]["active"] == True:
                _config = config["webhook"]
                role_id = _config["role id"]
                payload = {
                    "content": (role_id if role_id != 0 else "@everyone"),
                    "embeds": [{
                        "description": message,
                        "color": 62975,
                        "author": {"name": "Bloxflip Rain Notifier","url": "https://bloxflip.com/a/methods"},
                        "footer": {"text":"Mouad#7314","icon_url":"https://cdn.discordapp.com/attachments/1094813464037429310/1095701806811725866/M_Profile_Picture.png"}
                    }],
                    "username": _config["username"],
                    "avatar_url": _config["avatar url"],
                    "attachments": []
                }
                requests.post(_config["url"],json=payload)
def keep_alive(ws, interval):
    while True:
        time.sleep(int(interval))
        ws.send("2")

def on_message(ws,msg):
    if "pingInterval" in msg:
        threading.Thread(target=keep_alive,args=(ws,json.loads(msg.replace("0",""))["pingInterval"])).start()
        ws.send("40/chat,")
    elif 'rain-state-changed' in msg:
        data = json.loads(msg.replace("42/chat,",""))[1]
        if data.get("active"):
            if data["active"] == True:
                console.rain("Rain detected!",f"Robux: {data['prize']} | Host: {data['host']}")
                notify(data)
        elif data == False:
            console.rain("Rain ended.")
            print("($) Rain ended.")
            notify(data, "ended")

def on_open(_):
    console.banner()
    console.information(f"Connected to websocket{Fore.LIGHTCYAN_EX}!")

def on_err(_, err):
    console.error("Catched websocket error",err)

headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US',
    'Cache-Control': 'no-cache',
    'Connection': 'Upgrade',
    'Pragma': 'no-cache',
    'Upgrade': 'websocket',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}
wsa = WebSocketApp("wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket",header=headers,on_open=on_open,on_message=on_message,on_error=on_err)
wsa.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE},origin="https://bloxflip.com",host="ws.bloxflip.com",reconnect=True)
