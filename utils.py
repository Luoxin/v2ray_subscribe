import base64
import json
import socket
import urllib
import traceback


def check_ip_port(host: str = "", port: int = 0) -> bool:
    """
    监测翻墙服务是是否可以连接来监测节点是否可用(不是100%可信)
    :param host:
    :param port:
    :return:
    """
    false_host_list = ["127.0.0.1", "0.0.0.0", ""]
    if (host in false_host_list) or port is 0:
        return False
    ip = socket.getaddrinfo(host, None)[0][4][0]
    if ":" in ip:
        inet = socket.AF_INET6
    else:
        inet = socket.AF_INET

    sock = socket.socket(inet)
    status = sock.connect_ex((ip, int(port)))
    sock.close()
    if status != 0:
        return False
    return True


def check_ip_port_by_url(url: str = "") -> bool:
    try:
        if len(url) == 0:
            return False

        if url.startswith("ss://"):  # ss node
            base64_str = url.replace("ss://", "")
            base64_str = urllib.parse.unquote(base64_str)
            origin = decode(base64_str[0 : base64_str.index("#")])
            ipandport = origin[origin.index("@") + 1 :]
            host = ipandport[0 : ipandport.index(":")]
            port = int(ipandport[ipandport.index(":") + 1 :])

        elif url.startswith("vmess://"):  # vmess
            base64_str = url.replace("vmess://", "")
            info = json.loads(
                base64.b64decode(base64_str.encode())
                .decode()
                .replace("\r", "")
                .replace("\n", "")
                .replace(" ", "")
            )
            host = "" if info.get("add") is not None else info.get("add")
            port = 0 if info.get("port") is not None else int(info.get("port"))
        else:
            return False

        return check_ip_port(host, port)
    except:
        traceback.print_exc()
        return False