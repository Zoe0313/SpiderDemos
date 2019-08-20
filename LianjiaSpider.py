import requests
import random
import time
import re
import csv
from useragents import ua_list

class LianjiaSpider(object):
    def __init__(self):
        self.url = 'https://sh.lianjia.com/zufang/pg{}/'
        self.pattern = re.compile(r'<p class="content__list--item--title twoline">.*?">(.*?)</a>'
                                  r'.*?"content__list--item--des">.*?">(.*?)</a>.*?">(.*?)</a>'
                                  r'(.*?)<span class="hide">.*?'
                                  r'<span class="content__list--item-price"><em>(.*?)</span>',re.S)

        # 二手房
        # self.url = 'https://sh.lianjia.com/ershoufang/pg{}/'
        # self.pattern = re.compile(r'data-is_focus="" data-sl="">(.*?)</a>.*?data-el="region">(.*?)</a>'
        #                           r'(.*?)</div></div><div class="flood">.*?<div class="totalPrice"><span>'
        #                           r'(.*?)</div><div class="unitPrice".*?><span>(.*?)</span>',re.S)

    def get_page(self,url):
        res = requests.get(url=url,headers={'User-Agent':random.choice(ua_list)})
        res.encoding = 'utf-8'
        return res.text

    def parse_page(self,html):
        house_list = self.pattern.findall(html)
        result = []
        for house in house_list:
            # 二手房
            # detail = house[0]# 标题
            # name = house[1].strip()# 楼盘名称
            # infos = house[2].split('|')# 房型信息 | 分隔
            # infos = [i.strip() for i in infos]
            # infos = infos[1:]
            # total_price = house[3].replace('</span>','')# 总价
            # unit_price = house[4]# 单价
            # t = (name,infos[0],infos[1],infos[2],infos[3],total_price,unit_price,detail)

            # 租房
            title = house[0].strip()# 标题
            region = house[1]# 区县
            road = house[2]# 街道
            infos = house[3].split('<i>/</i>')#多个li元素组成的信息，取第一个
            infos = [i.strip() for i in infos]
            infos = infos[1:]
            rent = house[4].replace('</em> ','')#月租
            # print('{},{},{},{}'.format(detail,region,road,rent))
            # print(infos)
            t = (title,region,road,infos[2],infos[0],infos[1],rent)
            result.append(t)
        return result

    def main(self):
        with open('链家租房.csv','a',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(('标题','区县','所在街道','房型','面积','朝向','月租'))
            # writer.writerow(('楼盘','房型','面积','朝向','装修','总价','单价','简介'))
            for page in range(1,10):
                url = self.url.format(page)
                html = self.get_page(url)
                result = self.parse_page(html)
                writer.writerows(result)
                print('第{}页爬取成功'.format(page))
                time.sleep(random.randint(1,3))

if __name__ == '__main__':
    start = time.time()
    spider = LianjiaSpider()
    spider.main()
    end = time.time()
    print('总耗时%.2f'%(end-start))