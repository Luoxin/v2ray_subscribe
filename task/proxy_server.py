import os
import signal
import subprocess
import sys
import time
import traceback

import psutil

from conf import global_variable
from utils import logger


class V2rayServer:
    def __init__(self, path, conf):
        self._path = os.path.join(os.getcwd(), path)
        self._conf = conf
        self.cmd = "{} -config {} ".format(self._path, self._conf,)
        self.pid = 0
        logger.debug("启动 v2ray 的命令 {}".format(self.cmd))

    def run_server(self):
        try:
            self._run_server()
        except:
            logger.error(traceback.format_exc())

    def _run_server(self):
        try:
            if self.pid == 0:
                ps = subprocess.Popen(self.cmd)
                self.pid = ps.pid
        except:
            logger.error(traceback.format_exc())

    def kill(self):
        try:
            if self.pid != 0:
                # logger.debug("wil kill old progress, pid is {}".format(self.pid))
                try:
                    if sys.platform == "win32":
                        os.popen("taskkill.exe /F /PID:" + str(self.pid))
                        return
                except:
                    logger.error("err: {}".format(traceback.format_exc()))

                try:
                    os.kill(self.pid, signal.SIGTERM)
                except:
                    logger.error("err: {}".format(traceback.format_exc()))
                    try:
                        os.kill(self.pid, signal.SIGKILL)
                    except:
                        logger.error("err: {}".format(traceback.format_exc()))
        except:
            logger.error(traceback.format_exc())
            logger.error("进程pid为 {}".format(self.pid))
        finally:
            self.pid = 0

    def restart(self):
        # 如果未记录这个，需要重新获取一遍pid
        # if self.pid == 0:
        self._find_pid()

        # 如果存在已有的服务，再kill
        if self.pid != 0:
            self.kill()

        self.run_server()
        time.sleep(1)

    def _find_pid(self):
        for pid in psutil.pids():
            try:
                p = psutil.Process(pid)
                if pid == 0 or len(p.cmdline()) == 0:
                    continue
                for connection in p.connections():
                    if (
                        connection.type == 1
                        and (
                            connection.laddr.port
                            == global_variable.get_conf_int("CHECK_PORT", default=1080)
                            if connection.laddr != ()
                            else False
                        )
                        or (
                            connection.raddr.port
                            != global_variable.get_conf_int("CHECK_PORT", default=1080)
                            if connection.laddr == ()
                            else False
                        )
                    ):
                        self.pid = pid
                        return
            except (PermissionError, psutil.AccessDenied, psutil.NoSuchProcess):
                pass

    def get_conf_path(self):
        return self._conf


def new_proxy() -> V2rayServer:
    return V2rayServer(
        os.path.join(
            global_variable.get_conf_str(
                "V2RAY_SERVICE_PATH",
                default="C:/ProgramData/v2ray"
                if sys.platform == "win"
                else "/usr/bin/v2ray",
            ),
            "v2ray",
        ),
        os.path.join(
            global_variable.get_conf_str(
                "V2RAY_SERVICE_PATH",
                default="C:/ProgramData/v2ray"
                if sys.platform == "win"
                else "/usr/bin/v2ray",
            ),
            "v2ray_subscribe.conf",
        ),
    )
