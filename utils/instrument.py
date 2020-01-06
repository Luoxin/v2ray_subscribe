import json
import uuid as uu


class Instrument:
    @staticmethod
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

    @staticmethod
    def encode_to_utf8(data: str != "") -> str:
        # chardet.detect(data.encode()).get("encoding")
        return data.encode().decode("utf-8")

    @staticmethod
    def uuid() -> str:
        """
            获取uuid
        :return: uuid
        """
        return uu.uuid4().hex
