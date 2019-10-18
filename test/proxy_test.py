import requests


proxies = {
    "http": "socks5://127.0.0.1:1086",
    "https": "socks5://127.0.0.1:1086",
}

url = "https://www.google.com"

r = requests.get(url,
                 proxies=proxies,
                 timeout=60 * 1000,
                 )

speed = r.elapsed.microseconds / 1000

print(speed)