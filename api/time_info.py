"""
    时间服务，只要包括了校时以及时间戳的返回
"""
import datetime
import subprocess
import sys
import time
import traceback

import ntplib
from flask import Blueprint
from conf import global_variable
from utils import logger  # 日志

time_info = Blueprint("time_info", __name__)


@time_info.route("/time_info", methods=["GET", "POST"])
def time_info_index():
    return "时间戳服务"


# 校验系统时间
def check_time_consistent(host, port) -> bool:
    try:
        rsp = ntplib.NTPClient().request(host=host, port=port)
        now = rsp.tx_time
        if sys.platform == "win32":
            subprocess.check_output(
                "date {} && time {}".format(
                    time.strftime("%Y-%m-%d", time.localtime(now)),
                    datetime.datetime.utcfromtimestamp(now).strftime("%H:%M:%S"),
                ),
                shell=True,
            )
        elif sys.platform == "linux":
            subprocess.check_output("date --date='@{}'".format(now), shell=True)
        else:
            logger.warning("未知系统环境，无法进行系统时间校验: {}".format(sys.platform))
    except subprocess.CalledProcessError:
        logger.error("没有校验权限")
        return False
    except:
        logger.error("校时失败：{}".format(traceback.format_exc()))
    return True


# 保持系统时间一致性
def keep_time_consistent():
    need_start = False
    logger.info("时间校验服务启动")
    ntp_interval = global_variable.get_conf_int("NTP_INTERVAL", default=64)
    ntp_host = global_variable.get_conf_str("NTP_HOST", default="ntp.aliyun.com")
    ntp_port = global_variable.get_conf_int("NTP_PORT", default=123)
    while True:
        if not check_time_consistent(ntp_host, ntp_port):
            break
        time.sleep(ntp_interval)
