import sys

sys.path.append("..")
sys.path.append("../..")

import json
import utils
from node import V2ray

url = "vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIltmcmVlLXNzLnNpdGVdd3d3Lmtlcm5lbHMuYmlkIiwNCiAgImFkZCI6ICJ3d3cua2VybmVscy5iaWQiLA0KICAicG9ydCI6ICI0NDMiLA0KICAiaWQiOiAiM2RiM2E0MjktMDM2Yi00NzAxLWMyY2YtMTM2NzdiMzJkYjg0IiwNCiAgImFpZCI6ICIwIiwNCiAgIm5ldCI6ICJ3cyIsDQogICJ0eXBlIjogIm5vbmUiLA0KICAiaG9zdCI6ICIiLA0KICAicGF0aCI6ICIvd3MiLA0KICAidGxzIjogInRscyINCn0="

base64_str = url.replace('vmess://', '')
jsonstr = utils.decode(base64_str)

server_node = json.loads(jsonstr)
v2node = V2ray(server_node['add'], int(server_node['port']), server_node['ps'], 'auto', server_node['id'],
               int(server_node['aid']), server_node['net'], server_node['type'], server_node['host'],
               server_node['path'], server_node['tls'])
node = v2node

print(json.dumps(node.format_config()))
