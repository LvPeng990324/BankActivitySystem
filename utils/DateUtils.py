# 日期相关
import datetime


def check_date_in_range(start_date: datetime.date, end_date: datetime.date, now_date=datetime.date.today()):
    """ 判断给定日期是否在给定起止日期段内
    """
    if start_date > now_date or end_date < now_date:
        return False
    else:
        return True



