from flask import request, jsonify, ctx

from error_exception import InternalException
from utils import logger, json  # 日志


class ServiceResponse(object):
    def __init__(self, response=None):
        if response is None or isinstance(response, dict):
            self.response = json.dumps({"data": response, "errcode": 0, "errmsg": ""})
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


def error_handler(e):
    response_data = {"data": {}, "errcode": 0, "errmsg": ""}
    if isinstance(e, InternalException):
        response_data["errcode"] = e.args[0]
        response_data["errmsg"] = e.args[1]
    elif isinstance(e, ctx.HTTPException):
        response_data["errcode"] = e.code
        response_data["errmsg"] = e.description
    else:
        response_data["errcode"] = -1
        response_data["errmsg"] = "system error"
        logger.error("err message {}".format(e))

    logger.error(response_data)
    return jsonify(response_data)
