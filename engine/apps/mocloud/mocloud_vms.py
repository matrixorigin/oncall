import os
import logging

from alibabacloud_dyvmsapi20170525.client import Client as Dyvmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dyvmsapi20170525 import models as dyvmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from apps.mocloud.mocloud_template import DEFAULT_VMS_ALERT_TEMPLATE,VMS_ALERT_TEST_TEMPLATE, read_password_from_file


class MOCloudVMS:
    def __init__(self):
        if os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID") != None:
            ALIBABA_CLOUD_ACCESS_KEY_ID = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        else:
            ALIBABA_CLOUD_ACCESS_KEY_ID = read_password_from_file(os.environ.get("ACCESS_KEY_FILE"))

        if os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET") != None:
            ALIBABA_CLOUD_ACCESS_KEY_SECRET = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        else:
            ALIBABA_CLOUD_ACCESS_KEY_SECRET = read_password_from_file(os.environ.get("SECRET_KEY_FILE"))
        
        self.vms_client = MOCloudVMS.create_client(ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET)

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> Dyvmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret,
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dyvmsapi
        config.endpoint = f"dyvmsapi.aliyuncs.com"
        return Dyvmsapi20170525Client(config)

    def send_vms_notification(self, number, parmas):
        single_call_by_voice_request = dyvmsapi_20170525_models.SingleCallByTtsRequest(
            tts_param=parmas,
            speed=5,
            play_times=3,
            called_number=number,
            tts_code=DEFAULT_VMS_ALERT_TEMPLATE,
            volume=100,
        )
        try:
            # 复制代码运行请自行打印 API 的返回值
            self.vms_client.single_call_by_tts_with_options(single_call_by_voice_request, util_models.RuntimeOptions())
        except Exception as error:
            # 错误 message
            # print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
    
    def send_vms_test(self, number, parmas):
        single_call_by_voice_request = dyvmsapi_20170525_models.SingleCallByTtsRequest(
            tts_param=parmas,
            speed=5,
            play_times=3,
            called_number=number,
            tts_code=VMS_ALERT_TEST_TEMPLATE,
            volume=100,
        )
        try:
            self.vms_client.single_call_by_tts_with_options(single_call_by_voice_request, util_models.RuntimeOptions())
        except Exception as error:
            # 错误 message
            # print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
        pass