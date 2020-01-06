import traceback

from flask import request, jsonify, after_this_request
from werkzeug._compat import integer_types, text_type
from werkzeug.datastructures import Headers
from werkzeug.utils import get_content_type
from werkzeug.wrappers import Response

from utils import logger  # 日志


class JSONResponse(Response):
    default_mimetype = "application/json"

    def __init__(
        self,
        response=None,
        status=None,
        headers=None,
        mimetype=None,
        content_type=None,
        direct_passthrough=False,
    ):
        super().__init__(
            response, status, headers, mimetype, content_type, direct_passthrough
        )
        if isinstance(headers, Headers):
            self.headers = headers
        elif not headers:
            self.headers = Headers()
        else:
            self.headers = Headers(headers)

        if content_type is None:
            if mimetype is None and "content-type" not in self.headers:
                mimetype = self.default_mimetype
            if mimetype is not None:
                mimetype = get_content_type(mimetype, self.charset)
            content_type = mimetype
        if content_type is not None:
            self.headers["Content-Type"] = content_type
        if status is None:
            status = self.default_status
        if isinstance(status, integer_types):
            self.status_code = status
        else:
            self.status = status

        self.direct_passthrough = direct_passthrough
        self._on_close = []

        # we set the response after the headers so that if a class changes
        # the charset attribute, the data is set in the correct charset.
        if response is None:
            self.response = {}
        elif isinstance(response, (text_type, bytes, bytearray)):
            self.set_data(response)
        else:
            self.response = response

    @classmethod
    def force_type(cls, response, environ=None):
        response_data = {"data": response, "errcode": 0, "errmsg": ""}
        if isinstance(response, dict):
            if (
                isinstance(response.get("errcode"), int)
                and response.get("errcode") != 0
            ):
                response_data = response

        return super(JSONResponse, cls).force_type(jsonify(response_data), environ)


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


def after_request_func(rsp):
    try:
        pass
        # print(rsp.response[0].decode("utf-8"))
        # print(f.headers)
    except:
        traceback.print_exc()
    finally:
        return rsp
