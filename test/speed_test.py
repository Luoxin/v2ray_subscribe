import sys

sys.path.append("..")
sys.path.append("../..")

import json, utils
from node import V2ray

url = "vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIiIsDQogICJhZGQiOiAiNDcuNzUuNDkuMyIsDQogICJwb3J0IjogIjM2NjQ0IiwNCiAgImlkIjogIjdmMTg5YWQ2LTE2MGYtNGExZi1hODgwLWVhN2Y4NzZhZWFmYiIsDQogICJhaWQiOiAiMjMzIiwNCiAgIm5ldCI6ICJ3cyIsDQogICJ0eXBlIjogIm5vbmUiLA0KICAiaG9zdCI6ICIiLA0KICAicGF0aCI6ICIiLA0KICAidGxzIjogIiINCn0="

type = "v2ray"
base64_str = url.replace('vmess://', '')
jsonstr = utils.decode(base64_str)

server_node = json.loads(jsonstr)
v2node = V2ray(server_node['add'], int(server_node['port']), server_node['ps'], 'auto', server_node['id'],
               int(server_node['aid']), server_node['net'], server_node['type'], server_node['host'],
               server_node['path'], server_node['tls'])
node = v2node

print(node.formatConfig())
