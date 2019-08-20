import requests
import execjs
import re

class BaiduDictSpider(object):
    def __init__(self):
        self.token_url = 'https://fanyi.baidu.com/?aldtype=16047'
        self.trans_url = 'https://fanyi.baidu.com/v2transapi'
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': 'BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BIDUPSID=637E743104C3906898A296E55090EFFA; BAIDUID=2EFD145791137F7FA5C7515D00D416E1:FG=1; PSTM=1564019985; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; delPer=0; PSINO=5; H_PS_PSSID=1436_21121_29578_29518_28518_29099_29567_28830_29220_29071; locale=zh; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1564019996,1564025617,1564025621; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1564025621; yjs_js_security_passport=8bad0cc9e064b9ceaa03ac1cfb3943f94c5c43b6_1564025622_js',
            'pragma': 'no-cache',
            'referer': 'https://www.baidu.com/link?url=cT5jAWd2BIFD5qjjBhljr7a3HE8DvxRbZDB4H9ZAfg1dg-z6FWjgyLi_3RKHriA6YNlHp3-7dVZIvhq3d8k7Oq&wd=&eqid=c9519d6e00043416000000045d39230e',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        self.token = self.get_token()

    def get_token(self):
        html = requests.get(url=self.token_url,headers=self.headers).text
        pattern = re.compile("token: '(.*?)'",re.S)
        token = pattern.findall(html)[0]
        # print('token: ',token)
        return token

    def get_sign(self,word):
        with open('baidu_trans_tool.js', 'r') as f:
            js_data = f.read()
        exec_obj = execjs.compile(js_data)
        sign = exec_obj.call("e",word)
        # print('sign: ',sign)
        return sign

    def get_lang_detect(self,word):
        # 检测源语言是什么语言
        detect_url = 'https://fanyi.baidu.com/langdetect'
        data = {
            'query': word
        }
        result = requests.post(url=detect_url,
                               headers=self.headers,
                               data=data).json()
        #{error: 0, msg: "success", lan: "zh"}
        return result['lan']

    def translate(self, word):
        from_lang = self.get_lang_detect(word)
        to_lang = 'zh'
        if from_lang=='zh':
            to_lang = 'en'
        data = {
            'from': from_lang,#'auto',
            'to': to_lang,#'auto',
            'query': word,
            'transtype': 'realtime',#''enter',
            'simple_means_flag': '3',
            'sign': self.get_sign(word),
            'token': self.token
        }
        result = requests.post(url=self.trans_url,
                               headers=self.headers,
                               data=data).json()
        #print(result)
        return result

if __name__=='__main__':
    spider = BaiduDictSpider()

    while True:
        word = input('请输入要翻译的单词：（按q退出）')
        if word=='q':
            break
        result = spider.translate(word)

        data_list = result['trans_result']['data']
        for data in data_list:
            print(data['dst'])