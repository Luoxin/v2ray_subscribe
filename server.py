import traceback

from flask import Flask, ctx, jsonify
from flask_sqlalchemy import SQLAlchemy

from conf.conf import HOST, PORT
from conntext import JSONResponse, before_request
from error_exception import InternalException
from init_service import init_service
from route_list import ROUTE_LIST
from utils import logger

app = Flask(__name__)

app.response_class = JSONResponse
app.before_request(before_request)
app.logger = logger

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
db = SQLAlchemy(app)


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
    app.run(HOST, port=PORT, threaded=True)
