class Node:

    # ip
    ip = ''
    # port
    port = 0
    # beiz
    remark = ''
    # jiamiafangshi
    security = ''

    def __init__(self, ip, port, remark, security):
        self.ip = ip
        self.port = port
        self.remark = remark
        self.security = security


class V2ray(Node):
    uuid = ''
    alterId = 0
    network = ''
    camouflageType = ''
    camouflageHost = ''
    camouflagePath = ''
    camouflageTls = ''

    def __init__(self, ip, port, remark, security, uuid, alterId, network, camouflageType, camouflageHost, camouflagePath, camouflageTls):
        super(V2ray, self).__init__(ip, port, remark, security)
        self.uuid = uuid
        self.alterId = alterId
        self.network = network
        self.camouflageHost = camouflageHost
        self.camouflagePath = camouflagePath
        self.camouflageTls = camouflageTls
        self.camouflageType = camouflageType

    def formatConfig(self):
        v2rayConf = {
            "log": {
                "access": "/var/log/v2ray/access.log",
                "error": "/var/log/v2ray/error.log",
                "logLevel": "none"
            },
            "inbounds": [
                {
                    "port": 1086,
                    "listen": "0.0.0.0",
                    "protocol": "socks",
                    "settings": {
                        "udp": True
                    },
                    "tag": "in"
                }
            ],
            "outbounds": [
                {
                    "settings": {},
                    "protocol": "freedom",
                    "tag": "direct"
                },
                {
                    "settings": {},
                    "protocol": "blackhole",
                    "tag": "blocked"
                }
            ],
            "routing": {
                "strategy": "rules",
                "settings": {
                    "domainStrategy": "AsIs",
                    "rules": [
                        {
                            "type": "field",
                            "ip": [
                                "geoip:cn",
                                "geoip:private"
                            ],
                            "outboundTag": "direct"
                        },
                        {
                            "type": "field",
                            "inboundTag": ["in"],
                            "outboundTag":"out"
                        }
                    ]
                }
            }
        }
        if self.network == 'tcp' or self.network == 'auto':
            # tcp下
            v2rayConf['outbounds'].append({
                "protocol": "vmess",
                "settings": {
                    "vnext": [{
                        "address": self.ip,
                        "port": int(self.port),
                        "users": [
                            {
                                "id": self.uuid,
                                "alterId": self.alterId
                            }
                        ]
                    }]
                },
                "streamSettings": {
                    "network": "tcp"
                },
                "tag": "out"
            })
            return v2rayConf
        elif self.network == 'kcp':
            # kcp 下
            v2rayConf['outbounds'].append({
                "protocol": "vmess",
                "settings": {
                    "vnext": [{
                        "address": self.ip,
                        "port": int(self.port),
                        "users": [
                            {
                                "id": self.uuid,
                                "alterId": self.alterId
                            }
                        ]
                    }]
                },
                "streamSettings": {
                    "network": "kcp",
                    "kcpSettings": {
                        "mtu": 1350,
                        "tti": 50,
                        "uplinkCapacity": 12,
                        "downlinkCapacity": 100,
                        "congestion": False,
                        "readBufferSize": 2,
                        "writeBufferSize": 2,
                        "header": {
                            "type": self.camouflageType,
                        }
                    }
                },
                "tag": "out"
            })
            return v2rayConf
        elif self.network == 'ws':
            # ws
            v2rayConf['outbounds'].append({
                "protocol": "vmess",
                "settings": {
                    "vnext": [{
                        "address": self.ip,
                        "port": int(self.port),
                        "users": [
                            {
                                "id": self.uuid,
                                "alterId": self.alterId
                            }
                        ]
                    }]
                },
                "streamSettings": {
                    "network": "ws",
                    "security": self.camouflageTls,
                    "tlsSettings": {
                        "allowInsecure": True,
                    },
                    "wsSettings": {
                        "path": self.camouflagePath,
                        "headers": {
                            "Host": self.camouflageHost
                        }
                    }
                },
                "tag": "out"
            })
            return v2rayConf
        else:
            # h2
            v2rayConf['outbounds'].append({
                "protocol": "vmess",
                "settings": {
                    "vnext": [{
                        "address": self.ip,
                        "port": int(self.port),
                        "users": [
                            {
                                "id": self.uuid,
                                "alterId": self.alterId
                            }
                        ]
                    }]
                },
                "streamSettings": {
                    "network": "ws",
                    "security": self.camouflageTls,
                    "tlsSettings": {
                        "allowInsecure": True,
                    },
                    "httpSettings": {
                        "path": self.camouflagePath,
                        "host": [
                            self.camouflageHost
                        ]
                    }
                },
                "tag": "out"
            })
            return v2rayConf


class Shadowsocks(Node):
    password = ''

    def __init__(self, ip, port, remark, security, password):
        super(Shadowsocks, self).__init__(ip, port, remark, security)
        self.password = password

    def formatConfig(self):
        ssConfig = {
            "log": {
                "access" : "/var/log/v2ray/access.log",
                "error":"/var/log/v2ray/error.log",
                "logLevel": "none"
            },
            "inbounds": [
                {
                    "port": 1086,
                    "listen": "0.0.0.0",
                    "protocol": "socks",
                    "settings": {
                        "udp": True
                    },
                    "tag": "in"
                }
            ],
            "outbounds": [
                {
                    "settings": {},
                    "protocol": "freedom",
                    "tag": "direct"
                },
                {
                    "settings": {},
                    "protocol": "blackhole",
                    "tag": "blocked"
                }
            ],
            "routing": {
                "strategy": "rules",
                "settings": {
                    "domainStrategy": "AsIs",
                    "rules": [
                        {
                            "type": "field",
                            "ip": [
                                "geoip:cn",
                                "geoip:private"
                            ],
                            "outboundTag": "direct"
                        },
                        {
                            "type": "field",
                            "inboundTag": ["in"],
                            "outboundTag":"out"
                        }
                    ]
                }
            }
        }
        ssConfig['outbounds'].append({
            "tag": "out",
            "protocol": "shadowsocks",
            "settings": {
                "servers": [
                    {
                        "address": self.ip,
                        "method": self.security,
                        "ota": False,
                        "password": self.password,
                        "port": int(self.port),
                        "level": 1
                    }
                ]
            },
            "streamSettings": {
                "network": "tcp"
            },
            "mux": {
                "enabled": False
            }
        })
        return ssConfig
