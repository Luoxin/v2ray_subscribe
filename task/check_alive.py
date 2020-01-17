import json
import random
import sys
import time
import traceback
import requests

import utils
from conf.conf import get_conf, user_agent
from node import V2ray
from orm import SubscribeVmss
from proxy_server import V2rayServer
from utils import logger


class CheckAlive:
    def __init__(self):
        self.v2ray_server = V2rayServer(
            get_conf("V2RAY_SERVICE_PATH"), get_conf("V2RAY_CONFIG_LOCAL")
        )
        self.v2ray_config_local_path = get_conf("V2RAY_CONFIG_LOCAL")
        self.proxies = get_conf("PROXIES_TEST")
        self.ua = user_agent

        if self.v2ray_config_local_path is None:
            raise Exception("miss v2ray config local path")

    def check_link_alive(self):
        while True:
            try:
                data_list = (
                    SubscribeVmss.select()
                    .where(SubscribeVmss.next_at < utils.now())
                    .where(SubscribeVmss.is_closed == False)
                )
                for i, data in enumerate(data_list):
                    try:
                        speed, network_delay = self.check_by_v2ray_url(data.url, "")
                        SubscribeVmss.update(
                            next_at=random.uniform(0.5, 1.5) * data.interval
                            + utils.now(),
                        ).where(SubscribeVmss.id == data.id).execute()
                    except:
                        logger.error(traceback.format_exc())
                    finally:
                        time.sleep(5)
                        # logger.info("第{}个节点监测完成".format(i+1))

                logger.info("{}个节点检测完成".format(i + 1))
                del i
            except:
                logger.error(traceback.format_exc())
                time.sleep(10)
            finally:
                # logger.info("节点检测完成")
                time.sleep(10)

    def get_node_by_url(self, url: str != ""):
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
                server_node = json.loads(utils.decode(url.replace("vmess://", "")))
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
            logger.error("err: {}".format(traceback.format_exc()))
        return None

    def check_by_v2ray_url(self, url: str, test_url: str):
        try:
            if url == "" or test_url == "":
                return 0

            node, node_type = self.get_node_by_url(url)
            if node is None:
                return 0
            json.dump(
                node.format_config(), open(self.v2ray_config_local_path, "w"), indent=2
            )
            self.v2ray_server.restart()

            try:
                start_time = time.time()
                r = requests.get(
                    test_url,
                    proxies=self.proxies,
                    timeout=1 * 1000,
                    headers={"Connection": "close", "User-Agent": self.ua.random,},
                )
                if r.status_code == 200:
                    # speed = r.elapsed.microseconds / 1000 / 1000 // 请求的延时
                    request_time = time.time() - start_time
                    del start_time
                    size = sys.getsizeof(r.content) / 1024
                    network_delay = r.elapsed.microseconds / 1000 / 1000
                    speed = size / (request_time - network_delay)
                else:
                    speed = 0
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

            logger.info("\t{}kb/s\t{}\tms\t连接\t{}".format(speed, network_delay, url))
            # subprocess.call('mv ' + V2RAY_CONFIG_LOCAL + '.bak ' + V2RAY_CONFIG_LOCAL, shell=True)
            return float(speed), float(network_delay)
        except:
            logger.error(traceback.format_exc())

        return -1, -1
