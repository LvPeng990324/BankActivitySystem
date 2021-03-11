# 二维码方法
import qrcode
from six import BytesIO


def get_qrcode_stream(qr_text):
    img = qrcode.make(qr_text)

    buf = BytesIO()
    img.save(buf)
    qrcode_stream = buf.getvalue()
    return qrcode_stream
