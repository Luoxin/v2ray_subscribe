from flask import Flask, Response

from conf import global_variable
from conntext import before_request, ServiceResponse, error_handler
from init_service import start_task
from route_list import ROUTE_LIST
from utils import logger


class ServiceCentre(Flask):
    def __init__(self):
        super().__init__(
            import_name=global_variable.get_conf_str("SERVER_NAME", "v2ray_subscribe")
        )

        self._init_service()

    def make_response(self, rv):
        if isinstance(rv, ServiceResponse):
            return Response(rv.get_data(), mimetype="application/json", status=200)
        return super().make_response(rv)

    def _init_route_list(self):
        for ROUTE in ROUTE_LIST:
            logger.info("a new route will add {}".format(ROUTE.name))
            self.register_blueprint(ROUTE)

    def _init_service(self):
        self._init_route_list()
        self.logger = logger
        start_task()

        self.before_request_funcs.setdefault(None, []).append(before_request)

        self._register_error_handler(None, Exception, error_handler)


app = ServiceCentre()


@app.route("/favicon.ico")
def favicon():
    return ""


if __name__ == "__main__":
    app.run(
        global_variable.get_conf_str("HOST", default="0.0.0.0"),
        port=global_variable.get_conf_int("PORT", default=5000),
        threaded=True,
    )
