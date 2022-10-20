# -*- coding: utf-8 -*-
import json
from Tea.core import TeaCore

from alibabacloud_alidns20150109.client import Client as Alidns20150109Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alidns20150109 import models as alidns_20150109_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient


class AliDNS:
    def __init__(self):
        pass

    @staticmethod
    def create_client(access_key_id: str, access_key_secret: str) -> Alidns20150109Client:
        config = open_api_models.Config(access_key_id=access_key_id, access_key_secret=access_key_secret)
        config.endpoint = 'alidns.cn-beijing.aliyuncs.com'
        return Alidns20150109Client(config)

    @staticmethod
    def main(access_key_id, access_key_secret, record_id, value, type, rr) -> None:
        client = AliDNS.create_client(access_key_id, access_key_secret)
        update_domain_record_request = \
            alidns_20150109_models.UpdateDomainRecordRequest(record_id=record_id, value=value, type=type, rr=rr)
        resp = client.update_domain_record(update_domain_record_request)
        ConsoleClient.log(UtilClient.to_jsonstring(TeaCore.to_map(resp)))

    @staticmethod
    def get_dns_info(access_key_id, access_key_secret, record_id) -> str:
        client = AliDNS.create_client(access_key_id, access_key_secret)
        describe_domain_record_info_request = alidns_20150109_models.DescribeDomainRecordInfoRequest(record_id=record_id)
        resp = client.describe_domain_record_info(describe_domain_record_info_request)
        json_str = UtilClient.to_jsonstring(TeaCore.to_map(resp))
        data = json.loads(json_str)
        return str(data['body']['Value'])