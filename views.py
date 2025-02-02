import requests
import string
import random
import threading
import time

def TOKEN_MAKER():
    session = requests.Session()

    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
    }

    response = session.get("http://pornhd.josex1.name", headers=headers)

    cookies = session.cookies.get_dict()

    SID = cookies.get("SID")
    return SID

def send_views():
    random_text_number = ''.join(random.choices(string.ascii_letters + string.digits, k=4))    

    url = "http://pornhd.josex1.name/videos/MILF/A-passionate-mother-with-a-big-ass-decided-to-have-fun-on-a-dick.html"

    headers = {
        "Host": "pornhd.josex1.name",
        "Proxy-Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": f"Mozilla/5.0 ({random_text_number}; Android {random_text_number}; K) AppleWebKit/{random_text_number} (KHTML, like {random_text_number}) Chrome/132.0.0.0 Mobile Safari/{random_text_number}",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": "http://pornhd.josex1.name/popular/3.html",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en;q=0.9",
        "Cookie": f"SID={TOKEN_MAKER()}",
    }

    response = requests.get(url, headers=headers)

    print(response.status_code)

def run_threads():
    while True:
        for _ in range(100):
            thread = threading.Thread(target=send_views)
            thread.start()
        #time.sleep(0.1)

run_threads()
