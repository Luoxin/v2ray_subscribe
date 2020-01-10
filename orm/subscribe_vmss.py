import time
from orm import db
from peewee import *


class SubscribeVmss(Model):
    """
        抓取到的数据表
    """

    id = IntegerField(primary_key=True)

    created_at = IntegerField(default=time.time(), verbose_name="创建时间")
    updated_at = IntegerField(default=time.time(), verbose_name="更新时间")

    url = CharField(max_length=1000, null=False, unique=True, verbose_name="节点分享地址")
    network_protocol_type = CharField(max_length=50, verbose_name="网络协议类型")

    # 各个维度的速度测试
    speed_google = FloatField(verbose_name="google访问速度")
    network_delay_google = FloatField(verbose_name="google访问延时")

    speed_youtube = FloatField(verbose_name="youtube访问速度")
    network_delay_youtube = FloatField(verbose_name="youtube访问延时")

    speed_internet = FloatField(verbose_name="测速网站 测速速度")
    network_delay_internet = FloatField(verbose_name="测速网站 访问延时")

    next_time = IntegerField(verbose_name="下一次的测速时间", index=True)
    interval = IntegerField(verbose_name="间隔")
    crawl_id = IntegerField(verbose_name="关联的 SubscribeCrawl 的 id")

    class Meta:
        database = db
        db_name = "subscribe_vmss"

    def save(self, *args, **kwargs):
        """覆写save方法, update_time字段自动更新, 实例对象需要在update成功之后调用save()"""
        if self._get_pk_value() is None:
            # this is a create operation, set the date_created field
            self.created_at = time.time()

        self.updated_at = time.time()

        return super(SubscribeVmss, self).save(*args, **kwargs)
