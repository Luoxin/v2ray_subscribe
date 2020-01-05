from flask import Blueprint, request
from utils import logger  # 日志
from error_exception import create_error_with_msg

test_interface_api = Blueprint("test_interface", __name__)


@test_interface_api.route(
    "/testInterface", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "COPY"]
)
def test_post():
    logger.info(
        "a new {} request from {} ({})".format(
            request.method.lower(), request.remote_user, request.remote_addr
        )
    )
    logger.info("The incoming test information is {}".format(request.get_data()))
    if request.method == "GET":
        return {"info": "GET request successful"}
    elif request.method == "POST":
        return {"info": "POST request successful"}
    elif request.method == "PUT":
        return {"info": "PUT request successful"}
    elif request.method == "PATCH":
        create_error_with_msg(1, "测试接口的PATCH请求的错误测试")
        return {"info": "PATCH request successful"}
    elif request.method == "DELETE":
        return "DELETE request successful"
    elif request.method == "COPY":
        return {"info": "COPY request successful"}
