import json
import os
import traceback

import requests

import utils
from conf import global_variable, VariableManager
from utils import logger


class NodeTitle(object):
    cache_file_name = ".title.tmp"

    def __init__(self):
        self.url = "https://v1.hitokoto.cn/"
        self._lock = utils.Wlock()

        self.updated_at = 0
        self.title = "真正要分开的两个人，连“分手”二字都是多余的，因为殊途同归。"

        self._update_from_cache()

        pass

    def _update_from_cache(self):
        with utils.acquire(self._lock):
            if self.updated_at == 0 and os.path.exists(NodeTitle.cache_file_name):
                with open(NodeTitle.cache_file_name, "r", encoding="utf-8") as f:
                    cache = VariableManager(json.loads(f.read()))
                    self.title = cache.get_conf_str(
                        "title", "真正要分开的两个人，连“分手”二字都是多余的，因为殊途同归。"
                    )
                    self.updated_at = cache.get_conf_int("updated_at")

            if self.updated_at == 0 or (self.updated_at + 5 * 60) < utils.now():
                title = self._get_from_network()
                if title is not None:
                    self.title = title
                    self.updated_at = utils.now()

                    with open(NodeTitle.cache_file_name, "w", encoding="utf-8") as f:
                        f.write(
                            json.dumps(
                                {"title": self.title, "updated_at": self.updated_at}
                            )
                        )

    def _get_from_network(self):
        try:
            try:
                headers = {
                    "User-Agent": global_variable.get_user_agent(),
                    "Connection": "close",
                }

                rsp = requests.get(self.url, headers=headers, timeout=10, proxies=None)

                if rsp.status_code == 200:
                    return rsp.json().get("hitokoto")
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

    def get(self):
        self._update_from_cache()
        return self.title


if __name__ == "__main__":
    n = NodeTitle()
    print(n.get())
