# 生成图片验证码方法

import os
import random
import base64
from io import BytesIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def random_color():
    c1 = random.randint(0, 255)
    c2 = random.randint(0, 255)
    c3 = random.randint(0, 255)
    return c1, c2, c3


def generate_picture(width=120, height=35):
    image = Image.new('RGB', (width, height), random_color())
    return image


def random_str():
    '''
    获取一个随机字符, 数字或小写字母
    :return:
    '''
    random_num = str(random.randint(0, 9))
    random_low_alpha = chr(random.randint(97, 122))
    random_char = random.choice([random_num, random_low_alpha])
    return random_char

def draw_str(count, image, font_size):
    """
    在图片上写随机字符
    :param count: 字符数量
    :param image: 图片对象
    :param font_size: 字体大小
    :return:
    """
    draw = ImageDraw.Draw(image)
    # 获取一个font字体对象参数是ttf的字体文件的目录，以及字体的大小
    font_file = os.path.join('Andale Mono.ttf')
    font = ImageFont.truetype(font_file, size=font_size)
    temp = []
    for i in range(count):
        random_char = random_str()
        draw.text((10+i*30, -2), random_char, random_color(), font=font)
        temp.append(random_char)

    valid_str = "".join(temp)    # 验证码
    return valid_str, image


def noise(image, width=120, height=35, line_count=3, point_count=20):
    '''

    :param image: 图片对象
    :param width: 图片宽度
    :param height: 图片高度
    :param line_count: 线条数量
    :param point_count: 点的数量
    :return:
    '''
    draw = ImageDraw.Draw(image)
    for i in range(line_count):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=random_color())

        # 画点
        for i in range(point_count):
            draw.point([random.randint(0, width), random.randint(0, height)], fill=random_color())
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.arc((x, y, x + 4, y + 4), 0, 90, fill=random_color())

    return image


def valid_code():
    """
    生成图片验证码,并对图片进行base64编码
    :return:
    """
    image = generate_picture()
    valid_str, image = draw_str(4, image, 35)
    image = noise(image)

    f = BytesIO()
    image.save(f, 'png')        # 保存到BytesIO对象中, 格式为png
    data = f.getvalue()
    f.close()

    encode_data = base64.b64encode(data)
    data = str(encode_data, encoding='utf-8')
    img_data = "data:image/jpeg;base64,{data}".format(data=data)
    return valid_str, img_data


if __name__ == '__main__':
    print(valid_code())
