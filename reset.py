import requests

botToken = "1202514912:AAE2yMJiiRTbP2nXYhp2ksHPjJYe5GlVCxo"
botID = -1001194635704

msg = "/reset"
url = f"https://api.telegram.org/bot{botToken}/sendMessage?chat_id={botID}&text={msg}"

requests.get(url)