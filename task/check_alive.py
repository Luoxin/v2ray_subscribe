import json
import random
import sys
import time
import traceback
import urllib

import requests
import utils
from node import V2ray, Shadowsocks
from orm import SubscribeVmss, db
from proxy_server import V2rayServer
from conf.conf import user_agent, get_conf
from utils import logger

v2ray_server = V2rayServer(
    get_conf("V2RAY_SERVICE_PATH"), get_conf("V2RAY_CONFIG_LOCAL")
)


def get_node_by_url(url: str != ""):
    node = None
    node_type = ""
    try:
        if url.startswith("ss://"):  # ss node
            node_type = "ss"
            base64_str = url.replace("ss://", "")
            base64_str = urllib.parse.unquote(base64_str)

            origin = utils.decode(base64_str[0 : base64_str.index("#")])
            remark = base64_str[base64_str.index("#") + 1 :]
            security = origin[0 : origin.index(":")]
            password = origin[origin.index(":") + 1 : origin.index("@")]
            ipandport = origin[origin.index("@") + 1 :]
            ip = ipandport[0 : ipandport.index(":")]
            port = int(ipandport[ipandport.index(":") + 1 :])
            ssode = Shadowsocks(ip, port, remark, security, password)
            node = ssode
        elif url.startswith("vmess://"):  # vmess
            node_type = "v2ray"
            base64_str = url.replace("vmess://", "")
            jsonstr = utils.decode(base64_str)

            server_node = json.loads(jsonstr)
            v2node = V2ray(
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
            node = v2node
    finally:
        return node, node_type


def check_by_v2ray_url(url: str):
    try:
        node, node_type = get_node_by_url(url)
        if node is None:
            return 0
        json.dump(
            node.format_config(), open(get_conf("V2RAY_CONFIG_LOCAL"), "w"), indent=2
        )
        v2ray_server.restart()
        try:
            headers = {
                "Connection": "close",
                "User-Agent": user_agent.random,
            }
            start_time = time.time()
            r = requests.get(
                proxies=get_conf("PROXIES_TEST"), timeout=10, headers=headers,
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

        logger.info("\t{}kb/s\t连接\t{}".format(speed, url))
        # subprocess.call('mv ' + V2RAY_CONFIG_LOCAL + '.bak ' + V2RAY_CONFIG_LOCAL, shell=True)
        return float(speed), float(network_delay)
    except:
        logger.error(traceback.format_exc())
        return -1, -1


def check_link_alive():
    while True:
        try:
            data_list = (
                db.query(SubscribeVmss)
                .filter(SubscribeVmss.next_at < int(time.time()))
                .order_by(SubscribeVmss.speed.desc())
                .all()
            )
            # filter(SubscribeVmss.last_state.notin_(1)). \
            if len(data_list) <= 0:
                # logger.info("暂时没有待检测节点")
                time.sleep(20)
                continue

            else:
                for i, data in enumerate(data_list):
                    try:
                        speed, network_delay = check_by_v2ray_url(data.url)
                        if speed >= 0:
                            db.query(SubscribeVmss).filter(
                                SubscribeVmss.id == data.id
                            ).update(
                                {
                                    SubscribeVmss.next_at: int(
                                        random.uniform(0.5, 1.5) * data.interval
                                    )
                                    + int(time.time()),
                                    SubscribeVmss.death_count: 0,
                                }
                            )
                        else:
                            db.query(SubscribeVmss).filter(
                                SubscribeVmss.id == data.id
                            ).update(
                                {
                                    SubscribeVmss.next_at: int(
                                        random.uniform(0.5, 1.5) * data.interval
                                    )
                                    + int(time.time()),
                                    SubscribeVmss.death_count: data.death_count + 1,
                                }
                            )
                        db.commit()
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
