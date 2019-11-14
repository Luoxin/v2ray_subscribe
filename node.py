from conf.conf import CHECK_PORT


class Node:
    # ip
    ip = ""
    # port
    port = 0
    # beiz
    remark = ""
    # jiamiafangshi
    security = ""

    def __init__(self, ip, port, remark, security):
        self.ip = ip
        self.port = port
        self.remark = remark
        self.security = security


class V2ray(Node):
    uuid = ""
    alterId = 0
    network = ""
    camouflageType = ""
    camouflageHost = ""
    camouflagePath = ""
    camouflageTls = ""

    def __init__(
        self,
        ip,
        port,
        remark,
        security,
        uuid,
        alterId,
        network,
        camouflageType,
        camouflageHost,
        camouflagePath,
        camouflageTls,
    ):
        super(V2ray, self).__init__(ip, port, remark, security)
        self.uuid = uuid
        self.alterId = alterId
        self.network = network
        self.camouflageHost = camouflageHost
        self.camouflagePath = camouflagePath
        self.camouflageTls = camouflageTls
        self.camouflageType = camouflageType

    def format_config(self):
        v2ray_conf = {
            "policy": {
                "system": {"statsInboundUplink": True, "statsInboundDownlink": True}
            },
            "log": {"access": "", "error": "", "loglevel": "warning"},
            "inbounds": [
                {
                    "tag": "proxy",
                    "port": CHECK_PORT,
                    "listen": "127.0.0.1",
                    "protocol": "socks",
                    "sniffing": {"enabled": True, "destOverride": ["http", "tls"]},
                    "settings": {
                        "auth": "noauth",
                        "udp": True,
                        "ip": None,
                        "address": None,
                        "clients": None,
                    },
                    "streamSettings": None,
                },
                # {
                #     "tag": "api",
                #     "port": 1090,
                #     "listen": "127.0.0.1",
                #     "protocol": "dokodemo-door",
                #     "sniffing": None,
                #     "settings": {
                #         "auth": None,
                #         "udp": False,
                #         "ip": None,
                #         "address": "127.0.0.1",
                #         "clients": None
                #     },
                #     "streamSettings": None
                # }
            ],
            "outbounds": [],
            "stats": {},
            "api": {"tag": "api", "services": ["StatsService"]},
            # "dns": None,
            "routing": {
                "domainStrategy": "IPIfNonMatch",
                "rules": [
                    {
                        "type": "field",
                        "port": None,
                        "inboundTag": "api",
                        "outboundTag": "api",
                        "ip": None,
                        "domain": None,
                    },
                    {
                        "type": "field",
                        "port": None,
                        "inboundTag": None,
                        "outboundTag": "proxy",
                        "ip": None,
                        "domain": [
                            "geosite:google",
                            "geosite:github",
                            "geosite:netflix",
                            "geosite:steam",
                            "geosite:telegram",
                            "geosite:tumblr",
                            "geosite:speedtest",
                            "geosite:bbc",
                            "domain:gvt1.com",
                            "domain:textnow.com",
                            "domain:twitch.tv",
                            "domain:wikileaks.org",
                            "domain:naver.com",
                        ],
                    },
                    {
                        "type": "field",
                        "port": None,
                        "inboundTag": None,
                        "outboundTag": "proxy",
                        "ip": [
                            "91.108.4.0/22",
                            "91.108.8.0/22",
                            "91.108.12.0/22",
                            "91.108.20.0/22",
                            "91.108.36.0/23",
                            "91.108.38.0/23",
                            "91.108.56.0/22",
                            "149.154.160.0/20",
                            "149.154.164.0/22",
                            "149.154.172.0/22",
                            "74.125.0.0/16",
                            "173.194.0.0/16",
                            "172.217.0.0/16",
                            "216.58.200.0/24",
                            "216.58.220.0/24",
                        ],
                        "domain": None,
                    },
                    {
                        "type": "field",
                        "port": None,
                        "inboundTag": None,
                        "outboundTag": "direct",
                        "ip": None,
                        "domain": [
                            "domain:12306.com",
                            "domain:51ym.me",
                            "domain:52pojie.cn",
                            "domain:8686c.com",
                            "domain:abercrombie.com",
                            "domain:adobesc.com",
                            "domain:air-matters.com",
                            "domain:air-matters.io",
                            "domain:airtable.com",
                            "domain:akadns.net",
                            "domain:apache.org",
                            "domain:api.crisp.chat",
                            "domain:api.termius.com",
                            "domain:appshike.com",
                            "domain:appstore.com",
                            "domain:aweme.snssdk.com",
                            "domain:bababian.com",
                            "domain:battle.net",
                            "domain:beatsbydre.com",
                            "domain:bet365.com",
                            "domain:bilibili.cn",
                            "domain:ccgslb.com",
                            "domain:ccgslb.net",
                            "domain:chunbo.com",
                            "domain:chunboimg.com",
                            "domain:clashroyaleapp.com",
                            "domain:cloudsigma.com",
                            "domain:cloudxns.net",
                            "domain:cmfu.com",
                            "domain:culturedcode.com",
                            "domain:dct-cloud.com",
                            "domain:didialift.com",
                            "domain:douyutv.com",
                            "domain:duokan.com",
                            "domain:dytt8.net",
                            "domain:easou.com",
                            "domain:ecitic.net",
                            "domain:eclipse.org",
                            "domain:eudic.net",
                            "domain:ewqcxz.com",
                            "domain:fir.im",
                            "domain:frdic.com",
                            "domain:fresh-ideas.cc",
                            "domain:godic.net",
                            "domain:goodread.com",
                            "domain:haibian.com",
                            "domain:hdslb.net",
                            "domain:hollisterco.com",
                            "domain:hongxiu.com",
                            "domain:hxcdn.net",
                            "domain:images.unsplash.com",
                            "domain:img4me.com",
                            "domain:ipify.org",
                            "domain:ixdzs.com",
                            "domain:jd.hk",
                            "domain:jianshuapi.com",
                            "domain:jomodns.com",
                            "domain:jsboxbbs.com",
                            "domain:knewone.com",
                            "domain:kuaidi100.com",
                            "domain:lemicp.com",
                            "domain:letvcloud.com",
                            "domain:lizhi.io",
                            "domain:localizecdn.com",
                            "domain:lucifr.com",
                            "domain:luoo.net",
                            "domain:mai.tn",
                            "domain:maven.org",
                            "domain:miwifi.com",
                            "domain:moji.com",
                            "domain:moke.com",
                            "domain:mtalk.google.com",
                            "domain:mxhichina.com",
                            "domain:myqcloud.com",
                            "domain:myunlu.com",
                            "domain:netease.com",
                            "domain:nfoservers.com",
                            "domain:nssurge.com",
                            "domain:nuomi.com",
                            "domain:ourdvs.com",
                            "domain:overcast.fm",
                            "domain:paypal.com",
                            "domain:paypalobjects.com",
                            "domain:pgyer.com",
                            "domain:qdaily.com",
                            "domain:qdmm.com",
                            "domain:qin.io",
                            "domain:qingmang.me",
                            "domain:qingmang.mobi",
                            "domain:qqurl.com",
                            "domain:rarbg.to",
                            "domain:rrmj.tv",
                            "domain:ruguoapp.com",
                            "domain:sm.ms",
                            "domain:snwx.com",
                            "domain:soku.com",
                            "domain:startssl.com",
                            "domain:store.steampowered.com",
                            "domain:symcd.com",
                            "domain:teamviewer.com",
                            "domain:tmzvps.com",
                            "domain:trello.com",
                            "domain:trellocdn.com",
                            "domain:ttmeiju.com",
                            "domain:udache.com",
                            "domain:uxengine.net",
                            "domain:weather.bjango.com",
                            "domain:weather.com",
                            "domain:webqxs.com",
                            "domain:weico.cc",
                            "domain:wenku8.net",
                            "domain:werewolf.53site.com",
                            "domain:windowsupdate.com",
                            "domain:wkcdn.com",
                            "domain:workflowy.com",
                            "domain:xdrig.com",
                            "domain:xiaojukeji.com",
                            "domain:xiaomi.net",
                            "domain:xiaomicp.com",
                            "domain:ximalaya.com",
                            "domain:xitek.com",
                            "domain:xmcdn.com",
                            "domain:xslb.net",
                            "domain:xteko.com",
                            "domain:yach.me",
                            "domain:yixia.com",
                            "domain:yunjiasu-cdn.net",
                            "domain:zealer.com",
                            "domain:zgslb.net",
                            "domain:zimuzu.tv",
                            "domain:zmz002.com",
                            "domain:pinquest.com",
                            "domain:samsungdm.com",
                        ],
                    },
                    {
                        "type": "field",
                        "port": None,
                        "inboundTag": None,
                        "outboundTag": "block",
                        "ip": None,
                        "domain": ["geosite:category-ads"],
                    },
                    {
                        "type": "field",
                        "port": None,
                        "inboundTag": None,
                        "outboundTag": "direct",
                        "ip": ["geoip:private"],
                        "domain": None,
                    },
                    {
                        "type": "field",
                        "port": None,
                        "inboundTag": None,
                        "outboundTag": "direct",
                        "ip": ["geoip:cn"],
                        "domain": None,
                    },
                    {
                        "type": "field",
                        "port": None,
                        "inboundTag": None,
                        "outboundTag": "direct",
                        "ip": None,
                        "domain": ["geosite:cn"],
                    },
                ],
            },
        }

        if self.network == "tcp" or self.network == "auto":
            # tcp下
            v2ray_conf["outbounds"].append(
                {
                    "protocol": "vmess",
                    "settings": {
                        "vnext": [
                            {
                                "address": self.ip,
                                "port": int(self.port),
                                "users": [{"id": self.uuid, "alterId": self.alterId}],
                            }
                        ]
                    },
                    "streamSettings": {"network": "tcp"},
                    "tag": "out",
                }
            )
            return v2ray_conf
        elif self.network == "kcp":
            # kcp 下
            v2ray_conf["outbounds"].append(
                {
                    "protocol": "vmess",
                    "settings": {
                        "vnext": [
                            {
                                "address": self.ip,
                                "port": int(self.port),
                                "users": [{"id": self.uuid, "alterId": self.alterId}],
                            }
                        ]
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
                            "header": {"type": self.camouflageType,},
                        },
                    },
                    "tag": "out",
                }
            )
            return v2ray_conf
        elif self.network == "ws":
            # ws
            v2ray_conf["outbounds"].append(
                {
                    "protocol": "vmess",
                    "settings": {
                        "vnext": [
                            {
                                "address": self.ip,
                                "port": int(self.port),
                                "users": [{"id": self.uuid, "alterId": self.alterId}],
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": "ws",
                        "security": self.camouflageTls,
                        "tlsSettings": {"allowInsecure": True,},
                        "wsSettings": {
                            "path": self.camouflagePath,
                            "headers": {"Host": self.camouflageHost},
                        },
                    },
                    "tag": "out",
                }
            )
            return v2ray_conf
        else:
            # h2
            v2ray_conf["outbounds"].append(
                {
                    "protocol": "vmess",
                    "settings": {
                        "vnext": [
                            {
                                "address": self.ip,
                                "port": int(self.port),
                                "users": [{"id": self.uuid, "alterId": self.alterId}],
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": "ws",
                        "security": self.camouflageTls,
                        "tlsSettings": {"allowInsecure": True,},
                        "httpSettings": {
                            "path": self.camouflagePath,
                            "host": [self.camouflageHost],
                        },
                    },
                    "tag": "out",
                }
            )
            return v2ray_conf


class Shadowsocks(Node):
    password = ""

    def __init__(self, ip, port, remark, security, password):
        super(Shadowsocks, self).__init__(ip, port, remark, security)
        self.password = password

    def format_config(self):
        ss_config = {
            "log": {
                "access": "/var/log/v2ray/access.log",
                "error": "/var/log/v2ray/error.log",
                "logLevel": "none",
            },
            "inbounds": [
                {
                    "port": CHECK_PORT,
                    "listen": "127.0.0.1",
                    "protocol": "socks",
                    "settings": {"udp": True},
                    "tag": "proxy",
                }
            ],
            "outbounds": [
                {"settings": {}, "protocol": "freedom", "tag": "direct"},
                {"settings": {}, "protocol": "blackhole", "tag": "blocked"},
            ],
            "routing": {
                "strategy": "rules",
                "settings": {
                    "domainStrategy": "AsIs",
                    "rules": [
                        {
                            "type": "field",
                            "ip": ["geoip:cn", "geoip:private"],
                            "outboundTag": "direct",
                        },
                        {"type": "field", "inboundTag": ["in"], "outboundTag": "out"},
                    ],
                },
            },
        }
        ss_config["outbounds"].append(
            {
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
                            "level": 1,
                        }
                    ]
                },
                "streamSettings": {"network": "tcp"},
                "mux": {"enabled": False},
            }
        )
        return ss_config
