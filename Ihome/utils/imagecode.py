# import random
# # import matplotlib.pyplot as plt
# import string
# import sys
# import math
# from PIL import Image,ImageDraw,ImageFont,ImageFilter
# filename="C:/Users/95244/Desktop"
# #字体的位置，不同版本的系统会有不同BuxtonSketch.ttf
# font_path = 'C:/Windows/Fonts/Georgia.ttf'
# #font_path = 'C:/Windows/Fonts/默陌肥圆手写体.ttf'
# #生成几位数的验证码
# number = 4
# #生成验证码图片的高度和宽度
# size = (129,53)
# #背景颜色，默认为白色
# bgcolor = (255,255,255)
# #字体颜色，默认为蓝色
# fontcolor = (0,0,0)
# #干扰线颜色。默认为红色
# linecolor = (0,0,0)
# #是否要加入干扰线
# draw_line = True
# #加入干扰线条数的上下限
# line_number = (1,5)
#
# #用来随机生成一个字符串
# def gene_text():
#     # source = list(string.letters)
#     # for index in range(0,10):
#     #     source.append(str(index))
#     source = ['0','1','2','3','4','5','6','7','8','9']
#     # source = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I','J', 'K','L', 'M', 'N','O','P','Q','R',
#     #           'S', 'T', 'U', 'V', 'W', 'Z','X', 'Y']
#     return ''.join(random.sample(source,number))#number是生成验证码的位数
# #用来绘制干扰线
# def gene_line(draw,width,height):
#     # begin = (random.randint(0, width), random.randint(0, height))
#     # end = (random.randint(0, width), random.randint(0, height))
#     begin = (0, random.randint(0, height))
#     end = (74, random.randint(0, height))
#     draw.line([begin, end], fill = linecolor,width=3)
#
# #生成验证码
# def gene_code():
#     width,height = size #宽和高
#     image = Image.new('RGBA',(width,height),bgcolor) #创建图片
#     font = ImageFont.truetype(font_path,40) #验证码的字体
#     draw = ImageDraw.Draw(image)  #创建画笔
#     text = gene_text() #生成字符串
#     font_width, font_height = font.getsize(text)
#     draw.text(((width - font_width) / number, (height - font_height) / number),text,\
#             font= font,fill=fontcolor) #填充字符串
#     if draw_line:
#         gene_line(draw,width,height)
#     image = image.transform((width+30,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  #创建扭曲
#     # image = image.transform((width+20,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  #创建扭曲
#     image = image.filter(ImageFilter.EDGE_ENHANCE_MORE) #滤镜，边界加强
#     # a = str(m)
#     aa = str(".png")
#     path = filename + text + aa
#     # cv2.imwrite(path, I1)
#     # image.save('idencode.jpg') #保存验证码图片
#     image.save(path)
# x = 1
# # if __name__ == "__main__":
# # for k in(1,1000):
# while x<20:
#      gene_code()
#      x += 1
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# from PIL import Image, ImageDraw, ImageFont, ImageFilter
# import random
#
#
# # random character
# def rndChar():
#     return chr(random.randint(65, 90))
#
#
# # random color 1
# def rndColor1():
#     return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
#
#
# # random color 2
# def rndColor2():
#     return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
#
#
# # 240 * 60
# width = 60 * 4
# height = 60
# image = Image.new('RGB', (width, height), (255, 255, 255))
#
# # create Font object
# myfont = ImageFont.truetype('C:/Windows/Fonts/Calibri.ttf', 36)
#
# # create Draw object
# draw = ImageDraw.Draw(image)
#
# # fill in every pixel
# for x in range(width):
#     for y in range(height):
#         draw.point((x, y), fill=rndColor1())
#
# # output the text
# for t in range(4):
#     draw.text((60 * t + 10, 10), rndChar(), font=myfont, fill=rndColor2())
#
# # fuzzy
# image = image.filter(ImageFilter.BLUR)
# image.save('newI1g.jpg', 'jpeg')

# 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
# 账户注册：请通过该地址开通账户http://user.ihuyi.com/register.html
# 注意事项：
# （1）调试期间，请使用用系统默认的短信内容：您的验证码是：【变量】。请不要把验证码泄露给其他人。
# （2）请使用 APIID 及 APIKEY来调用接口，可在会员中心获取；
# （3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；

# !/usr/local/bin/python
# -*- coding:utf-8 -*-
from urllib.parse import urlencode

import http.client
import urllib

host = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"

# 查看用户名 登录用户中心->验证码通知短信>产品总览->API接口信息->APIID
account = "C12847646"
# 查看密码 登录用户中心->验证码通知短信>产品总览->API接口信息->APIKEY
password = "1d7d17ea49e14ac50d138bb60f63d7db"


def send_sms(text, mobile):
    params = urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


if __name__ == '__main__':
    mobile = "18482100382"
    text = "您的验证码是：888888。请不要把验证码泄露给其他人。"

    print(send_sms(text, mobile))
