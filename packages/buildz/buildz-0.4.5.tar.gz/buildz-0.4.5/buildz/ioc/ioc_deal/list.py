#coding=utf-8
from ..ioc.base import Base, EncapeData
from .base import FormatData,BaseDeal
from buildz import xf, pyz
import os
dp = os.path.dirname(__file__)
join = os.path.join
class ListDeal(BaseDeal):
    def init(self, fp_lists=None, fp_defaults=None):
        super().init("ListDeal", fp_lists, fp_defaults, join(dp, "conf", "list_lists.js"), None)
    def deal(self, edata:EncapeData):
        data = edata.data
        data = self.fill(data)
        lists = xf.g(data, data=[])
        conf = edata.conf
        rst = [self.get_obj(k, conf) for k in lists]
        return rst

pass
