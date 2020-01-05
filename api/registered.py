import requests
from flask import Blueprint, request, redirect

from error_exception import create_error_with_msg
from utils import logger  # 日志

registered = Blueprint("registered", __name__)


@registered.route("/registered/<path:sub_path>", methods=["GET", "POST"])
def registered_api(sub_path):

    return ""
