import json
import random
import time
import traceback

from playhouse.shortcuts import model_to_dict, dict_to_model

from utils import logger, base64_decode

import requests

import utils
from conf.conf import get_conf, user_agent, get_conf_int
from orm import SubscribeCrawl, SubscribeVmss, db
from orm.subscribe_crawl import SubscribeCrawlType


def add_new_vmess(v2ray_url, crawl_id: int = 0, interval: int = 60 * 60) -> bool:
    try:
        if v2ray_url == "":
            return False

        # 已经存在了，就不管了
        data = db().query(SubscribeVmss).filter(SubscribeVmss.url == v2ray_url).first()
        if data is not None:
            if data.death_count is None or data.death_count < get_conf_int(
                "MAX_DEATH_COUNT"
            ):
                new_db = db()
                new_db.query(SubscribeVmss).filter(SubscribeVmss.id == data.id).update(
                    {
                        SubscribeVmss.death_count: int(
                            int(get_conf_int("MAX_DEATH_COUNT")) / 2
                        ),
                    }
                )
                new_db.commit()
            return True

        if v2ray_url.startswith("vmess://"):  # vmess
            try:
                logger.debug("new vmess is {}".format(v2ray_url))
                v = json.loads(base64_decode(v2ray_url.replace("vmess://", "")))
                new_db = db()
                new_db.add(
                    SubscribeVmss(
                        url=v2ray_url,
                        network_protocol_type=""
                        if v.get("net") is None
                        else v.get("net"),
                        death_count=0,
                        next_at=0,
                        is_closed=False,
                        interval=int(interval),
                        crawl_id=int(crawl_id),
                        conf_details=v,
                    )
                )
                new_db.commit()
            except (UnicodeDecodeError, json.decoder.JSONDecodeError):
                pass
            except:
                logger.error("err: {}".format(traceback.format_exc()))
                return False
    except:
        logger.error("err: {}".format(traceback.format_exc()))
    return False


def crawl_by_subscribe_url(data: SubscribeCrawl):
    try:
        proxies = None
        if isinstance(data.rule, dict):
            if data.rule.get("need_proxy"):
                proxies = get_conf("PROXIES_CRAWLER")

        try:
            headers = {
                "User-Agent": user_agent.random,
                "Connection": "close",
            }
            v2ray_url_list = base64_decode(
                requests.get(
                    data.crawl_url, headers=headers, timeout=10, proxies=proxies
                ).text
            ).split("\n")
            for v2ray_url in v2ray_url_list:
                add_new_vmess(v2ray_url, crawl_id=data.id, interval=data.interval)
        except (
            requests.exceptions.RequestException,
            requests.exceptions.RequestsWarning,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ):
            return
        except:
            logger.error("err: {}".format(traceback.format_exc()))

    except:
        logger.error("err: {}".format(traceback.format_exc()))


def crawl_by_subscribe():
    data_list = (
        db()
        .query(SubscribeCrawl)
        .filter(SubscribeCrawl.next_at <= utils.now())
        .filter(SubscribeCrawl.is_closed == False)
        .filter(SubscribeCrawl.crawl_type == SubscribeCrawlType.Subscription.value)
        .all()
    )

    for data in data_list:
        try:
            crawl_by_subscribe_url(data)
            new_db = db()
            new_db.query(SubscribeCrawl).filter(SubscribeCrawl.id == data.id).update(
                {
                    SubscribeCrawl.next_at: int(
                        random.uniform(0.5, 1.5) * data.interval + utils.now()
                    )
                }
            )
            new_db.commit()
        except:
            traceback.print_exc()

    logger.debug("已经完成了\t{}\t个订阅节点的更新".format(len(data_list)))


