import json
import os
import random
import sys
import time
import traceback
from conf import global_variable
import requests

import utils
from orm import SubscribeVmss, or_
from task.node import V2ray
from task.proxy_server import V2rayServer
from utils import logger

v2ray_server = V2rayServer(
    os.path.join(global_variable.get_conf_str("V2RAY_SERVICE_PATH",
                                              default="C:/ProgramData/v2ray" if sys.platform == "win" else "/usr/bin/v2ray"),
                 "v2ray"),
    os.path.join(global_variable.get_conf_str("V2RAY_SERVICE_PATH",
                                              default="C:/ProgramData/v2ray" if sys.platform == "win" else "/usr/bin/v2ray"),
                 "v2ray_subscribe.conf"),
)


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


def check_by_v2ray_url(test_url: str):
    try:
        try:
            headers = {
                "Connection": "close",
                "User-Agent": global_variable.get_user_agent(),
            }
            start_time = time.time()
            r = requests.get(
                url=test_url,
                proxies={
                    "http": "socks5://127.0.0.1:{}".format(global_variable.get_conf_int("CHECK_PORT", default=1080)),
                    "https": "socks5://127.0.0.1:{}".format(global_variable.get_conf_int("CHECK_PORT", default=1080)),
                },
                timeout=10,
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

        logger.info("{}kb/s({} ms)\t测试连接{}".format(speed, network_delay, test_url))
        return float(speed), float(network_delay)
    except:
        logger.error(traceback.format_exc())
        return -1, -1


def check_link_alive_by_google(data: SubscribeVmss):
    try:
        speed, network_delay = check_by_v2ray_url("https://www.google.com/")

        new_db = global_variable.get_db()
        new_db.query(SubscribeVmss).filter(SubscribeVmss.id == data.id).update(
            {
                SubscribeVmss.speed_google: speed,
                SubscribeVmss.network_delay_google: network_delay,
            }
        )
        new_db.commit()
        return True if speed >= 0 else False
    except:
        logger.error(traceback.format_exc())
        return False


def check_link_alive_by_youtube(data: SubscribeVmss):
    try:
        speed, network_delay = check_by_v2ray_url("https://www.youtube.com/")
        new_db = global_variable.get_db()
        new_db.query(SubscribeVmss).filter(SubscribeVmss.id == data.id).update(
            {
                SubscribeVmss.speed_youtube: speed,
                SubscribeVmss.network_delay_youtube: network_delay,
            }
        )
        new_db.commit()
        return True if speed >= 0 else False
    except:
        logger.error(traceback.format_exc())
        return False


def check_link_alive_by_internet(data: SubscribeVmss):
    try:
        speed, network_delay = check_by_v2ray_url(
            "http://cachefly.cachefly.net/1mb.test"
        )

        new_db = global_variable.get_db()
        new_db.query(SubscribeVmss).filter(SubscribeVmss.id == data.id).update(
            {
                SubscribeVmss.speed_internet: speed,
                SubscribeVmss.network_delay_internet: network_delay,
            }
        )
        new_db.commit()
        return True if speed >= 0 else False
    except:
        logger.error(traceback.format_exc())
        return False


def update_v2ray_conf(v2ray_url):
    node = get_node_by_url(v2ray_url)
    if node is None:
        return -1, -1
    json.dump(node.format_config(), open(v2ray_server.get_conf_path(), "w"), indent=2)
    v2ray_server.restart()
    logger.info("v2ray 配置已更换为\t{}".format(v2ray_url))


def check_link_alive():
    logger.info("starting check vpn node......")
    while True:
        try:
            data_list = (
                global_variable.get_db()
                    .query(SubscribeVmss)
                    .filter(
                    or_(
                        SubscribeVmss.death_count < global_variable.get_conf_int("MAX_DEATH_COUNT"),
                        SubscribeVmss.death_count == None,
                    )
                )
                    .filter(
                    or_(
                        SubscribeVmss.next_at < int(time.time()),
                        SubscribeVmss.next_at == None,
                    )
                )
                    .order_by(SubscribeVmss.next_at)
                    .all()
            )
            if len(data_list) <= 0:
                logger.debug("暂时没有待检测节点")
                time.sleep(20)
                continue

            else:
                for i, data in enumerate(data_list):
                    try:
                        update_v2ray_conf(data.url)
                        death_count = data.death_count

                        alive = (
                                check_link_alive_by_google(data)
                                + check_link_alive_by_youtube(data)
                                + check_link_alive_by_internet(data)
                        )

                        if alive <= 0:
                            death_count -= 3 - alive
                        else:
                            if death_count < 0:
                                death_count = 0
                            death_count += alive

                        new_db = global_variable.get_db()
                        new_db.query(SubscribeVmss).filter(
                            SubscribeVmss.id == data.id
                        ).update(
                            {
                                SubscribeVmss.next_at: int(
                                    random.uniform(0.5, 1.5) * data.interval
                                )
                                                       + int(time.time()),
                                SubscribeVmss.death_count: death_count,
                            }
                        )
                        new_db.commit()
                    except:
                        logger.error(traceback.format_exc())
                    finally:
                        time.sleep(5)
                        # logger.info("第{}个节点监测完成".format(i+1))
                logger.debug("{}个节点检测完成".format(i + 1))
        except:
            logger.error(traceback.format_exc())
            time.sleep(10)
        finally:
            time.sleep(10)
