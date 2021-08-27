# 导出excel相关工具方法
import xlwt
from io import BytesIO
import datetime
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path


def excel_response(data_list, sheet_name):
    """ 写入excel并生成下载回应方法
    """
    # 创建工作薄
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建工作表
    worksheet = workbook.add_sheet(sheet_name)
    # 设置日期样式
    date_style = xlwt.XFStyle()
    date_style.num_format_str = 'YYYY-MM-DD'
    # 设置时间格式
    datetime_style = xlwt.XFStyle()
    datetime_style.num_format_str = 'YYYY-MM-DD hh:mm:ss'

    # 遍历列表写入excel
    row_index = 0  # 行索引
    col_index = 0  # 列索引
    for line in data_list:
        for col_index in range(len(line)):
            # 获取要写入的数据
            data = line[col_index]
            # 写入一个单元格
            # 判断是不是datetime类型
            # 是的话就加日期样式写入
            if isinstance(data, datetime.datetime):
                # 是日期类型，加入样式
                worksheet.write(row_index, col_index, data, datetime_style)
            elif isinstance(data, datetime.date):
                # 是时间类型，加入样式
                worksheet.write(row_index, col_index, data, date_style)
            else:
                # 不是日期类型，直接写入
                worksheet.write(row_index, col_index, data)
        # 行索引自增
        row_index += 1
    # 生成下载回应
    sio = BytesIO()
    workbook.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = "attachment;filename*=UTF-8''{}".format(escape_uri_path(sheet_name+'.xls'))
    response.write(sio.getvalue())
    return response


def export_activity_record_customer_info(data):
    """ 导出活动参与记录与客户信息表
    传入客户的QuerySet对象
    """
    # 将数据存入列表
    data_list = []  # 用于存储所有数据
    temp_list = []  # 用于临时存储一行，最后存入data_list
    # 建立表头
    temp_list = ['活动记录ID', '姓名', '标签', '性别', '手机号', '地址', '是否为商户', '是否安装微邮付', '是否为餐饮商户', '食盐配送',
                 '参与活动', '报名时间', '客户经理']
    data_list.append(temp_list)
    temp_list = []
    # 遍历数据库内容并存入data_list
    for line in data:
        temp_list.append(line.id)  # 活动记录ID
        temp_list.append(line.customer.name)  # 姓名
        temp_list.append(line.customer.tag)  # 标签
        temp_list.append(line.customer.gender)  # 性别
        temp_list.append(line.customer.phone)  # 手机号
        temp_list.append('{}-{}-{}-{}'.format(line.customer.town, line.customer.village, line.customer.group, line.customer.street))  # 地址
        temp_list.append('是' if line.customer.is_merchant else '否')  # 是否为商户
        temp_list.append('是' if line.customer.is_installed_micro_post_pay else '否')  # 是否安装微邮付
        temp_list.append('是' if line.customer.is_catering_merchant else '否')  # 是否为餐饮商户
        temp_list.append(line.customer.salt_delivery)  # 食盐配送
        temp_list.append(line.customer.activiey.name)  # 参与活动
        temp_list.append(line.create_time)  # 报名时间
        temp_list.append(line.admin_third.name)  # 客户经理

        # 存入data_list并清空temp_list
        data_list.append(temp_list)
        temp_list = []
    # 返回下载回应
    return excel_response(data_list, sheet_name='活动记录与客户信息表')


def export_give_merchandise_record(data):
    """ 导出商品发放记录表
    传入商品发放记录的QuerySet对象
    """
    # 将数据存入列表
    data_list = []  # 用于存储所有数据
    temp_list = []  # 用于临时存储一行，最后存入data_list
    # 建立表头
    temp_list = ['发放记录ID', '商品名', '发放人', '接收客户', '数量', '发放时间']
    data_list.append(temp_list)
    temp_list = []
    # 遍历数据库内容并存入data_list
    for line in data:
        temp_list.append(line.id)  # 发放记录ID
        temp_list.append(line.merchandise.name)  # 商品名
        temp_list.append(line.give_admin_name)  # 发放人
        temp_list.append('{}-{}'.format(line.customer.name, line.customer.phone))  # 接收客户
        temp_list.append(line.give_num)  # 数量
        temp_list.append(line.give_time)  # 发放时间

        # 存入data_list并清空temp_list
        data_list.append(temp_list)
        temp_list = []
    # 返回下载回应
    return excel_response(data_list, sheet_name='商品发放记录表')

