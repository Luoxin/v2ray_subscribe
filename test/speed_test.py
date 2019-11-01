import sys

sys.path.append("..")
sys.path.append("../..")

import json
import utils
from node import V2ray

url = "vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIuKYheS4gOWumuimgee7j+W4uOabtOaWsOiuoumYheKYhSIsDQogICJhZGQiOiAidW5pLmtpdHN1bmViaS5mdW4iLA0KICAicG9ydCI6ICIxMDAyNSIsDQogICJpZCI6ICI5NTEzNzg1Ny03MGZhLTRhYzgtOGY5MC00ZTIwYWViNjYyY2YiLA0KICAiYWlkIjogIjAiLA0KICAibmV0IjogInRjcCIsDQogICJ0eXBlIjogIm5vbmUiLA0KICAiaG9zdCI6ICIiLA0KICAicGF0aCI6ICIiLA0KICAidGxzIjogIiINCn0="

base64_str = url.replace("vmess://", "")
jsonstr = utils.decode(base64_str)

server_node = json.loads(jsonstr)
v2node = V2ray(
    server_node["add"],
    int(server_node["port"]),
    server_node["ps"],
    "auto",
    server_node["id"],
    int(server_node["aid"]),
    server_node["net"],
    server_node["type"],
    server_node["host"],
    server_node["path"],
    server_node["tls"],
)
node = v2node

print(json.dumps(node.format_config()))
