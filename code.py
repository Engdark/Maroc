import requests
import random
import string
import threading
import time

def send_request():
    while True:
        rad = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        e_rad = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        m_rad = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        hard_rad = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        imposible = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        random_text_number = rad + e_rad + m_rad + imposible + hard_rad
        
        #print(random_text_number)

        url = "http://pornhd.josex1.name/js/like.php"
        data = {
            "id": "41437",
            "type": "like"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": f"Mozilla{random_text_number}/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        response = requests.post(url, data=data, headers=headers)
        print("Response Text:", response.text)

        #time.sleep(1)

threads = []
for _ in range(200): 
    thread = threading.Thread(target=send_request)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
