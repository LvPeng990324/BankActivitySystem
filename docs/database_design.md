> 此文档简洁的记录了本系统的数据库结构，可供快速理解项目以及开发时候作简略参考

> 每张表都有一个框架自动添加的id字段，是自增的int类型

# Customer 客户

- name 姓名
- gender 性别
- town 镇子
- village 村子
- group 组
- street 街道
- phone 手机号码
- tag 标签
- tag_type 标签类型
- is_vip 是否会员
- card_num 邮政卡卡号
- password 密码
- comment 备注

# NoticeTemplate 通知模板

> 由二级管理员创建的通知内容

- title 标题
- content 内容
- create_time 创建时间

# Notice 通知

> 发送给客户的通知，通过外键指定客户

- title 标题
- content 内容
- create_time 发布时间
- customer 客户 --外键
- is_read 是否已查看

# AdminThird 三级管理员

- name 姓名
- job_num 工号
- password 密码
- admin_second 二级管理员 --外键

# AdminSecond 二级管理员

- name 姓名
- job_num 工号
- password 密码

# AdminFirst 一级管理员

- name 姓名
- job_num 工号
- password 密码

# AdminZero 零级管理员

- name 姓名
- job_num 工号
- password 密码

# Activity 活动

> 活动主体，记录活动的所有信息

- name 活动名
- create_time 创建时间
- end_time 截止时间
- content 介绍
- admin_second 二级管理员 --外键
- is_delete 是否已删除

# ActivityRecord 活动记录

> 标记了活动与参与客户以及三级管理员关系

- activity 活动 --外键
- customer 客户 --外键
- admin_third 三级管理员 --外键
- create_time 报名时间

# Town 镇子

- name 镇名

# Village 村子

- name 村名
- town 镇名 --外键

# Group 组

- name 组名
- village 村名 --外键

# Merchandise 商品

- name 商品名
- remain_num 库存量
- description 介绍