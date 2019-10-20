import sys
import time

import requests


proxies = {
    "http": "socks5://127.0.0.1:1088",
    "https": "socks5://127.0.0.1:1088",
}

url = "http://www.google.com"

start_time = time.time()
r = requests.get(url,
                 proxies=proxies,
                 timeout=60 * 1000,
                 )

# speed = r.elapsed.microseconds / 1000
request_time = time.time() - start_time
del start_time
size = sys.getsizeof(r.content)
print(size)

speed = size/request_time

print(speed)