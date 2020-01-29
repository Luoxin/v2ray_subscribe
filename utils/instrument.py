import base64
import hashlib
import json
import re
import time
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
    hl.update(s.encode(encoding="utf-8"))
    return hl.hexdigest()


def base64_encode(s: (str, int, float, dict)) -> str:
    if isinstance(s, str):
        pass
    elif isinstance(s, (int, float)):
        s = str(s)
    elif isinstance(s, dict):
        s = json.dumps(s)
    elif isinstance(s, bytes):
        s = s.decode("utf-8")

    return base64.b64encode(s.encode()).decode("utf-8")


def base64_decode(base64_str: str):
    base64_str = base64_str.replace("\n", "").replace("-", "+").replace("_", "/")
    padding = int(len(base64_str) % 4)
    if padding != 0:
        base64_str += "=" * (4 - padding)
    return str(base64.b64decode(base64_str), "utf-8")


def now():
    return int(time.time())


def is_url(url: str) -> bool:
    return True if re.match(r"^[a-z+]+?:/{2,3}\w.+$", url) else False
