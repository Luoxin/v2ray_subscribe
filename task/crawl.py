import json
import random
import time
import traceback
from lxml import etree

import requests

import utils
from conf import global_variable, VariableManager
from orm import SubscribeCrawl, SubscribeVmss
from orm.subscribe_crawl import SubscribeCrawlType
from utils import logger


def add_new_vmess(
    v2ray_url,
    crawl_id: int = 0,
    interval: int = global_variable.get_conf_int("INTERVAL", default=1800),
) -> bool:
    try:
        if v2ray_url == "":
            return False

        # 已经存在了，就不管了
        data = (
            global_variable.get_db()
            .query(SubscribeVmss)
            .filter(SubscribeVmss.url == v2ray_url)
            .first()
        )
        if data is not None:
            if (
                data.death_count is None
                or data.death_count
                < global_variable.get_conf_int("BASE_DEATH_COUNT", default=10)
            ):
                new_db = global_variable.get_db()
                new_db.query(SubscribeVmss).filter(SubscribeVmss.id == data.id).update(
                    {
                        SubscribeVmss.death_count: int(
                            global_variable.get_conf_int("BASE_DEATH_COUNT", default=10)
                            / 2
                        ),
                    }
                )
                new_db.commit()
            return True

        if v2ray_url.startswith("vmess://"):  # vmess
            try:
                logger.debug("new vmess is {}".format(v2ray_url))
                v = json.loads(utils.base64_decode(v2ray_url.replace("vmess://", "")))
                new_db = global_variable.get_db()
                new_db.add(
                    SubscribeVmss(
                        url=v2ray_url,
                        network_protocol_type=""
                        if v.get("net") is None
                        else v.get("net"),
                        death_count=global_variable.get_conf_int(
                            "BASE_DEATH_COUNT", default=10
                        ),
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


def download(data: SubscribeCrawl):
    try:
        proxies = None
        timeout = 10

        if isinstance(data.rule, dict):
            rule = VariableManager(data.rule)
            if rule.get_conf_bool("need_proxy", default=False):
                proxies = global_variable.get_conf_dict(
                    "PROXIES_CRAWLER",
                    default={
                        "http": "socks5://127.0.0.1:10808",
                        "https": "socks5://127.0.0.1:10808",
                    },
                )
            if data.rule.get("timeout"):
                try:
                    timeout = int(data.rule.get("timeout"))
                except:
                    timeout = 10

        try:
            headers = {
                "User-Agent": global_variable.get_user_agent(),
                "Connection": "close",
            }

            rsp = requests.get(
                data.crawl_url, headers=headers, timeout=timeout, proxies=proxies
            )

            if rsp.status_code == 200:
                return rsp.content.decode("utf-8")
        except (
            requests.exceptions.RequestException,
            requests.exceptions.RequestsWarning,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ):
            pass
        except:
            logger.error("err: {}".format(traceback.format_exc()))

    except:
        logger.error("err: {}".format(traceback.format_exc()))

    return None


def analyze(data: SubscribeCrawl, html: str):
    if html is None or html == "":
        return None

    if data.crawl_type == SubscribeCrawlType.Subscription.value:
        try:
            v2ray_url_list = utils.base64_decode(html).split("\n")
            for v2ray_url in v2ray_url_list:
                add_new_vmess(v2ray_url, crawl_id=data.id, interval=data.interval)
        except:
            logger.error("err: {}".format(traceback.format_exc()))

    elif data.crawl_type == SubscribeCrawlType.Xpath.value:
        rule = VariableManager(data.rule)
        soup = etree.HTML(html)
        for result in soup.xpath(rule.get_conf_str("xpath")):
            if not isinstance(result, str) or result.__len__() == 0:
                continue
            try:
                v2ray_url_list = utils.base64_decode(result).split("\n")
                for v2ray_url in v2ray_url_list:
                    add_new_vmess(v2ray_url, crawl_id=data.id, interval=data.interval)
            except:
                logger.error("err: {}".format(traceback.format_exc()))


def get_data_from_network(data: SubscribeCrawl):
    html = download(data)
    if html is not None and isinstance(html, str) and len(html) > 0:
        analyze(data, html)


def crawl_by_subscribe():
    data_list = (
        global_variable.get_db()
        .query(SubscribeCrawl)
        .filter(SubscribeCrawl.next_at <= utils.now())
        .filter(SubscribeCrawl.is_closed == False)
        .all()
    )

    for data in data_list:
        try:
            get_data_from_network(data)
            new_db = global_variable.get_db()
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
    print(utils.base64_decode(v2ray_url.replace("vmess://", "")))
    print(json.loads(utils.base64_decode(v2ray_url.replace("vmess://", ""))))
