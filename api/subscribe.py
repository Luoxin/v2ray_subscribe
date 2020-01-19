from flask import Blueprint, request

import utils
from orm import db, SubscribeVmss, or_
from utils import logger  # 日志
from error_exception import create_error_with_msg

subscribe_api = Blueprint("subscribe", __name__)


@subscribe_api.route("/api/subscription", methods=["GET"])
def subscription():
    req = request.args

    new_db = (
        db()
        .query(SubscribeVmss)
        .filter(SubscribeVmss.death_count >= 0)
        .filter(or_(SubscribeVmss.is_closed == False, SubscribeVmss.is_closed == None))
    )

    subscription_site = req.get("site") if "site" in req.keys() else "google"
    subscription_type = req.get("type") if "type" in req.keys() else "delayed"

    if subscription_site == "youtube":
        if subscription_type == "speed":
            new_db = (
                new_db.filter(SubscribeVmss.speed_youtube > 0)
                .filter(SubscribeVmss.network_delay_youtube > 0)
                .order_by(SubscribeVmss.speed_youtube.desc())
                .order_by(SubscribeVmss.network_delay_youtube.desc())
            )
        else:
            new_db = (
                new_db.filter(SubscribeVmss.speed_youtube > 0)
                .filter(SubscribeVmss.network_delay_youtube > 0)
                .order_by(SubscribeVmss.network_delay_youtube.desc())
                .order_by(SubscribeVmss.speed_youtube.desc())
            )
    elif subscription_site == "internet":
        if subscription_type == "speed":
            new_db = (
                new_db.filter(SubscribeVmss.speed_internet > 0)
                .filter(SubscribeVmss.network_delay_internet > 0)
                .order_by(SubscribeVmss.speed_internet.desc())
                .order_by(SubscribeVmss.network_delay_internet.desc())
            )
        else:
            new_db = (
                new_db.filter(SubscribeVmss.network_delay_internet > 0)
                .filter(SubscribeVmss.speed_internet > 0)
                .order_by(SubscribeVmss.network_delay_internet.desc())
                .order_by(SubscribeVmss.speed_youtube.desc())
            )
    else:
        if subscription_type == "speed":
            new_db = (
                new_db.filter(SubscribeVmss.speed_google > 0)
                .filter(SubscribeVmss.network_delay_google > 0)
                .order_by(SubscribeVmss.speed_google.desc())
                .order_by(SubscribeVmss.network_delay_google.desc())
            )
        else:
            new_db = (
                new_db.filter(SubscribeVmss.network_delay_google > 0)
                .filter(SubscribeVmss.speed_google > 0)
                .order_by(SubscribeVmss.network_delay_google.desc())
                .order_by(SubscribeVmss.speed_google.desc())
            )

        can_be_used = new_db.all()
        vmess_list = []
        for subscribe_vmess in can_be_used:
            vmess_list.append(subscribe_vmess.url)

        return utils.base64_encode(("\n".join(vmess_list)))


# def get_alive_url():
#     data_list = (
#         session.query(subscribe_vmss)
#         .filter(subscribe_vmss.speed > 0)
#         .filter(subscribe_vmss.health_points > HEALTH_POINTS)
#         .filter(subscribe_vmss.updated_at >= int(int(time.time()) - 24 * 60 * 60))
#         .order_by(subscribe_vmss.speed.desc())
#         .all()
#     )
#     return data_list


# @app.route("/count")
# def count():
#     return "当前节点数量为 {}</br>其中高速节点数量为 {}</br>可供手机使用的高速节点数量为 {}".format(
#         session.query(subscribe_vmss).count(),
#         session.query(subscribe_vmss).filter(subscribe_vmss.speed > 0).count(),
#         session.query(subscribe_vmss)
#         .filter(subscribe_vmss.speed > 0)
#         .filter(subscribe_vmss.type == "ws")
#         .count(),
#     )


