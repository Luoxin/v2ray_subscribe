import base64
import json

from orm import session, subscribe_vmss

data_list = session.query(subscribe_vmss).all()
for i, data in enumerate(data_list):
    try:
        v2ray_url = data.url
        if v2ray_url.startswith("vmess://"):  # vmess
            try:
                v = json.loads(
                    base64.b64decode(
                        v2ray_url.replace("vmess://", "").encode()
                    ).decode()
                )
                url_type = "" if v.get("net") is None else v.get("net")
                print(url_type)
                session.query(subscribe_vmss).filter(
                    subscribe_vmss.id == data.id
                ).update(
                    {subscribe_vmss.type: url_type,}
                )
            except:
                pass
    except:
        pass

session.commit()
