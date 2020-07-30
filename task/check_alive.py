import json
import random
import sys
import time
import traceback

import requests

import utils
from conf import global_variable
from orm import SubscribeVmss, or_
from task.node import V2ray
from task.proxy_server import new_proxy
from utils import logger

_v2ray_server = new_proxy()


class CheckAlive(object):
    def __init__(
        self,
        check_port: int = global_variable.get_conf_int("CHECK_PORT", 10808),
        interval: int = global_variable.get_conf_int("CHECK_interval", 300),
    ):
        self._check_port = check_port
        self._proxy = "socks5://127.0.0.1:{}".format(self._check_port)
        self._interval = interval

    def check_alive(self, u: str):
        try:
            try:
                time.sleep(5)
                headers = {
                    "Connection": "close",
                    "User-Agent": global_variable.get_user_agent(),
                }
                start_time = time.time()
                r = requests.get(
                    url=u,
                    proxies={
                        "http": self._proxy,
                        "https": self._proxy,
                        "socks": self._proxy,
                        "socks4": self._proxy,
                        "socks5": self._proxy,
                    },
                    timeout=30,
                    headers=headers,
                )
                if r.status_code == 200:
                    request_time = time.time() - start_time
                    del start_time
                    size = sys.getsizeof(r.content) / 1024
                    network_delay = r.elapsed.microseconds / 1000 / 1000
                    speed = size / (request_time - network_delay)
                else:
                    speed = 0
                    network_delay = 0
                r.close()
                del r
            except requests.exceptions.Timeout:
                logger.warning("connect time out")
                speed = -2
                network_delay = -2
            except requests.exceptions.ConnectionError:
                logger.warning("connect error")
                speed = -3
                network_delay = -3
            except:
                speed = -1
                network_delay = -1
                logger.error(traceback.format_exc())

            logger.info("{}kb/s({} ms)\t测试连接{}".format(speed, network_delay, u))
            return float(speed), float(network_delay)
        except:
            logger.error(traceback.format_exc())
            return -1, -1

    def check_alive4google(self, node_id: int):
        try:
            speed, network_delay = self.check_alive("https://www.google.com/")
            new_db = global_variable.get_db()
            new_db.query(SubscribeVmss).filter(SubscribeVmss.id == node_id).update(
                {
                    SubscribeVmss.speed_google: speed,
                    SubscribeVmss.network_delay_google: network_delay,
                }
            )
            new_db.commit()
            return 1 if speed > 0 else -1
        except:
            logger.error(traceback.format_exc())
            return False

    def check_alive4youtube(self, node_id: int):
        try:
            speed, network_delay = self.check_alive("https://www.youtube.com/")
            new_db = global_variable.get_db()
            new_db.query(SubscribeVmss).filter(SubscribeVmss.id == node_id).update(
                {
                    SubscribeVmss.speed_youtube: speed,
                    SubscribeVmss.network_delay_youtube: network_delay,
                }
            )
            new_db.commit()
            return 1 if speed > 0 else -1
        except:
            logger.error(traceback.format_exc())
            return False

    def check_alive4internet(self, node_id: int):
        try:
            speed, network_delay = self.check_alive(
                "http://cachefly.cachefly.net/1mb.test"
            )

            new_db = global_variable.get_db()
            new_db.query(SubscribeVmss).filter(SubscribeVmss.id == node_id).update(
                {
                    SubscribeVmss.speed_internet: speed,
                    SubscribeVmss.network_delay_internet: network_delay,
                }
            )
            new_db.commit()
            return 1 if speed > 0 else -1
        except:
            logger.error(traceback.format_exc())
            return False

    def check_node(self, node: SubscribeVmss):

        update_v2ray_conf(node.url)

        node_id = node.id

        alive = (
            self.check_alive4google(node_id)
            + self.check_alive4youtube(node_id)
            + self.check_alive4internet(node_id)
        )

        if node.interval is None or node.interval <= 0:
            node.interval = self._interval

        try:
            new_db = global_variable.get_db()
            new_db.query(SubscribeVmss).filter(SubscribeVmss.id == node_id).update(
                {
                    SubscribeVmss.next_at: int(random.uniform(0.5, 1.5) * node.interval)
                    + int(time.time()),
                    SubscribeVmss.death_count: node.death_count + alive,
                    SubscribeVmss.interval: node.interval,
                }
            )
            new_db.commit()
        except:
            logger.error(traceback.format_exc())

    def check_all_node(self):
        node_list = (
            global_variable.get_db()
            .query(SubscribeVmss)
            .filter(
                or_(SubscribeVmss.death_count > 0, SubscribeVmss.death_count == None,)
            )
            .filter(
                or_(SubscribeVmss.next_at < utils.now(), SubscribeVmss.next_at == None,)
            )
            .order_by(SubscribeVmss.next_at)
            .all()
        )

        for node in node_list:
            self.check_node(node)


def get_node_by_url(url: str != ""):
    try:
        # if url.startswith("ss://"):  # ss node
        #     node_type = "ss"
        #     base64_str = url.replace("ss://", "")
        #     base64_str = urllib.parse.unquote(base64_str)
        #
        #     origin = utils.decode(base64_str[0 : base64_str.index("#")])
        #     remark = base64_str[base64_str.index("#") + 1 :]
        #     security = origin[0 : origin.index(":")]
        #     password = origin[origin.index(":") + 1 : origin.index("@")]
        #     ipandport = origin[origin.index("@") + 1 :]
        #     ip = ipandport[0 : ipandport.index(":")]
        #     port = int(ipandport[ipandport.index(":") + 1 :])
        #     ssode = Shadowsocks(ip, port, remark, security, password)
        #     node = ssode
        if url.startswith("vmess://"):  # vmess
            server_node = json.loads(utils.base64_decode(url.replace("vmess://", "")))
            return V2ray(
                server_node["add"],
                int(server_node["port"]),
                server_node["ps"],
                "auto",
                server_node["id"],
                int(server_node["aid"]),
                server_node["net"],
                server_node["type"],
                server_node["host"],
                server_node["path"],
                server_node["tls"],
            )
    except:
        logger.error(traceback.format_exc())
    return None


def update_v2ray_conf(v2ray_url):
    node = get_node_by_url(v2ray_url)
    if node is None:
        return -1, -1
    json.dump(node.format_config(), open(_v2ray_server.get_conf_path(), "w"), indent=2)
    _v2ray_server.restart()
    logger.info("v2ray 配置已更换为\t{}".format(v2ray_url))


def check_link_alive():
    logger.info("starting check vpn node......")

    c = CheckAlive()
    while True:
        try:
            c.check_all_node()
        except:
            logger.error(traceback.format_exc())
            time.sleep(10)
        finally:
            time.sleep(10)
