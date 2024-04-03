# -*- coding: utf-8 -*-


# 商户服务
class UserService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def get_user(self):
        """
        获取商户账号信息
        """
        return self.__client.call("eleme.user.getUser", {})

    def get_phone_number(self):
        """
        获取当前授权账号的手机号,特权接口仅部分帐号可以调用
        """
        return self.__client.call("eleme.user.getPhoneNumber", {})

    def get_token_status(self, token):
        """
        获取授权token状态
        :param token:授权token
        """
        return self.__client.call("eleme.user.getTokenStatus", {"token": token})

    def auth_del_operate(self, auth_operate_req):
        """
        批量解除令牌授权
        :param authOperateReq:查询条件
        """
        return self.__client.call("eleme.user.authDelOperate", {"authOperateReq": auth_operate_req})

    def auth_recover_operate(self, auth_operate_req):
        """
        批量恢复令牌授权
        :param authOperateReq:查询条件
        """
        return self.__client.call("eleme.user.authRecoverOperate", {"authOperateReq": auth_operate_req})

    def get_open_user_id_by_user_id(self, user_id):
        """
        获取新用户ID(openUserId)
        :param userId:userId或者userIdStr均可
        """
        return self.__client.call("eleme.user.getOpenUserIdByUserId", {"userId": user_id})

