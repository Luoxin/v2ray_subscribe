from conf import global_variable
import traceback
from flask import Flask, ctx, jsonify, Response

from conntext import before_request
from error_exception import InternalException
from init_service import init_service

from route_list import ROUTE_LIST
from utils import logger

class ServiceCentre(Flask):
    def make_response(self, rv):
        logger.info(rv)
        if isinstance(rv, ServiceResponse):
            return Response(rv.get_data(), mimetype='application/json', status=200)
        return super().make_response(rv)


app = ServiceCentre(global_variable.get_conf_str("SERVER_NAME", "v2ray_subscribe"))

app.before_request(before_request)
app.logger = logger


def init_route_list():
    for ROUTE in ROUTE_LIST:
        logger.info("a new route will add {}".format(ROUTE.name))
        app.register_blueprint(ROUTE)


init_route_list()
init_service()


@app.errorhandler(Exception)
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


@app.after_request
def after_request(f):
    try:
        pass
        # print(f.__dict__)
        # print(f.response)
        # print(f.response[0].decode("utf-8"))
        # print(app.url_map.__dict__)
        # print(app.url_map._rules_by_endpoint)
    except:
        traceback.print_exc()
    finally:
        return f


@app.route("/favicon.ico")
def favicon():
    return ""


if __name__ == "__main__":
    app.run(
        global_variable.get_conf_str("HOST", default="127.0.0.1"),
        port=global_variable.get_conf_int("PORT", default=5000),
        threaded=True,
    )
