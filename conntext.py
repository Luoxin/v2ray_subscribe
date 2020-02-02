import traceback

from flask import request, jsonify
from werkzeug._compat import integer_types, text_type
from werkzeug.datastructures import Headers
from werkzeug.utils import get_content_type
from werkzeug.wrappers import Response

from utils import logger, json  # 日志


class ServiceResponse(object):
    def __init__(self, response=None):
        if response is None or isinstance(response, dict):
            self.response = json.dumps({"data": {}, "errcode": 0, "errmsg": ""})
        else:
            self.response = response

    def get_data(self):
        return self.response


def before_request():
    if request.path == "/favicon.ico":
        return

    method = request.method

    # 获取请求参数
    request_message = ""
    if method == "GET":
        request_message = request.args.to_dict()
    elif method == "POST":
        if request.json is not None:
            request_message = request.json
        elif request.form is not None:
            request_message = request.form

    # 获取请求用户的真实ip地址
    real_ip = request.remote_addr
    if request.headers.get("X-Forwarded-For") is not None:
        real_ip = request.headers.get("X-Forwarded-For")

    # if request.path == "/api/subscribe/subscription":
    #     req = request.args
    #     secret_key = req.get("key")
    #     uuid = req.get("id")
    #
    #     # 访客访问的限制
    #     if (
    #         secret_key != "2AB0621AC6B94E29BE37B583EAFA80C6"
    #         or uuid != "6358dca556c34349a10d146ae4bf5ad6"
    #     ):
    #         secret = get_global("secret")
    #         if real_ip not in secret:
    #             secret[real_ip] = 0
    #
    #         secret[real_ip] += 1
    #         set_global(key="secret", value=secret)
    #         if secret[real_ip] > 3:
    #             create_error_with_msg(2, "权限错误")

    logger.info(
        "Path: {}  Method: {} RemoteAddr: {} headers: {} request_message: {}  ".format(
            request.path,
            request.method,
            real_ip,
            request.headers.to_wsgi_list(),
            request_message
            # , request.__dict__
        )
    )
