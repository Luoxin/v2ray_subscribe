from orm import *
from orm import base


class SubscribeVmss(base):
    __tablename__ = "subscribe_vmss"

    id = Column(Integer, primary_key=True)
    created_at = Column(Integer, server_default=str(utils.now()))
    updated_at = Column(
        Integer, server_default=str(int(utils.now())), onupdate=str(int(utils.now()))
    )

    url = Column(String(500), unique=True, comment="节点分享地址")
    network_protocol_type = Column(String(100), index=True, comment="网络协议类型")

    conf_details = Column(JSON, comment="配置的详情内容")

    # 各个维度的速度测试
    speed_google = Column(Float, comment="google访问速度")
    network_delay_google = Column(Float, comment="google访问延时")

    speed_youtube = Column(Float, comment="youtube访问速度")
    network_delay_youtube = Column(Float, comment="youtube访问延时")

    speed_internet = Column(Float, comment="测速网站 测速速度")
    network_delay_internet = Column(Float, comment="测速网站 访问延时")

    next_at = Column(Integer, comment="下一次的测速时间")
    interval = Column(Integer, comment="间隔")
    crawl_id = Column(Integer, comment="关联的 SubscribeCrawl 的 id")

    is_closed = Column(Boolean, comment="是否禁用")

    death_count = Column(Integer, comment="死亡计时")

    __table_args__ = ({"comment": "抓取到的数据表"},)  # 添加索引和表注释
