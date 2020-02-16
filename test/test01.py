import utils
import json

url = "vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIummmea4ryBIS1RBU0gwMiB8IFYyVjIgfCDkuInnvZHkvJjljJYiLA0KICAiYWRkIjogImNuLXNoLnNodXNoZW5nZGFpbmlmZWkuY29tIiwNCiAgInBvcnQiOiAiMjIwMDIiLA0KICAiaWQiOiAiZDcyYWExNGEtNDA2Zi0zZTk4LTk2NzMtMDMyY2U1YWU4Y2VhIiwNCiAgImFpZCI6ICIyIiwNCiAgIm5ldCI6ICJ3cyIsDQogICJ0eXBlIjogIm5vbmUiLA0KICAiaG9zdCI6ICJhamF4Lm1pY3Jvc29mdC5jb20iLA0KICAicGF0aCI6ICIvdjJyYXkiLA0KICAidGxzIjogIiINCn0="

conf = json.loads(utils.base64_decode(url.replace("vmess://", "")))
conf["ps"] = "真正要分开的两个人，连“分手”二字都是多余的，因为殊途同归。"

print("vmess://" + utils.base64_encode(conf))
