import base64
import json
import random
import time
import traceback

import requests

import utils
from conf.conf import HEALTH_POINTS, Interval
from log import logger
from memory_cache import MemoryCache
from orm import session, SubscribeVmss, SubscribeCrawl

from fake_useragent import UserAgent

ua = UserAgent()


def add_new_vmess(v2ray_url, crawl_id=0) -> bool:
    try:
        if v2ray_url == "":
            return
        data = session.query(SubscribeVmss).filter(SubscribeVmss.url == v2ray_url).first()
        if data is None:
            url_type = ""
            if v2ray_url.startswith('vmess://'):  # vmess
                try:
                    v = json.loads(base64.b64decode(v2ray_url.replace('vmess://', '').encode()).decode())
                    url_type = "" if v.get("net") is None else v.get("net")
                except:
                    pass
            elif v2ray_url.startswith('ss://'):
                pass
            else:  # 把不能被 v2ray 客户端使用的链接过滤掉
                return False

            new_data = SubscribeVmss(
                url=v2ray_url,
                speed=0,
                health_points=HEALTH_POINTS,
                next_time=0,
                interval=Interval,
                created_at=int(time.time()),
                updated_at=int(time.time()),
                type=url_type,
                crawl_id=crawl_id,
            )
            session.add(new_data)
            session.commit()
            return True
        elif data.health_points < HEALTH_POINTS:
            # 如果速度小于0，则更正其速度为 0 以加入测速列表
            if data.speed < 0:
                data.speed = 0

            session.query(SubscribeVmss).filter(SubscribeVmss.id == data.id).update({
                SubscribeVmss.health_points: HEALTH_POINTS,
                SubscribeVmss.updated_at: int(time.time()),
                SubscribeVmss.speed: data.speed,
                SubscribeVmss.crawl_id: crawl_id,
            })
    except:
        logger.error(traceback.format_exc())
        logger.error()
    return False


def crawl_by_subscribe_url(url: str, crawl_id=0):
    headers = {
        "User-Agent": ua.random,
        'Connection': 'close',
    }
    re_text = ""
    try:
        re = requests.get(url, headers=headers, timeout=10)
        re_text = re.text
        try:
            data = base64.b64decode(re_text.encode()).decode()
        except:
            data = utils.decode(re_text)

        for v2ray_url in data.split("\n"):
            add_new_vmess(v2ray_url, crawl_id)

        re.close()
    except:
        logger.error("结果解码失败 {}".format(re_text))
        logger.error("抓取的地址为 {}".format(url))
        logger.error(traceback.format_exc())


def crawl_by_subscribe():
    data_list = session.query(SubscribeCrawl). \
        filter(SubscribeCrawl.next_time <= int(time.time())). \
        filter(SubscribeCrawl.is_closed == False). \
        filter(SubscribeCrawl.type == 1). \
        all()

    for data in data_list:
        try:
            crawl_by_subscribe_url(data.url, data.id)
            session.query(SubscribeCrawl).filter(SubscribeCrawl.id == data.id).update({
                SubscribeCrawl.next_time: int(random.uniform(0.5, 1.5) * data.interval) + int(time.time()),
                SubscribeCrawl.updated_at: int(time.time()),
            })
            session.commit()
        except:
            traceback.print_exc()

    logger.info("已经获取了 {} 个".format(len(data_list)))


# TODO 迁移cache的update_node到数据库
cache = MemoryCache(ttl=7 * 24 * 60 * 60, max_size=5 * 1024 * 1024)


# def init():
#     global cache
#     domain_weight = {
#         "free-ss-443": 5,
#         "free-ss-80": 5,
#         "freev2ray": 1,
#         "kitsunebi_sub": 1,
#         "jiang.netlify": 1,
#         "muma16fx.netlify": 1,
#         "youlianboshi.netlify": 1,
#         "heikejilaila.xyz": 1,
#     }
#     update_node = cache.get_node("update_node")
#     if isinstance(update_node, dict):
#         for domain in domain_weight.keys():
#             if update_node.get(domain) is not None:
#                 update_node[domain] = 0
#     else:
#         logger.info("初始化 update_node")
#         update_node = {}
#         for domain in domain_weight.keys():
#             update_node[domain] = 0
#     cache.add_node("update_node", update_node)
#
#     logger.info("初始化完成")


