import sys
sys.path.append("../")

# 模块名
MODEL_NAME = "v2ray_subscribe"

# 日志级别
LOG_DEBUG = False
# 日志路径
LOG_PATH = "v2ray_subscribe.log"

V2RAY_CONFIG_LOCAL = "/etc/v2ray/config.json"
TEST_FILE_URL = "http://cachefly.cachefly.net/1mb.test"

# host
HOST = "0.0.0.0"
# port
PORT = 1084

# flask debug
FLASK_DEBUG = False

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
