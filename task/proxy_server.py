import os
import signal
import subprocess
import threading
import traceback
import psutil

from utils import logger


class V2rayServer:
    def __init__(self, path, conf):
        self.cmd = "{} -config {}".format(path, conf)
        self.pid = 0

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
                os.kill(self.pid, signal.SIGTERM)
        except:
            logger.error(traceback.format_exc())
            logger.error("进程pid为 {}".format(self.pid))
        finally:
            self.pid = 0

    def restart(self):
        # 如果未记录这个，需要重新获取一遍pid
        if self.pid == 0:
            self._find_pid()

        # 如果存在已有的服务，再kill
        if self.pid != 0:
            self.kill()

        self.run_server()

    def _find_pid(self):
        for pid in psutil.pids():
            try:
                p = psutil.Process(pid)
                cmd = p.cmdline()
                cmd = " ".join(cmd)
                # print(cmd)
                if cmd == self.cmd:
                    self.pid = pid
                    return
            except:
                pass
