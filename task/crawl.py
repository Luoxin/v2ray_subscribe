import json
import random
import time
import traceback

import requests
import sqlalchemy.exc
from grab import Grab, GrabNetworkError, GrabTimeoutError, GrabMisuseError, GrabError
from lxml import etree

import utils
from conf import global_variable, VariableManager
from orm import SubscribeCrawl, SubscribeVmss
from orm.subscribe_crawl import SubscribeCrawlType
from utils import logger


class Crawl(object):
    def __init__(
        self,
        interval: int = global_variable.get_conf_int("INTERVAL", default=360),
        proxy: str = global_variable.get_conf_str("PROXIES_CRAWLER", default=None),
        timeout: str = global_variable.get_conf_float("TIMEOUT_CRAWLER", default=5),
        base_death_count: int = global_variable.get_conf_int(
            "BASE_DEATH_COUNT", default=30
        ),
    ):
        self._interval = interval
        self._proxy = proxy
        self._timeout = timeout
        self._base_death_count = base_death_count

    def download(self, u: str, crawl_type: int, rule: dict) -> str:
        try:
            rule = VariableManager(rule)

            g = Grab()
            g.go(
                url=u,
                user_agent=global_variable.get_user_agent(),
                method=rule.get_conf_str("method", None),
                proxy=None if rule.get_conf_bool("need_proxy", False) else self._proxy,
                timeout=self._timeout
                if rule.get_conf_float("timeout", default=0) > 0
                else rule.get_conf_float("timeout", default=0),
            )

            if g.doc is None:
                logger.error("get data none,url:{}".format(u))

            if crawl_type == SubscribeCrawlType.Subscription.value:
                return g.doc.body
            elif crawl_type == SubscribeCrawlType.Xpath.value:
                xpath = rule.get_conf_str("xpath")
                if xpath == "" or len(xpath) == "":
                    logger.error("rule missed xpath, url:{}".format(u))
                    return ""

                return g.doc(xpath).text()
            else:
                logger.error("invalid crawler type {}".format(crawl_type))
                return ""
        except (GrabNetworkError, GrabTimeoutError, GrabMisuseError, GrabError):
            return ""
        except:
            logger.error("err: {}".format(traceback.format_exc()))
            return ""

    def add_new(self, u: str, crawl_id: int = 0) -> bool:
        if u == "":
            return False

        try:
            data = (
                global_variable.get_db()
                .query(SubscribeVmss)
                .filter(SubscribeVmss.url == u)
                .first()
            )

            if data is not None:  # 如果存在
                if (
                    data.death_count is None
                    or data.death_count < self._base_death_count
                ):  # 如果死了，就救活
                    logger.info("rescue node {}".format(u))
                    new_db = global_variable.get_db()
                    new_db.query(SubscribeVmss).filter(
                        SubscribeVmss.id == data.id
                    ).update(
                        {
                            SubscribeVmss.death_count: self._base_death_count,
                            SubscribeVmss.is_closed: False,
                        }
                    )
                    new_db.commit()
                    return True
            else:
                if u.startswith("vmess://"):
                    try:
                        v = json.loads(utils.base64_decode(u.replace("vmess://", "")))

                        logger.info("add new node {}".format(u))

                        new_db = global_variable.get_db()
                        new_db.add(
                            SubscribeVmss(
                                url=u,
                                network_protocol_type=""
                                if v.get("net") is None
                                else v.get("net"),
                                death_count=self._base_death_count,
                                next_at=0,
                                is_closed=False,
                                interval=self._interval,
                                crawl_id=crawl_id,
                                conf_details=v,
                            )
                        )
                        new_db.commit()
                        return True

                    except sqlalchemy.exc.IntegrityError:
                        pass
                    except (UnicodeDecodeError, json.decoder.JSONDecodeError):
                        pass
                    except:
                        logger.error("err: {}".format(traceback.format_exc()))
        except:
            logger.error("err: {}".format(traceback.format_exc()))

        return False

    def crawler(self, task: SubscribeCrawl):
        try:
            data = self.download(
                u=task.crawl_url, crawl_type=task.crawl_type, rule=task.rule
            )
            if data is None or len(data) == 0:
                return

            node_list = utils.base64_decode(data).split("\n")
            for node in node_list:
                self.add_new(node, task.id)

        except:
            logger.error("err: {}".format(traceback.format_exc()))

    def crawl_all(self):
        task_list = (
            global_variable.get_db()
            .query(SubscribeCrawl)
            .filter(SubscribeCrawl.next_at <= utils.now())
            .filter(SubscribeCrawl.is_closed == False)
            .all()
        )

    def crawl_by_subscribe(self):
        task_list = (
            global_variable.get_db()
            .query(SubscribeCrawl)
            .filter(SubscribeCrawl.next_at <= utils.now())
            .filter(SubscribeCrawl.is_closed == False)
            .all()
        )

        for task in task_list:
            try:
                self.crawler(task=task)

                if task.interval is None or task.interval == 0:
                    task.interval = self._interval

                new_db = global_variable.get_db()
                new_db.query(SubscribeCrawl).filter(
                    SubscribeCrawl.id == task.id
                ).update(
                    {
                        SubscribeCrawl.next_at: int(
                            random.uniform(0.5, 1.5) * task.interval + utils.now()
                        )
                    }
                )
                new_db.commit()
            except:
                logger.error("err: {}".format(traceback.format_exc()))
            finally:
                logger.info("{}抓取更新已完成".format(task.crawl_url))


def crawler_node():
    logger.info("starting crawl node...")

    crawl = Crawl()

    while True:
        try:
            crawl.crawl_all()
        except:
            logger.error("err: {}".format(traceback.format_exc()))
        finally:
            time.sleep(60)
