import json
from datetime import datetime

from dateutil.tz import tz

from .file_manager import LogFileManager
import time
import requests

ERROR_MSG = """
---------------------------------- {0} begin ----------------------------------
请求URL是：{1}
请求headers是：{2}
请求params是：{3}
请求post是：{4}
错误信息是：{5}
---------------------------------- {0} end ----------------------------------
"""


class ApiClient(requests.Session):
    def __init__(self, node_id: int, retry_count: int, timeout: int, host: str):
        """
        初始化API客户端基类
        :param node_id 节点ID
        :param retry_count 重试次数
        :param timeout 请求超时时间
        :param host 域名地址
        """
        super(ApiClient, self).__init__()
        self.retry_count = retry_count
        self.node_id = node_id
        self.timeout = timeout
        self.host = host

    def try_get(self, url, error_count: int = 0, **kwargs):
        """
        尝试重发get请求
        """
        while error_count <= self.retry_count:
            try:
                kwargs['timeout'] = self.timeout
                return self.get(url, **kwargs)
            except Exception as e:
                print(e)
                error_count += 1
                return self.try_get(url, error_count, **kwargs)

    def try_post(self, url: str, error_count: int = 0, **kwargs):
        """
        尝试重发post请求
        """
        while error_count <= self.retry_count:
            try:
                kwargs['timeout'] = self.timeout
                return self.post(url, **kwargs)
            except Exception as e:
                print(e)
                error_count += 1
                time.sleep(error_count)
                return self.try_post(url, error_count, **kwargs)
        raise Exception('已经尝试请求：{}次，服务器依然没有响应'.format(self.retry_count))


