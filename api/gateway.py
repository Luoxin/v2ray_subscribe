import requests
from flask import Blueprint, request, redirect

from error_exception import create_error_with_msg
from utils import logger  # 日志

PKT_BUFF_SIZE = 2048

gateway = Blueprint("gateway", __name__)


@gateway.route("/gateway/<path:sub_path>", methods=["GET", "POST"])
def gateway_api(sub_path):
    return forward_request_gateway(sub_path)


def forward_request_gateway(sub_path: str):
    path_list = sub_path.split("/")

    # methods = request.method
    #
    # if methods == "GET":
    #     r = requests.get("http://127.0.0.1:5000")
    # elif methods == "POST":
    #     r = requests.post("http://127.0.0.1:5000")
    # else:
    create_error_with_msg(
        404,
        "The requested URL was not found on the server. If you entered the URL manually please "
        "check your spelling and try again.",
    )
    # return r.content
