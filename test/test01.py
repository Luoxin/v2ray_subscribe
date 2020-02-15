import requests
from lxml import etree

r = requests.get(
    "https://sites.google.com/site/v2raysub/",
    timeout=5,
    proxies={"http": "socks5://127.0.0.1:10808", "https": "socks5://127.0.0.1:10808"},
).content.decode("utf-8")
soup = etree.HTML(r)
