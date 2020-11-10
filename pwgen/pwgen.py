#!/usr/bin/env python
#coding:utf-8
"""
使用方法：
1. 如果系统没有python，请先安装python。
2. 启动命令行，windows操作系统中是：开始 > 命令提示符。Mac操作系统中是：应用程序 > 终端。
3. 在命令行中输入以下命令：  python  pwgen.py -s
4. 正常情况下，会有一些输出信息，找到类似于 http://0.0.0.0:3722  的网址，复制到浏览器打开即可。
"""
from __future__ import print_function
import argparse
import base64
from Crypto.Cipher import AES
from Crypto import Random

# padding算法
BS = AES.block_size # aes数据分组长度为128 bit
pad = lambda s: s + (BS - len(s) % BS) * chr(0)
aes_mode = AES.MODE_CBC

def preprocess_key(key):
    key_len = len(key)
    if key_len <= 16:
        key = key + ('0' * (16 - key_len))
    elif key_len <= 24:
        key = key + ('0' * (24 - key_len))
    elif key_len <= 32:
        key = key + ('0' * (32 - key_len))
    else:
        raise Exception('length of key must no more than 32')
    return key

def encode(key, msg):
    key = preprocess_key(key)

    iv = Random.new().read(AES.block_size)
    cryptor = AES.new(key, aes_mode, iv)
    out = cryptor.encrypt(pad(msg))

    return base64.b64encode(iv + out)

def decode(key, msg):
    key = preprocess_key(key)
    msg = base64.b64decode(msg)
    iv = msg[0:AES.block_size]
    ciphertext = msg[AES.block_size:len(msg)]
    cryptor = AES.new(key, aes_mode, iv)
    out = cryptor.decrypt(ciphertext)

    return out.rstrip(chr(0))

def run_server():
    from flask import Flask, render_template, request
    import json, random
    app = Flask(__name__)

    @app.route('/', methods = ['GET', 'POST'])
    def index():
        if request.method == 'GET':
            tpl = u'''
<form action="/" method="post">
    秘钥: <input name="key" type="password">
    数据: <input name="msg">
    模式: <input type="radio" name="mode" value="encode" checked>加密 <input type="radio" name="mode" value="decode">解密
    <input type="submit" value="提交" onclick="">
</form>
			'''
            return tpl, {'Context-Type': 'text/html;charset:utf-8'}
        else:
            mode = request.form['mode']
            key = str(request.form['key'])
            msg = str(request.form['msg'])
            if mode == 'encode':
                out = encode(key, msg)
            elif mode == 'decode':
                out = decode(key, msg)
            data = {
                'out' : out,
                'status' : 200
            }
            return json.dumps(data, ensure_ascii=False), {'Content-Type':'application/json'}

    app.run('0.0.0.0', port=random.randint(2049, 10000))


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description=u'密码加密工具')
    parse.add_argument('-s', '--server', action='store_true', help=u'启动web服务')
    parse.add_argument('-d', '--decode', action='store_true', help=u'解密模式,默认是加密模式')
    parse.add_argument('-k', '--key', help=u'秘钥')
    parse.add_argument('msg', nargs='?', help=u'消息内容')
    args = parse.parse_args()
    if args.server:
        run_server()
        exit(0)
    if args.key is None or args.msg is None:
        parse.print_help()
        exit(1)
    elif args.decode:
        print(decode(args.key, args.msg))
    else:
        print(encode(args.key, args.msg))