def update_new_node():
    while True:
        try:
            # 对订阅类型的进行抓取
            crawl_by_subscribe()

            # if (last_update_info.get("free-ss-443") is not None) and ((last_update_info.get("free-ss-443") > now) or (last_update_info.get("free-ss-443") == 0)):
            #     try:
            #         v2ray_conf = "ew0KICAidiI6ICIyIiwNCiAgInBzIjogIltmcmVlLXNzLnNpdGVdd3d3Lmtlcm5lbHMuYmlkIiwNCiAgImFkZCI6ICJ3d3cua2VybmVscy5iaWQiLA0KICAicG9ydCI6ICI0NDMiLA0KICAiaWQiOiAiYmZmNDA0YmItZTFjMy02MTU4LTY4MDAtOTRmMTk2MTQwNzY5IiwNCiAgImFpZCI6ICIwIiwNCiAgIm5ldCI6ICJ3cyIsDQogICJ0eXBlIjogIm5vbmUiLA0KICAiaG9zdCI6ICIiLA0KICAicGF0aCI6ICIvd3MiLA0KICAidGxzIjogInRscyINCn0="
            #         v2ray_conf = base64.b64decode(v2ray_conf.encode()).decode()
            #
            #         url = "https://free-ss.site/v/443.json"
            #         data = requests.get(url, timeout=10, proxies=proxies).json()
            #         id = data.get("outbounds")[0].get("settings").get("vnext")[0].get("users")[0].get("id")
            #         v2ray_url = "vmess://" + base64.b64encode(v2ray_conf.replace("bff404bb-e1c3-6158-6800-94f196140769", id).encode()).decode()
            #         today8 = datetime.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0).timestamp()
            #         today20 = datetime.datetime.now().replace(hour=20, minute=0, second=0, microsecond=0).timestamp()
            #         if now < today8:
            #             dead_time = today8
            #         elif now < today20:
            #             dead_time = today20
            #         else:
            #             dead_time = (datetime.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)).timestamp()
            #         dead_time = int(dead_time)
            #         logger.info("free-ss-443 的下次更新时间为 {}".format(dead_time))
            #         add_new_node(v2ray_url, 0, dead_time=dead_time)
            #         last_update_info["free-ss-443"] = dead_time
            #     except:
            #         traceback.print_exc()
            #
            # if (last_update_info.get("free-ss-80") is not None) and ((last_update_info.get("free-ss-80") > now) or (last_update_info.get("free-ss-80") == 0)):
            #     try:
            #         v2ray_conf = "ew0KICAidiI6ICIyIiwNCiAgInBzIjogIltmcmVlLXNzLnNpdGVdd3d3Lmtlcm5lbHMuYmlkIiwNCiAgImFkZCI6ICJ3d3cua2VybmVscy5iaWQiLA0KICAicG9ydCI6ICI4MCIsDQogICJpZCI6ICIxMTQ2MjYxYi1kOTE4LWJjZGYtMmRiMy00YzdlZmY4Y2JmZjIiLA0KICAiYWlkIjogIjAiLA0KICAibmV0IjogIndzIiwNCiAgInR5cGUiOiAibm9uZSIsDQogICJob3N0IjogIiIsDQogICJwYXRoIjogIi93cyIsDQogICJ0bHMiOiAibm9uZSINCn0="
            #         v2ray_conf = base64.b64decode(v2ray_conf.encode()).decode()
            #
            #         url = "https://free-ss.site/v/80.json"
            #         data = requests.get(url, timeout=10, proxies=proxies).json()
            #         id = data.get("outbounds")[0].get("settings").get("vnext")[0].get("users")[0].get("id")
            #         v2ray_url = "vmess://" + base64.b64encode(v2ray_conf.replace("1146261b-d918-bcdf-2db3-4c7eff8cbff2", id).encode()).decode()
            #
            #         today8 = datetime.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0).timestamp()
            #         today20 = datetime.datetime.now().replace(hour=20, minute=0, second=0, microsecond=0).timestamp()
            #         if now < today8:
            #             dead_time = today8
            #         elif now < today20:
            #             dead_time = today20
            #         else:
            #             dead_time = (datetime.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)).timestamp()
            #         dead_time = int(dead_time)
            #         logger.info("free-ss-80 的下次更新时间为 {}".format(dead_time))
            #         add_new_node(v2ray_url, 0, dead_time=dead_time)
            #         last_update_info["free-ss-80"] = dead_time
            #     except:
            #         traceback.print_exc()

            # if (last_update_info.get("freev2ray") is not None) and (
            #         (last_update_info.get("freev2ray") > now) or (last_update_info.get("freev2ray") == 0)):
            #     try:
            #         url = "https://xxx.freev2ray.org/"
            #         data = requests.get(url, timeout=10).text
            #
            #         soup = etree.HTML(data)
            #         v2ray_url = (
            #             soup.xpath('//*[@id="intro"]/div/div/footer/ul[1]/li[2]/button/@data-clipboard-text')[0])
            #         add_new_vmess(v2ray_url)
            #     except:
            #         traceback.print_exc()
            #     finally:
            #         last_update_info["freev2ray"] = now + int(random.uniform(0.5, 1.5) * 60 * 60) + int(time.time())

        finally:
            logger.info("更新节点完成")
            time.sleep(60)
