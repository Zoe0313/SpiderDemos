import requests
import csv

class AldzsSpider(object):
    def __init__(self):
        self.url = 'https://zhishuapi.aldwx.com/Main/action/Dashboard/Homepage/data_list'
        self.sub_url = 'https://zhishuapi.aldwx.com/Main/action/Miniapp/App/appDetails'
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "http://www.aldzs.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        }

    def get_page(self,url,data):
        result = requests.post(url=url,
                               headers=self.headers,
                               data=data).json()
        if result['code']!=200:
            return None
        return result['data']

    def parse_page(self):
        data = {
            'type': 0,
            'typeid': 1,  # 游戏类型
            'date': 1,  # 1:日榜单  2:周榜单
            'size': 100, # 榜单数量
            'token': ''
        }
        result = self.get_page(self.url, data)
        if not result:
            return None

        csv_list = []
        app_list = result
        for app in app_list:
            app_value = app['aldzs'] # 阿拉丁今日指数
            app_grow = app['grow'] # 成长指数
            app_type = app['category'] # 小程序类型
            app_name = app['name'] # 小程序名称
            app_id = app['id'] # 小程序id
            detail = self.parse_sub_page(app_id)

            t = (app_id, app_name, app_type, app_value, app_grow, detail[0], detail[1], detail[2])
            csv_list.append(t)
            print(t)

        return csv_list

    def parse_sub_page(self, app_id):
        data = {
            'id': app_id,
            'token': ''
        }
        result = self.get_page(self.sub_url, data)
        if not result:
            return None

        detail = result['details']
        app_entity = detail['app_entity'] # 公司名称
        app_desc = detail['desc'] # app描述
        app_line = result['lineChat'] # 阿拉丁月指数曲线表
        return (app_entity,app_desc,app_line)

    def main(self):
        result = self.parse_page()
        with open('阿拉丁指数100榜.csv','w') as f:
            writer = csv.writer(f)
            writer.writerows(result)

if __name__=='__main__':
    spider = AldzsSpider()
    spider.main()