class MigoApiClient(ApiClient):
    def __init__(self, node_id: int, retry_count: int, timeout: int, host: str, auth_key: str, log_path: str):
        """
        初始化米果API客户端
        :param node_id 节点ID
        :param retry_count 重试次数
        :param timeout 请求超时时间
        :param host
        :param auth_key 认证key
        :param log_path 日志路径
        """
        super(MigoApiClient, self).__init__(node_id, retry_count, timeout, host)
        self.auth_key = auth_key
        self.headers = {
            'AUTH-KEY': auth_key,
            'CURRENT-USER-NAME': 'system',
            'CURRENT-USER-ID': '100001'
        }
        self.log_manager = LogFileManager(log_path)

    def try_post(self, url, error_count: int = 0, **kwargs):
        now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            kwargs['headers'] = kwargs.get('headers', dict())
            kwargs['headers'].update(self.headers)
            response = super(MigoApiClient, self).try_post(url, error_count, **kwargs)
            response_data = response.json()
            if response_data and response_data['code'] != 200:
                msg = ERROR_MSG.format(
                    now_datetime,
                    url,
                    kwargs.get('headers', ''),
                    kwargs.get('params', ''),
                    kwargs.get('json', {}),
                    response_data.get('message', ''),
                )
                self.log_manager.write_request_error_log(msg)
            return response_data
        except Exception as e:
            msg = ERROR_MSG.format(
                now_datetime,
                url,
                kwargs.get('headers', ''),
                kwargs.get('params', ''),
                kwargs.get('json', ''),
                str(e)
            )
            self.log_manager.write_system_error_log(msg)
            raise e

    def try_get(self, url, error_count: int = 0, **kwargs):
        now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            kwargs['headers'] = kwargs.get('headers', dict())
            kwargs['headers'].update(self.headers)
            response = super(MigoApiClient, self).try_get(url, error_count, **kwargs)
            response_data = response.json()
            if response_data and response_data['code'] != 200:
                msg = ERROR_MSG.format(
                    now_datetime,
                    url,
                    kwargs.get('headers', ''),
                    kwargs.get('params', ''),
                    kwargs.get('json', {}),
                    response_data.get('message', ''),
                )
                self.log_manager.write_request_error_log(msg)
                raise Exception(msg)
            return response_data
        except Exception as e:
            msg = ERROR_MSG.format(
                now_datetime,
                url,
                kwargs.get('headers', ''),
                kwargs.get('params', ''),
                kwargs.get('json', ''),
                str(e)
            )
            self.log_manager.write_system_error_log(msg)
            raise Exception(msg)

    def get_shop_auth(self, migo_shop_id: int):
        """
        获取店铺授权信息
        :param migo_shop_id 米果店铺ID
        """
        uri = f'/data-collection-service/node/auths/{migo_shop_id}'
        return self.try_get(self.host + uri)

    def get_node_info_list(self, migo_shop_id: int):
        """
        获取节点信息列表
        :param migo_shop_id 米果店铺ID
        """
        post_data = {
            "nodeConfigId": self.node_id,
            "shopId": migo_shop_id
        }
        uri = f'/data-collection-service/node/search'
        return self.try_post(self.host + uri, json=post_data)

    def post_auth_data(self, migo_shop_id, **kwargs):
        """
        刷新认证数据
        :param migo_shop_id 米果店铺ID
        :param kwargs 所需的认证参数
        """
        post_data = {
            "crawlData": json.dumps(kwargs),
            "nodeConfigId": self.node_id,
            "shopId": migo_shop_id
        }
        uri = '/data-collection-service/node/refresh'
        return self.try_post(self.host + uri, json=post_data)

    def post_crawl_data(self, crawl_data: dict):
        """
        推送采集数据
        :param crawl_data 采集数据
        """
        uri = '/data-collection-service/node/save'
        if 'tabelName' not in crawl_data:
            raise Exception('表名不能为空')
        elif 'shopId' not in crawl_data:
            raise Exception('店铺ID不能为空')
        return self.try_post(self.host + uri, json=crawl_data)

    def get_heartbeat(self):
        """
        发送心跳
        """
        uri = f'/data-collection-service/node/heartbeat/{self.node_id}'
        return self.try_get(self.host + uri, error_count=0)

    def post_error_log(self, error_msg: str, data_type: str, node_id: str, shop_id: str, log_data: dict = None,
                       log_params: dict = None, log_stack: str = None):
        """
        上传日志
        :param error_msg 错误信息
        :param data_type 数据类型
        :param node_id 节点ID
        :param shop_id 店铺ID
        :param log_data 请求的post参数
        :param log_params 请求的get参数
        :param log_stack 日志其他信息
        """
        uri = '/data-collection-service/node/logsave'
        post_data = {
            "data": [
                {
                    "id": str(time.time()).replace('.', ''),
                    "shopId": shop_id,
                    "nodeId": node_id,
                    "dataType": data_type,
                    "logTime": str(datetime.fromtimestamp(int(time.time()), tz.gettz('Asia/Shanghai'))),
                    "logData": json.dumps(log_data),
                    "logParams": json.dumps(log_params),
                    "logStack": log_stack,
                    "logMsg": error_msg
                }
            ],
            "primaryKey": "id",
            "refreshNow": 0,
            "tableName": "log_node_spider_error"
        }
        response_data = self.try_post(self.host + uri, 0, json=post_data)
        return response_data

    def post_info_log(self, msg: str, data_type: str, node_id: str, shop_id: str, log_data: dict = None,
                      log_params: dict = None, log_stack: str = None):
        """
        上传日志
        :param msg 错误信息
        :param data_type 数据类型
        :param node_id 节点ID
        :param shop_id 店铺ID
        :param log_data 请求的post参数
        :param log_params 请求的get参数
        :param log_stack 日志其他信息
        """
        uri = '/data-collection-service/node/logsave'
        post_data = {
            "data": [
                {
                    "id": str(time.time()).replace('.', ''),
                    "shopId": shop_id,
                    "nodeId": node_id,
                    "dataType": data_type,
                    "logTime": str(datetime.fromtimestamp(int(time.time()), tz.gettz('Asia/Shanghai'))),
                    "logData": json.dumps(log_data),
                    "logParams": json.dumps(log_params),
                    "logStack": log_stack,
                    "logMsg": msg
                }
            ],
            "primaryKey": "id",
            "refreshNow": 0,
            "tableName": "log_node_spider"
        }
        response_data = self.try_post(self.host + uri, 0, json=post_data)
        return response_data
