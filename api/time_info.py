"""
    时间服务，只要包括了校时以及时间戳的返回
"""
import subprocess
import sys
import time

import datetime

import ntplib
import requests
import traceback
from flask import Blueprint, request, redirect

from conf.conf import NTP_HOST, NTP_PORT, NTP_INTERVAL
from error_exception import create_error_with_msg
from utils import logger  # 日志

time_info = Blueprint("time_info", __name__)


@time_info.route("/time_info", methods=["GET", "POST"])
def time_info_index():
    return "时间戳服务"


# 校验系统时间
def check_time_consistent() -> bool:
    try:
        rsp = ntplib.NTPClient().request(host=NTP_HOST, port=NTP_PORT)
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
    logger.info("时间校验服务启动")
    while True:
        if not check_time_consistent():
            break
        time.sleep(NTP_INTERVAL)
