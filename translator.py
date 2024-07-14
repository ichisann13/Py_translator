# -*- coding: utf-8 -*-

import requests
import random
from hashlib import md5

def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

def init_key():
    try:
        with open("./key.txt", "r", encoding="utf-8") as f:
            infor = f.readlines()
            if infor[0].strip() != "" and infor[1].strip() != "":
                appid = infor[0].strip()
                appkey = infor[1].strip()
            
            else:
                print("缺少密钥")
                exit(1)

    except FileNotFoundError as e:
        print("key.txt不存在")
        exit(1)

    return appid, appkey

def init_translator(source_lang):
    # 自动检测auto, 英文en, 中文zh
    from_lang = source_lang
    to_lang =  'zh'
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

    return from_lang, to_lang, url

def translator(source_text, source_lang):    
    appid, appkey = init_key()
    from_lang, to_lang, url = init_translator(source_lang)

    while True:
        query = source_text
        if query == "":
            continue

        else:
            # 生成salt
            salt = random.randint(32768, 65536)

            # 计算签名值, 拼接顺序:appid, query, salt, appkey
            sign = make_md5(appid + query + str(salt) + appkey)

            # 使用post方式发送要指定Content-Type为application/x-www-form-urlencoded
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

            # 发送请求
            req = requests.post(url, params=payload, headers=headers)
            result = req.json()

            # 取出翻译结果
            trans_result = result["trans_result"][0]["dst"]
            print(trans_result)