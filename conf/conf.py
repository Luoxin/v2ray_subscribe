import sys

sys.path.append("../")

# 模块名
MODEL_NAME = "v2ray_subscribe"

# 日志级别
LOG_DEBUG = True
# 日志路径
# LOG_PATH = "/root/log/v2ray_subscribe.log"
LOG_PATH = "v2ray_subscribe.log"

# TEST_FILE_URL = "http://cachefly.cachefly.net/1mb.test"
# TEST_FILE_URL = "http://speedtest-sfo2.digitalocean.com/1mb.test "
# TEST_FILE_URL = "http://www.google.com"
TEST_FILE_URL = "https://www.youtube.com/"

# host
HOST = "127.0.0.1"
# port
PORT = 5000

CHECK_PORT = 5002

# flask debug
FLASK_DEBUG = False

# sqlalchemy debug
SQLALCHEMY_DEBUG = False

# shelve save path
SHELVE_PATH = "/root/app/v2ray_subscribe/WallBuffer.dbm"

# min speed
BASE_SPEED = 5000

# 默认的生命值
HEALTH_POINTS = 10

# Redis连接信息
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

# 错误码文件路径
ERROR_ENUM_PATH = "./conf/error.yaml"

# 数据库地址
# 如果使用 `sqlite` 请加上 ?check_same_thread=False
# DB_URL = "postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/dev"
DB_URL = "sqlite:///D:/server/v2ray_subscribe/subscribe.vdb?check_same_thread=False"
# DB_URL = "postgresql+psycopg2://postgres:postgres@106.12.107.126:5432/dev"

# 默认检测间隔
Interval = 60 * 60

PROXIES_TEST = {
    "http": "socks5://127.0.0.1:{}".format(CHECK_PORT),
    "https": "socks5://127.0.0.1:{}".format(CHECK_PORT),
}

PROXIES_CRAWLER = {
    "http": "socks5://127.0.0.1:10808",
    "https": "socks5://127.0.0.1:10808",
}

V2RAY_SERVICE_PATH = "C:/Users/luoxi/Desktop/v2ray/v2ray.exe"
# V2RAY_SERVICE_PATH = "/usr/bin/v2ray/v2ray"

# V2RAY_CONFIG_LOCAL = "/etc/v2ray/config.json"
V2RAY_CONFIG_LOCAL = "C:/Users/luoxi/Desktop/v2ray/c.json"
