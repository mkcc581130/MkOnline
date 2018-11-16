# coding:utf-8

import base64
import hashlib
import httplib
import json
import urllib


class ExpressSearch(object):
    def __init__(self, shipper_code, logistic_code):
        self.request_data = '{"LogisticCode":"'+logistic_code+'","ShipperCode":"'+shipper_code+'"}'
        self.__params = {
            'EBusinessID': '1303360',
            'RequestType': '1002',
            'RequestData': urllib.quote(self.request_data),
            'DataType': '2'
        }

    def get_data(self):
        md5_data = hashlib.md5(self.request_data + '60f113a8-f4d9-4b6c-9607-e62c74bb2314').hexdigest()
        base64_data = base64.b64encode(md5_data)
        data_sign = urllib.quote(base64_data)
        self.__params.update({'DataSign': data_sign})
        args = urllib.urlencode(self.__params)
        host = 'api.kdniao.cc'
        urls = '/Ebusiness/EbusinessOrderHandle.aspx'
        conn = httplib.HTTPConnection(host, 80)
        conn.request('POST', urls, args, {"Content-type": "application/x-www-form-urlencoded"})
        r = conn.getresponse()
        read = r.read()
        data_all = json.dumps(json.loads(read))
        return data_all
