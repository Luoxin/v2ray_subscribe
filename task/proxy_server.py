import os
import signal
import subprocess
import sys
import time
import traceback

import psutil

from utils import logger


class V2rayServer:
    def __init__(self, path, conf):
        self._path = (
            path.replace("\\", "/")
            if sys.platform == "win"
            else path.replace("/", "\\") + ".exe"
        )
        self._conf = (
            conf.replace("\\", "/")
            if sys.platform == "win"
            else conf.replace("/", "\\")
        )
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
        def _filepath_comparison(path1, path2) -> bool:
            return path1.replace("/", "").replace("\\", "") == path1.replace(
                "/", ""
            ).replace("\\", "")

        for pid in psutil.pids():
            try:
                p = psutil.Process(pid)
                cmd = p.cmdline()

                if len(cmd) == 3:
                    if "v2ray" in cmd[0]:
                        if _filepath_comparison(cmd[0], self._path) and _filepath_comparison(cmd[2], self._conf):
                            logger.info("找到的 cmd 的指令".format(cmd))
                            self.pid = pid
                            return

                cmd = " ".join(cmd)
                if cmd == self.cmd:
                    logger.info("找到了正确的指令为 {}".format(cmd))
                    self.pid = pid
                    return
            except:
                pass

    def get_conf_path(self):
        return self._conf
