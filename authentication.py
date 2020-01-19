import traceback

from flask import request

from orm import db
from orm.orm import SubscribeAuthentication
from utils import logger


def get_authentication(secret_key: (str, None), uuid: (str, None)):
    try:
        if secret_key is None:
            secret_key = request.args.get("SecretKey")

        if uuid is None:
            uuid = request.args.get("id")

        if secret_key is None or uuid is None:
            return False, "非法请求"

        # uuid大写，避免不必要的错误
        uuid = uuid.upper()

        authentication = (
            db.query(SubscribeAuthentication)
            .filter(SubscribeAuthentication.secret_key == secret_key)
            .filter(SubscribeAuthentication.uuid == uuid)
            .first()
        )

        if authentication is None:
            return False, "权限不够"

        return True, authentication
    except:
        logger.error(traceback.format_exc())
        return False, ""
