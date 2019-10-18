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

    def __init__(self, ip, port, remark, security, uuid, alterId, network, camouflageType, camouflageHost,
                 camouflagePath, camouflageTls):
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
            'log': {
                'access': None,
                'error': None,
                'loglevel': None
            },
            'inbound': {
                'port': 1086,
                'listen': '127.0.0.1',
                'protocol': 'socks',
                'settings': {
                    'auth': 'noauth',
                    'udp': False,
                    'ip': '127.0.0.1',
                    'clients': None
                },
                'streamSettings': None
            },
            'outbound': {
                'tag': 'agentout',
                'protocol': 'vmess',
                'settings': {
                    'vnext': [
                        {
                            'address': '213.213.213.213',
                            'port': 23333,
                            'users': [
                                {
                                    'id': 'dddda000-bbbb-4444-2222-fffff6666666',
                                    'alterId': 100,
                                    'security': 'aes-128-gcm'
                                }
                            ]
                        }
                    ],
                    'servers': None
                },
                'streamSettings': {
                    'network': None,
                    'security': None,
                    'tcpSettings': None,
                    'kcpSettings': None,
                    'wsSettings': None
                },
                'mux': {
                    'enabled': False
                }
            },
            'inboundDetour': None,
            'outboundDetour': [
                {
                    'protocol': 'freedom',
                    'settings': {
                        'response': None
                    },
                    'tag': 'direct'
                },
                {
                    'protocol': 'blackhole',
                    'settings': {
                        'response': {
                            'type': 'http'
                        }
                    },
                    'tag': 'blockout'
                }
            ],
            '_dns': {
                'servers': [
                    '8.8.8.8',
                    '8.8.4.4',
                    '114.114.114.114'
                ]
            },
            '_routing': {
                'strategy': 'rules',
                'settings': {
                    'domainStrategy': 'IPIfNonMatch',
                    'rules': [
                        {
                            'type': 'field',
                            'port': None,
                            'outboundTag': 'direct',
                            'ip': [
                                '0.0.0.0/8',
                                '10.0.0.0/8',
                                '100.64.0.0/10',
                                '127.0.0.0/8',
                                '169.254.0.0/16',
                                '172.16.0.0/12',
                                '192.0.0.0/24',
                                '192.0.2.0/24',
                                '192.168.0.0/16',
                                '198.18.0.0/15',
                                '198.51.100.0/24',
                                '203.0.113.0/24',
                                '::1/128',
                                'fc00::/7',
                                'fe80::/10'
                            ],
                            'domain': None
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
                "access": "/var/log/v2ray/access.log",
                "error": "/var/log/v2ray/error.log",
                "logLevel": "none"
            },
            "inbounds": [
                {
                    "port": 1086,
                    "listen": "127.0.0.1",
                    "protocol": "socks",
                    "settings": {
                        "udp": True
                    },
                    "tag": "proxy"
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
                            "outboundTag": "out"
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
