# -*- coding: utf-8 -*-


# 斗金服务
class AdService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def find_dou_jin_cpc_solution(self, request):
        """
        查询斗金推广设置
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.findDouJinCpcSolution", {"request": request})

    def find_dou_jin_click_distribution_report(self, request):
        """
        查询斗金推广点击分布信息
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.findDouJinClickDistributionReport", {"request": request})

    def find_dou_jin_effect_report(self, request):
        """
        查询斗金推广效果数据
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.findDouJinEffectReport", {"request": request})

    def update_dou_jin_time(self, request):
        """
        设置斗金时段
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.updateDouJinTime", {"request": request})

    def update_dou_jin_target(self, request):
        """
        设置斗金定向
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.updateDouJinTarget", {"request": request})

    def update_dou_jin_budget(self, request):
        """
        设置斗金预算
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.updateDouJinBudget", {"request": request})

    def update_dou_jin_bid(self, request):
        """
        设置斗金出价
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.updateDouJinBid", {"request": request})

    def update_dou_jin_state(self, request):
        """
        设置斗金状态
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.updateDouJinState", {"request": request})

    def create_dou_jin_solution(self, request):
        """
        创建斗金计划
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.createDouJinSolution", {"request": request})

    def find_dou_jin_account_balance(self, request):
        """
        查询斗金最大可用余额
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.findDouJinAccountBalance", {"request": request})

    def find_display_cpc_solution(self, request):
        """
        查询优享大牌推广设置
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.findDisplayCpcSolution", {"request": request})

    def find_display_effect_report(self, request):
        """
        查询优享大牌推广效果数据
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.findDisplayEffectReport", {"request": request})

    def update_display_time(self, request):
        """
        设置优享大牌时段
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.updateDisplayTime", {"request": request})

    def update_display_target(self, request):
        """
        设置优享大牌定向
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.updateDisplayTarget", {"request": request})

    def update_display_budget(self, request):
        """
        设置优享大牌预算
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.updateDisplayBudget", {"request": request})

    def update_display_bid(self, request):
        """
        设置优享大牌出价
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.updateDisplayBid", {"request": request})

    def update_display_state(self, request):
        """
        设置优享大牌状态
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.updateDisplayState", {"request": request})

    def create_display_solution(self, request):
        """
        创建优享大牌计划
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.createDisplaySolution", {"request": request})

    def find_display_account_balance(self, request):
        """
        查询优享大牌最大可用余额
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.findDisplayAccountBalance", {"request": request})

