from ronglian_sms_sdk import SmsSDK
from BankActivitySystem import settings

accId = settings.accId
accToken = settings.accToken
appId = settings.appId


# 发送短信验证码方法
# 【礼县邮政】您的验证码为{1}，请于{2}分钟内正确输入，如非本人操作，请忽略此短信。
# 变量1：验证码
# 变量2：有效分钟数
# 模板ID：893451
# 参数1：要发送的手机号
# 参数2：验证码字符串
def send_msg_code(to_phone, msg_code):
    sdk = SmsSDK(accId, accToken, appId)
    tid = '893451'
    mobile = to_phone
    datas = (msg_code, '5')
    resp = sdk.sendMessage(tid, mobile, datas)
    return resp


# 发送通知提示方法
# 【礼县邮政】您好{1},您在我行有{2}条未读通知,请及时前往{3}查看，以免遗漏专属优惠.
# 变量1：客户姓名
# 变量2：未读通知数量
# 变量3：客户后台首页URL
# 模板ID：893433
# 参数1：要发送的手机号
# 参数2：客户姓名
# 参数3：未读通知数量
# 参数4：客户后台首页URL
def send_msg_notice(to_phone, name, unread_num, customer_url):
    sdk = SmsSDK(accId, accToken, appId)
    tid = '893433'
    mobile = to_phone
    datas = (name, unread_num, customer_url)
    resp = sdk.sendMessage(tid, mobile, datas)
    return resp


if __name__ == '__main__':
    pass
    # print(send_msg_code('13061299868', '123456'))

    # print(send_msg_notice(
    #     '13061299868',
    #     '吕鹏',
    #     3,
    #     'http://demo.lvpeng990324.cn/customer/customer-index/ '
    # ))
