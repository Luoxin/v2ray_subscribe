import base64
import re
import traceback
from threading import Thread

from flask import Flask, request
from werkzeug.wrappers import json

from check_alive import check_link_alive
from conf.conf import *
from crawl import init, update_new_node, add_new_vmess
from log import logger
from orm import session, SubscribeVmss

app = Flask(__name__)


def get_alive_url_list_by_speed(speed:(int, float)):
    data_list = session.query(SubscribeVmss).filter(SubscribeVmss.speed > speed).filter(SubscribeVmss.health_points >= 0).all()
    return data_list


@app.route("/count")
def count():
    return "当前节点数量为 {}</br>其中高速节点数量为 {}</br>可供手机使用的高速节点数量为 {}".format(
        session.query(SubscribeVmss).count(),
        session.query(SubscribeVmss).filter(SubscribeVmss.speed > 0).count(),
        session.query(SubscribeVmss).filter(SubscribeVmss.speed > 0).filter(SubscribeVmss.type == "ws").count()
    )


# 所有的高速节点
@app.route("/subscription")
def get_all_link_by_max_speed():
    base_speed = BASE_SPEED
    can_be_used = []
    while (base_speed >= 0) and (can_be_used.__len__() <= 0):
        can_be_used = get_alive_url_list_by_speed(base_speed)
        base_speed -= 1000

    vmss_list = []
    for subscribeVmss in can_be_used:
        vmss_list.append(subscribeVmss.url)

    return base64.b64encode(("\n".join(vmss_list)).encode()).decode()


# 手机使用的连接
@app.route("/subscriptionmp")
def get_all_link_by_max_speed_by_mobile_phone():
    base_speed = BASE_SPEED
    can_be_used = []
    while (base_speed >= 0) and (can_be_used.__len__() <= 0):
        can_be_used = session.query(SubscribeVmss).filter(SubscribeVmss.speed > base_speed).filter(SubscribeVmss.health_points >= 0).filter(SubscribeVmss.type == "ws").all()
        base_speed -= 1000

    vmss_list = []
    for subscribeVmss in can_be_used:
        vmss_list.append(subscribeVmss.url)

    return base64.b64encode(("\n".join(vmss_list)).encode()).decode()

@app.route("/maxspeed")
def max_speed():
    data = session.query(SubscribeVmss).order_by(SubscribeVmss.speed.desc()).first()
    return "当前最大的速度为：{}kb/s</br>{}".format(data.speed, data.url)


@app.route("/share")
def share_new_node():
    if request.method == "GET":
        try:
            url = request.args.get("url")
        except:
            return "error args"
    # TODO POST请求有问题
    elif request.method == "POST":
        try:
            url = request.json.get("url")
        except:
            return "error args"
    else:
        return "error method"
    if url is None:
        return "error args"
    if re.match(r'(http|https|ss|ssr|vmess)://[\43-\176]*', url):
        logger.info("new url will be add {}".format(url))
        add_new_vmess(url)
        return "success"
    return "error args"


@app.route("/shares")
def share_by_subscription():
    urls = []
    if request.method == "GET":
        try:
            subscription = request.args.get("s")
            urls = base64.b64decode(subscription.encode()).decode().split("\n")
        except:
            return "error args"
    # TODO POST请求有问题
    elif request.method == "POST":
        try:
            subscription = request.json.get("s")
            urls = base64.b64decode(subscription.encode()).decode().split("\n")
        except:
            return "error args"
    else:
        return "error method"
    if len(urls) == 0:
        return "error args"

    success_count = 0
    for url in urls:
        try:
            if re.match(r'(http|https|ss|ssr|vmess)://[\43-\176]*', url):
                logger.info("new url will be add {}".format(url))
                if add_new_vmess(url):
                    success_count += 1
        except:
            logger.error(traceback.format_exc())
    if success_count == 0:
        return "all is add already"
    return "add new node {}".format(success_count)


init()
update = Thread(None, update_new_node, None, )
update.daemon = True
update.start()
check_alive = Thread(None, check_link_alive, None, )
check_alive.daemon = True
check_alive.start()
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=FLASK_DEBUG)
