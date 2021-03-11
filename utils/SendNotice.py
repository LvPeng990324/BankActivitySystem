# 给客户推送通知相关方法
from django.db.models import Q
from BankActivitySystem.settings import DEPLOY_DOMAIN

from Customer.models import Customer
from Notice.models import NoticeTemplate
from Notice.models import Notice

from utils.SendMessage import send_msg_notice


def send_one(send_customer_id, notice_template_id, need_msg):
    """
    给一个客户推送通知
    :param send_customer_id: 要推送的客户id
    :param notice_template_id: 要推送的通知模板id
    :param need_msg: 是否需要发送短信
    :return:
    """
    # 取出客户和通知模板
    customer = Customer.objects.get(id=send_customer_id)
    notice_template = NoticeTemplate.objects.get(id=notice_template_id)
    # 推送通知，也即创建通知
    Notice.objects.create(
        title=notice_template.title,
        content=notice_template.content,
        customer=customer
    )

    # 判断是否需要发送短信通知
    if need_msg:
        # 客户手机号
        phone = customer.phone
        # 客户姓名
        name = customer.name
        # 客户未读通知数量
        unread_num = Notice.objects.filter(
            Q(customer=customer),
            Q(is_read=False)
        ).count()
        # 客户后台首页URL
        # http://127.0.0.1:8000/customer/customer-index/
        # http://demo.lvpeng990324.cn/customer/customer-index/
        # URL似乎最后需要加个空格或标点，不然会连着模板里链接后面两个字也被手机识别成链接，导致访问404
        customer_url = '{domain}/customer/customer-index/ '.format(domain=DEPLOY_DOMAIN)
        # customer_url = 'http://demo.lvpeng990324.cn/customer/customer-index/ '
        # 发送短信
        send_msg_notice(phone, name, unread_num, customer_url)


def batch_send(send_customer_ids, notice_template_id, need_msg):
    """
    批量推送通知
    :param send_customer_ids: 要推送的客户id们
    :param notice_template_id: 要推送的通知模板id
    :param need_msg: 需不需要发送短信
    :return:
    """
    send_customer_ids = send_customer_ids.split(',')
    for send_customer_id in send_customer_ids:
        send_one(send_customer_id, notice_template_id, need_msg)
        # print('给{}发送{}通知，短信：{}'.format(send_customer_id, notice_template_id, need_msg))