# # 所有的高速节点
# @app.route("/subscription", methods=["GET"])
# def get_all_link_by_max_speed():
#     state, authentication = get_authentication(None, None)
#     if not state:
#         return authentication
#
#     can_be_used = get_alive_url()
#
#     if can_be_used.__len__() == 0:
#         return get_all_link_by_max_speed_by_no_check()
#
#     vmss_list = []
#     for subscribeVmss in can_be_used:
#         vmss_list.append(subscribeVmss.url)
#
#     return base64.b64encode(("\n".join(vmss_list)).encode()).decode()


# @app.route("/subscriptionmp")
# def get_all_link_by_max_speed_by_mobile_phone():
#     state, authentication = get_authentication(None, None)
#     if not state:
#         return authentication
#
#     can_be_used = (
#         session.query(subscribe_vmss)
#         .filter(subscribe_vmss.speed > 0)
#         .filter(subscribe_vmss.health_points > HEALTH_POINTS)
#         .filter(subscribe_vmss.updated_at >= int(int(time.time()) - 24 * 60 * 60))
#         .filter(subscribe_vmss.type == "ws")
#         .order_by(subscribe_vmss.speed.desc())
#         .all()
#     )
#
#     if can_be_used.__len__() == 0:
#         return get_all_link_by_max_speed_by_no_check()
#
#     vmss_list = []
#     for subscribeVmss in can_be_used:
#         vmss_list.append(subscribeVmss.url)
#
#     return base64.b64encode(("\n".join(vmss_list)).encode()).decode()


# @app.route("/subscriptionnc")
# def get_all_link_by_max_speed_by_no_check():
#     state, authentication = get_authentication(None, None)
#     if not state:
#         return authentication
#
#     can_be_used = (
#         session.query(subscribe_vmss)
#         .filter(subscribe_vmss.speed >= 0)
#         .filter(subscribe_vmss.updated_at >= int(time.time() - 60 * 60 * 24))
#         .filter(subscribe_vmss.type == "ws")
#         .order_by(subscribe_vmss.speed.desc())
#         .all()
#     )
#
#     vmss_list = []
#     for subscribeVmss in can_be_used:
#         vmss_list.append(subscribeVmss.url)
#
#     return base64.b64encode(("\n".join(vmss_list)).encode()).decode()


# @app.route("/maxspeed")
# def max_speed():
#     data = session.query(subscribe_vmss).order_by(subscribe_vmss.speed.desc()).first()
#     return "当前最大的速度为：{}kb/s".format(data.speed)


# @app.route("/share")
# def share_new_node():
#     if request.method == "GET":
#         try:
#             url = request.args.get("url")
#         except:
#             return "error args"
#     # TODO POST请求有问题
#     elif request.method == "POST":
#         try:
#             url = request.json.get("url")
#         except:
#             return "error args"
#     else:
#         return "error method"
#     if url is None:
#         return "error args"
#     if re.match(r"(http|https|ss|ssr|vmess)://[\43-\176]*", url):
#         logger.info("new url will be add {}".format(url))
#         add_new_vmess(url)
#         return "success"
#     return "error args"


# @app.route("/shares")
# def share_by_subscription():
#     if request.method == "GET":
#         try:
#             subscription = request.args.get("s")
#             urls = base64.b64decode(subscription.encode()).decode().split("\n")
#         except:
#             return "error args"
#     # TODO POST请求有问题
#     elif request.method == "POST":
#         try:
#             subscription = request.json.get("s")
#             urls = base64.b64decode(subscription.encode()).decode().split("\n")
#         except:
#             return "error args"
#     else:
#         return "error method"
#     if len(urls) == 0:
#         return "error args"
#
#     success_count = 0
#     for url in urls:
#         try:
#             if re.match(r"(http|https|ss|ssr|vmess)://[\43-\176]*", url):
#                 logger.info("new url will be add {}".format(url))
#                 if add_new_vmess(url):
#                     success_count += 1
#         except:
#             logger.error(traceback.format_exc())
#     if success_count == 0:
#         return "all is add already"
#     return "add new node {}".format(success_count)