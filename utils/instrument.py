import base64
import hashlib
import json
import uuid as uu


def is_json(data: (bytes, str)) -> bool:
    if isinstance(data, bytes):
        data = data.decode()
    if isinstance(data, str):
        try:
            json.loads(data)
            return True
        except:
            return False
    return False


def encode_to_utf8(data: str != "") -> str:
    # chardet.detect(data.encode()).get("encoding")
    return data.encode().decode("utf-8")


def gen_uuid() -> str:
    """
        获取uuid
    :return: uuid
    """
    return uu.uuid4().hex


def md5(s) -> str:
    hl = hashlib.md5()
    hl.update(s.encode(encoding='utf-8'))
    return hl.hexdigest()


def base64_encode(s) -> str:
    return base64.b64encode(s.encode()).decode("utf-8")
