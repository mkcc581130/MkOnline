# coding: utf8
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest, QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
import random
from management.models import Verify
import json


class Sms(object):
    def __init__(self):
        self.ACCESS_KEY_ID = "LTAIRtKXRCVSjcMc"
        self.ACCESS_KEY_SECRET = "Bqf0z4nbK5DaJcqZAliYJw52o0vP61"
        self.acs_client = AcsClient(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET, "cn-hangzhou")

    def set_access_key(self, access_key_id, access_key_secret):
        self.ACCESS_KEY_ID = access_key_id
        self.ACCESS_KEY_SECRET = access_key_secret

    def send_sms(self, phone_number, sign_name, template_code):
        ran = ''
        for i in range(0, 6):
            ran += str(random.randint(0, 9))
        template_param = '{\"code\":\"'+ran+'\"}'
        acs_client = AcsClient(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET, "cn-hangzhou")
        business_id = uuid.uuid1()
        sms_request = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        sms_request.set_TemplateCode(template_code)
        # 短信模板变量参数,友情提示:如果JSON中需要带换行符,请参照标准的JSON协议对换行符的要求,比如短信内容中包含\r\n的情况在JSON中需要表示成\\r\\n,否则会导致JSON在服务端解析失败
        if template_param is not None:
            sms_request.set_TemplateParam(template_param)
        # 设置业务请求流水号，必填。
        sms_request.set_OutId(business_id)
        # 短信签名
        sms_request.set_SignName(sign_name)
        # 短信发送的号码，必填。支持以逗号分隔的形式进行批量调用，批量上限为1000个手机号码,批量调用相对于单条调用及时性稍有延迟,验证码类型的短信推荐使用单条调用的方式
        sms_request.set_PhoneNumbers(phone_number)
        # 发送请求
        sms_response = acs_client.do_action_with_exception(sms_request)
        sms_response_loads = json.loads(sms_response)
        if sms_response_loads['Code'] == 'OK':
            try:
                verify = Verify.objects.get(tel=phone_number)
                verify.code = ran
                verify.save()
            except:
                Verify(tel=phone_number, code=ran).save()
            return True
        else:
            return False

    def query_send_detail(self, biz_id, phone_number, page_size, current_page, send_date):
        acs_client = AcsClient(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET, "cn-hangzhou")
        query_request = QuerySendDetailsRequest.QuerySendDetailsRequest()
        # 查询的手机号码
        query_request.set_PhoneNumber(phone_number)
        # 可选 - 流水号
        query_request.set_BizId(biz_id)
        # 必填 - 发送日期 支持30天内记录查询，格式yyyyMMdd
        query_request.set_SendDate(send_date)
        # 必填-当前页码从1开始计数
        query_request.set_CurrentPage(current_page)
        # 必填-页大小
        query_request.set_PageSize(page_size)
        query_response = acs_client.do_action_with_exception(query_request)
        return query_response

# __business_id = uuid.uuid1()
# params = "{\"code\":\"12345\",\"product\":\"云通信\"}"
# print send_sms(__business_id, "1500000000", "云通信产品", "SMS_000000", params)