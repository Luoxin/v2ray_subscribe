import os
import signal
import subprocess
import threading
import traceback

import psutil

from log import logger


class V2rayServer:
    def __init__(self, path, conf):
        self.cmd = "{} -config {}".format(path, conf)
        self.pid = 0

    def run_server(self):
        try:
            run = threading.Thread(None, self.__run_server(), None,)
            run.daemon = True
            run.start()
        except:
            logger.error(traceback.format_exc())

    def __run_server(self):
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
                self.pid = 0
        except:
            logger.error(traceback.format_exc())

    def restart(self):
        # 如果未记录这个，需要重新获取一遍pid
        if self.pid == 0:
            self.__find_pid()

        # 如果存在已有的服务，再kill
        if self.pid != 0:
            self.kill()

        self.run_server()

    def __find_pid(self):
        pid_list = psutil.pids()

        for pid in pid_list:
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
