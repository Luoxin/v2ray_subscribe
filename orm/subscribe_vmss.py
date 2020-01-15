from orm import *


class SubscribeVmss(BaseModel):
    """
        抓取到的数据表
    """

    id = IntegerField(primary_key=True)

    created_at = IntegerField(default=now(), verbose_name="创建时间")
    updated_at = IntegerField(default=now(), verbose_name="更新时间")

    url = CharField(max_length=1000, null=False, verbose_name="节点分享地址")
    network_protocol_type = CharField(max_length=50, verbose_name="网络协议类型")

    # 各个维度的速度测试
    speed_google = FloatField(verbose_name="google访问速度")
    network_delay_google = FloatField(verbose_name="google访问延时")

    speed_youtube = FloatField(verbose_name="youtube访问速度")
    network_delay_youtube = FloatField(verbose_name="youtube访问延时")

    speed_internet = FloatField(verbose_name="测速网站 测速速度")
    network_delay_internet = FloatField(verbose_name="测速网站 访问延时")

    next_at = IntegerField(verbose_name="下一次的测速时间")
    interval = IntegerField(verbose_name="间隔")
    crawl_id = IntegerField(verbose_name="关联的 SubscribeCrawl 的 id")

    is_closed = BooleanField(verbose_name="是否禁用")

    class Meta:
        db_table = "subscribe_vmss"
