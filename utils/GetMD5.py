# 将给定字符串MD5加密方法


import hashlib


def get_md5(password):
    m = hashlib.md5()
    m.update(password.encode())
    return m.hexdigest()


if __name__ == '__main__':
    data = '0001'
    print(get_md5(data))
