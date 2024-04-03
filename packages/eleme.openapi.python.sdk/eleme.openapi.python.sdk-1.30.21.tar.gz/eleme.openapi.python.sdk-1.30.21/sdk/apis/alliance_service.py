# -*- coding: utf-8 -*-


# 渠道管理服务
class AllianceService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def create_channel_level_3(self, channel_level_3_create_request):
        """
        创建三级渠道
        :param channelLevel3CreateRequest:三级渠道信息
        """
        return self.__client.call("eleme.alliance.createChannelLevel3", {"channelLevel3CreateRequest": channel_level_3_create_request})

    def update_channel_level_3(self, channel_level_3_batch_update_request):
        """
        编辑三级渠道配置数据
        :param channelLevel3BatchUpdateRequest:渠道配置批量编辑
        """
        return self.__client.call("eleme.alliance.updateChannelLevel3", {"channelLevel3BatchUpdateRequest": channel_level_3_batch_update_request})

    def query_channel_level_3_list(self, channel_level_3_query_request):
        """
        查询三级渠道配置数据
        :param channelLevel3QueryRequest:渠道信息批量查询
        """
        return self.__client.call("eleme.alliance.queryChannelLevel3List", {"channelLevel3QueryRequest": channel_level_3_query_request})

    def query_order_info(self, channel_order_query_request):
        """
        查询订单信息
        :param channelOrderQueryRequest:订单信息查询
        """
        return self.__client.call("eleme.alliance.queryOrderInfo", {"channelOrderQueryRequest": channel_order_query_request})