def update_new_node():
    logger.info("starting crawl vpn node...")
    while True:
        try:
            # 对订阅类型的进行抓取
            crawl_by_subscribe()

            # if (last_update_info.get("free-ss-443") is not None) and ((last_update_info.get("free-ss-443") > now)
            # or (last_update_info.get("free-ss-443") == 0)): try: v2ray_conf =
            # "ew0KICAidiI6ICIyIiwNCiAgInBzIjogIltmcmVlLXNzLnNpdGVdd3d3Lmtlcm5lbHMuYmlkIiwNCiAgImFkZCI6ICJ3d3cua2VybmVscy
            # 5iaWQiLA0KICAicG9ydCI6ICI0NDMiLA0KICAiaWQiOiAiYmZmNDA0YmItZTFjMy02MTU4LTY4MDAtOTRmMTk2MTQwNzY5IiwNCiAgImFpZ
            # CI6ICIwIiwNCiAgIm5ldCI6ICJ3cyIsDQogICJ0eXBlIjogIm5vbmUiLA0KICAiaG9zdCI6ICIiLA0KICAicGF0aCI6ICIvd3MiLA0KICAi
            # dGxzIjogInRscyINCn0=" v2ray_conf = base64.b64decode(v2ray_conf.encode()).decode()
            #
            # url = "https://free-ss.site/v/443.json" data = requests.get(url, timeout=10, proxies=proxies).json() id
            # = data.get("outbounds")[0].get("settings").get("vnext")[0].get("users")[0].get("id") v2ray_url =
            # "vmess://" + base64.b64encode(v2ray_conf.replace("bff404bb-e1c3-6158-6800-94f196140769", id).encode(
            # )).decode() today8 = datetime.datetime.now().replace(hour=8, minute=0, second=0,
            # microsecond=0).timestamp() today20 = datetime.datetime.now().replace(hour=20, minute=0, second=0,
            # microsecond=0).timestamp() if now < today8: dead_time = today8 elif now < today20: dead_time = today20
            # else: dead_time = (datetime.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0) +
            # datetime.timedelta(days=1)).timestamp() dead_time = int(dead_time) logger.info("free-ss-443 的下次更新时间为 {
            # }".format(dead_time)) add_new_node(v2ray_url, 0, dead_time=dead_time) last_update_info["free-ss-443"] =
            # dead_time except: traceback.print_exc()
            #
            # if (last_update_info.get("free-ss-80") is not None) and ((last_update_info.get("free-ss-80") > now) or
            # (last_update_info.get("free-ss-80") == 0)): try: v2ray_conf =
            # "ew0KICAidiI6ICIyIiwNCiAgInBzIjogIltmcmVlLXNzLnNpdGVdd3d3Lmtlcm5lbHMuYmlkIiwNCiAgImFkZCI6ICJ3d3cua2VybmVsc
            # y5iaWQiLA0KICAicG9ydCI6ICI4MCIsDQogICJpZCI6ICIxMTQ2MjYxYi1kOTE4LWJjZGYtMmRiMy00YzdlZmY4Y2JmZjIiLA0KICAiYWl
            # kIjogIjAiLA0KICAibmV0IjogIndzIiwNCiAgInR5cGUiOiAibm9uZSIsDQogICJob3N0IjogIiIsDQogICJwYXRoIjogIi93cyIsDQogI
            # CJ0bHMiOiAibm9uZSINCn0=" v2ray_conf = base64.b64decode(v2ray_conf.encode()).decode()
            #
            # url = "https://free-ss.site/v/80.json" data = requests.get(url, timeout=10, proxies=proxies).json() id
            # = data.get("outbounds")[0].get("settings").get("vnext")[0].get("users")[0].get("id") v2ray_url =
            # "vmess://" + base64.b64encode(v2ray_conf.replace("1146261b-d918-bcdf-2db3-4c7eff8cbff2", id).encode(
            # )).decode()
            #
            # today8 = datetime.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0).timestamp() today20
            # = datetime.datetime.now().replace(hour=20, minute=0, second=0, microsecond=0).timestamp() if now <
            # today8: dead_time = today8 elif now < today20: dead_time = today20 else: dead_time = (
            # datetime.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0) + datetime.timedelta(
            # days=1)).timestamp() dead_time = int(dead_time) logger.info("free-ss-80 的下次更新时间为 {}".format(dead_time))
            # add_new_node(v2ray_url, 0, dead_time=dead_time) last_update_info["free-ss-80"] = dead_time except:
            # traceback.print_exc()

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
        except:
            logger.error("err: {}".format(traceback.format_exc()))
        finally:
            time.sleep(60)


if __name__ == "__main__":
    v2ray_url = "vmess://Y2hhY2hhMjAtcG9seTEzMDU6OTUxMzc4NTctNzBmYS00YWM4LThmOTAtNGUyMGFlYjY2MmNmQHVuaS5raXRzdW5lYmkuZnVuOjQ0Mw==?network=h2&h2Path=/v2&aid=0&tls=1&allowInsecure=0&tlsServer=uni.kitsunebi.fun&mux=0&muxConcurrency=8&remark=H2%20Test%20Outbound"
    print(base64_decode(v2ray_url.replace("vmess://", "")))
    print(json.loads(base64_decode(v2ray_url.replace("vmess://", ""))))
