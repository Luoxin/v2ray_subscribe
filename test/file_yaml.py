import yaml

# 获取文件全路径
filename = "test.yaml"

f = open(filename, encoding="utf-8")
y = yaml.load(f, Loader=yaml.FullLoader)
print(y.get("PROXIES_TEST"))
print(y)
