import requests


proxies = {
    "http": "socks://127.0.0.1:1088",
    "https": "socks://127.0.0.1:1088",
}

url = "https://www.google.com"

r = requests.get(url,
                 proxies=proxies,
                 timeout=60 * 1000,
                 )

speed = r.elapsed.microseconds / 1000

print(speed)