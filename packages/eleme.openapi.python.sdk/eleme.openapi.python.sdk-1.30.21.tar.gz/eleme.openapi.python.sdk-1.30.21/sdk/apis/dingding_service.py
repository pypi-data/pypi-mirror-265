# -*- coding: utf-8 -*-


# 生活钉接口
class DingdingService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def query_transformer_v_1_life_ding(self, request):
        """
        生活钉首页接口
        :param request:钉钉入参
        """
        return self.__client.call("eleme.dingding.queryTransformerV1LifeDing", {"request": request})

    def collect_transformer_v_1_life_ding(self, request):
        """
        生活钉回收接口for推荐列表
        :param request:钉钉入参
        """
        return self.__client.call("eleme.dingding.collectTransformerV1LifeDing", {"request": request})

