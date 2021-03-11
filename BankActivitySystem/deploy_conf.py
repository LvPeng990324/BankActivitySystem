# 此处存放系统部署时候相对于开发环境可能需要更改的配置项
# 将由同目录的settings.py文件读取本文件所有配置项
from pathlib import Path


DEBUG = True

ALLOWED_HOSTS = ['*', ]


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 容联云短信
# 容联云通讯分配的主账号ID
accId = ''
# 容联云通讯分配的主账号TOKEN
accToken = ''
# 容联云通讯分配的应用ID
appId = ''

# 部署环境的域名，用于拼接二维码链接以及短信内容等
# 如果有端口记得端口也加上
DEPLOY_DOMAIN = 'http://127.0.0.1:8000'
