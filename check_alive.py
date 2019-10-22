import json
import os
import random
import signal
import subprocess
import sys
import threading
import time
import traceback
import urllib

import psutil
import requests

import utils
from conf.conf import V2RAY_CONFIG_LOCAL, HEALTH_POINTS, PROXIES_TEST, TEST_FILE_URL, V2RAY_SERVICE_PATH
from log import logger
from node import V2ray, Shadowsocks
from orm import session, SubscribeVmss

from fake_useragent import UserAgent

ua = UserAgent()


class V2rayServer:
    def __init__(self, path, conf):
        self.cmd = "{} -config {}".format(path, conf)
        self.pid = 0

    def run_server(self):
        try:
            run = threading.Thread(None, self.__run_server(), None, )
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
            if self != 0:
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


v2ray_server = V2rayServer(V2RAY_SERVICE_PATH, V2RAY_CONFIG_LOCAL)


def get_node_by_url(url: str != ""):
    node = None
    node_type = ""
    try:
        if url.startswith('ss://'):  # ss node
            node_type = "ss"
            base64_str = url.replace('ss://', '')
            base64_str = urllib.parse.unquote(base64_str)

            origin = utils.decode(base64_str[0: base64_str.index('#')])
            remark = base64_str[base64_str.index('#') + 1:]
            security = origin[0: origin.index(':')]
            password = origin[origin.index(':') + 1: origin.index('@')]
            ipandport = origin[origin.index('@') + 1:]
            ip = ipandport[0: ipandport.index(':')]
            port = int(ipandport[ipandport.index(':') + 1:])
            ssode = Shadowsocks(ip, port, remark, security, password)
            node = ssode
        elif url.startswith('vmess://'):  # vmess
            node_type = "v2ray"
            base64_str = url.replace('vmess://', '')
            jsonstr = utils.decode(base64_str)

            server_node = json.loads(jsonstr)
            v2node = V2ray(server_node['add'], int(server_node['port']), server_node['ps'], 'auto', server_node['id'],
                           int(server_node['aid']), server_node['net'], server_node['type'], server_node['host'],
                           server_node['path'], server_node['tls'])
            node = v2node
    finally:
        return node, node_type


def check_by_v2ray_url(url: str) -> float:
    try:
        node, type = get_node_by_url(url)
        if node is None:
            return 0
        # subprocess.call('cp ' + V2RAY_CONFIG_LOCAL + ' ' + V2RAY_CONFIG_LOCAL + '.bak', shell=False)

        json.dump(node.format_config(), open(V2RAY_CONFIG_LOCAL, 'w'), indent=2)
        v2ray_server.restart()
        # subprocess.call('systemctl restart v2ray.service', shell=True)
        time.sleep(5)
        # subprocess.call('supervisorctl restart v2ray_speed_measurement', shell=True)
        try:
            # speed = subprocess.check_output(
            #     'curl -o /dev/null -s -w %{speed_download} -x socks://127.0.0.1:1086 ' + TEST_FILE_URL, timeout=30,
            #     shell=True)
            headers = {
                'Connection': 'close',
                "User-Agent": ua.random,
            }
            start_time = time.time()
            r = requests.get(TEST_FILE_URL,
                             proxies=PROXIES_TEST,
                             timeout=1 * 1000,
                             headers=headers
                             )
            if r.status_code == 200:
                # speed = r.elapsed.microseconds / 1000 / 1000 // 请求的延时
                request_time = time.time() - start_time
                del start_time
                size = sys.getsizeof(r.content) / 1024
                speed = size / (request_time - r.elapsed.microseconds / 1000 / 1000)
            else:
                speed = 0
            r.close()
            del r
        except requests.exceptions.Timeout:
            logger.warning("connect time out")
            speed = -2
        except requests.exceptions.ConnectionError:
            logger.warning("connect error")
            speed = -3
        except:
            speed = -1
            logger.error(traceback.format_exc())

        logger.info("\t{}kb/s\t连接\t{}".format(speed, url))
        # subprocess.call('mv ' + V2RAY_CONFIG_LOCAL + '.bak ' + V2RAY_CONFIG_LOCAL, shell=True)
        return float(speed)
    except:
        logger.error(traceback.format_exc())
        return -1


def check_link_alive():
    while True:
        try:
            data_list = session.query(SubscribeVmss). \
                filter(SubscribeVmss.next_time < int(time.time())). \
                filter(SubscribeVmss.health_points > 0). \
                order_by(SubscribeVmss.speed.desc()). \
                all()
            # filter(SubscribeVmss.last_state.notin_(1)). \
            if len(data_list) <= 0:
                # logger.info("暂时没有待检测节点")
                time.sleep(20)
                continue
            else:
                for i, data in enumerate(data_list):
                    try:
                        speed = check_by_v2ray_url(data.url)
                        state = 0
                        if speed < 0:
                            state = int(-1 * speed)

                        if speed > 0:
                            session.query(SubscribeVmss).filter(SubscribeVmss.id == data.id).update({
                                SubscribeVmss.speed: speed,
                                SubscribeVmss.health_points: HEALTH_POINTS + 1 if data.health_points < HEALTH_POINTS else data.health_points + 1,
                                SubscribeVmss.next_time: int(random.uniform(0.5, 1.5) * data.interval) + int(
                                    time.time()),
                                SubscribeVmss.last_state: state,
                            })
                        elif speed == 0 or (state != 0 and speed < 0):
                            session.query(SubscribeVmss).filter(SubscribeVmss.id == data.id).update({
                                SubscribeVmss.health_points: HEALTH_POINTS if data.health_points > HEALTH_POINTS else data.health_points - 1,
                                SubscribeVmss.next_time: int(random.uniform(0.5, 1.5) * data.interval) + int(
                                    time.time()),
                                SubscribeVmss.last_state: state,
                            })
                        else:
                            session.query(SubscribeVmss).filter(SubscribeVmss.id == data.id).update({
                                SubscribeVmss.speed: speed,
                                SubscribeVmss.health_points: -1,
                                SubscribeVmss.last_state: state,
                            })
                        session.commit()
                    except:
                        logger.error(traceback.format_exc())
                    finally:
                        time.sleep(5)
                        # logger.info("第{}个节点监测完成".format(i+1))
                logger.info("{}个节点检测完成".format(i + 1))
        except:
            logger.error(traceback.format_exc())
            time.sleep(10)
        finally:
            # logger.info("节点检测完成")
            time.sleep(10)
