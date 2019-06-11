#!/usr/bin/env python
#coding:utf-8
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


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description=u'密码加密工具')
    parse.add_argument('-d', '--decode', action='store_true', help=u'解密模式,默认是加密模式')
    parse.add_argument('-k', '--key', help=u'秘钥')
    parse.add_argument('msg', help=u'消息内容')
    args = parse.parse_args()
    if args.decode:
        print(decode(args.key, args.msg))
    else:
        print(encode(args.key, args.msg))
