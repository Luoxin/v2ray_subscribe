import sys
import time

import requests

sys.path.append("..")
sys.path.append("../..")

from check_alive import V2rayServer

vs = V2rayServer("C:/Users/Luoxin/Desktop/v2ray/v2ray.exe", "C:/Users/Luoxin/Desktop/v2ray/c.json")
vs.find_pid()
# vs.restart()
#
# start_time = time.time()
# r = requests.get("http://www.google.com",
#                  proxies={
#                      "http": "socks5://127.0.0.1:10808",
#                      "https": "socks5://127.0.0.1:10808",
#                  },
#                  timeout=1 * 1000,
#                  )
# if r.status_code == 200:
#     # speed = r.elapsed.microseconds / 1000 / 1000 // 请求的延时
#     request_time = time.time() - start_time
#     del start_time
#     size = sys.getsizeof(r.content) / 1024
#     speed = size / request_time - r.elapsed.microseconds / 1000 / 1000
# else:
#     speed = 0
# r.close()
#
# print(speed)
#
# time.sleep(60 * 60 * 60)
