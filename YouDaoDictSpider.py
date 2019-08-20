import requests
import time
import random
from hashlib import md5

# 获取salt sign ts
def get_salt_sign_ts(word):
    salt = str(int(time.time()*1000))
    ts = str(random.randint(0,9))
    string = 'fanyideskweb' + word + salt + 'n%A-rKaT5fb[Gy?;N5@Tj'
    s = md5()
    s.update(string.encode())
    sign = s.hexdigest()
    return salt,ts,sign

# 破解有道
def attack_yd(word):
    # 有道翻译检查了Cookie、Referer、User-Agent
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '238',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=374112974@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=670622856.6691092; JSESSIONID=aaafqST0_YxC2d59jRIWw; ___rl__test__cookies=1563949866562',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Pragma': 'no-cache',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    # 请求的表单数据里，检查了salt、sign
    salt, ts, sign = get_salt_sign_ts(word)
    data = {
        'i': word,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'ts': ts,
        'bv': '4cb44256c2c2d3e6c1fb2c2b6e03c5f0',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }
    html_json = requests.post(
        url=url,
        data=data,
        headers=headers
    ).json()
    return html_json

if __name__=='__main__':
    word = input('请输入要翻译的单词：')
    result = attack_yd(word)
    #print(result)
    if result.get('errorCode')==0:
        trans_couple = result['translateResult'][0][0]
        print('{} -> {}'.format(trans_couple.get('src'),trans_couple.get('tgt')))

        if result.get('smartResult'):
            print('完整结果：')
            info_list = result['smartResult'].get('entries')
            for info in info_list:
                if not info:
                    continue
                print(info.strip())