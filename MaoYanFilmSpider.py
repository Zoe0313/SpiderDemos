import requests
from lxml import etree
import random
import time
import csv

ua_list = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
    'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
]

class MaoyanSpider(object):
    def __init__(self):
        self.url = 'https://maoyan.com/films?showType={}&offset={}'

    def parse_page(self, type_index, page):
        url = self.url.format(type_index, page)
        html = requests.get(url, headers={'User-Agent':random.choice(ua_list)}).content.decode('utf-8')
        # 创建解析对象
        parse_html = etree.HTML(html)

        movie_list = []

        # 1.基准xpath：匹配每个电影信息的节点对象
        dd_list = parse_html.xpath('//dl[@class="movie-list"]//dd')
        # 2.for依次遍历每个节点对象，获取信息
        print(len(dd_list))
        for dd in dd_list:
            movie_dict = {}
            # 电影类型
            if 1==type_index:
                movie_dict['stype'] = 'now'
            elif 2==type_index:
                movie_dict['stype'] = 'later'
            elif 3==type_index:
                movie_dict['stype'] = 'classic'
            # 名称
            movie_dict['name'] = dd.xpath('.//div[@class="channel-detail movie-item-title"]/@title')[0].strip()
            if '周杰伦摩天轮演唱会 2014'==movie_dict['name'] or '钢铁侠4'==movie_dict['name']:
                continue
            # 评分
            if 2==type_index:
                movie_dict['score'] = int(random.uniform(10000,100000))
            else:
                scorelist = dd.xpath('.//div[@class="channel-detail channel-detail-orange"]/i/text()')
                movie_dict['score'] = ''.join(scorelist[:2])
            # 二级界面url
            movie_dict['detail_url'] = 'https://maoyan.com' + dd.xpath('.//div[@class="movie-item"]/a/@href')[0]

            res = self.parse_sub_page(movie_dict['detail_url'],movie_dict['name'])

            movie_dict.update(res)
            try:
                t = (movie_dict['name'],
                   movie_dict['stype'],
                   movie_dict['duration'],
                   movie_dict['region'],
                   movie_dict['score'],
                   movie_dict['stars'],
                   movie_dict['img_url'],
                   movie_dict['detail_url'],
                   movie_dict['release_time'],
                   movie_dict['introduce'],
                   movie_dict['content'])
            except Exception:
                print(movie_dict['name']+' error!')
                continue

            print(t)
            movie_list.append(t)
            time.sleep(0.5)

        return movie_list

    def parse_sub_page(self,url,name):
        movie_dict = {}
        html = requests.get(url, headers={'User-Agent': random.choice(ua_list)}).content.decode('utf-8')
        parse_html = etree.HTML(html)

        # 海报图片url
        img_str = parse_html.xpath('//div[@class="avatar-shadow"]/img/@src')[0]
        movie_dict['img_url'] = img_str.split('@')[0]

        # 下载图片
        self.download_img(movie_dict['img_url'],name)

        info_list = parse_html.xpath('//li[@class="ellipsis"]/text()')

        try:
            temp_str = info_list[1].split('/')
            # 时长
            if len(temp_str)>1:
                movie_dict['duration'] = temp_str[1].strip()
            else:
                movie_dict['duration'] = '100分钟'
            # 上映地区
            movie_dict['region'] = temp_str[0].strip()
            movie_dict['region'] = movie_dict['region'].replace(',',' ')
            # 上映时间
            movie_dict['release_time'] = info_list[2].strip()
            # 剧情
            movie_dict['content'] = parse_html.xpath('//div[@class="mod-content"]/span/text()')[0].replace(',',' ')
            # 摘要
            movie_dict['introduce'] = movie_dict['content'][:30]
            # 演员表
            stars = parse_html.xpath('//div[@class="celebrity-group"]//text()')
            star_names = []
            for star in stars:
                star_str = star.strip()
                if not star_str:
                    continue

                star_names.append(star_str)

            star_names = star_names[:10]
            directors = star_names[0] + ': ' + star_names[1]
            actors = star_names[2] + ': ' + ' '.join(star_names[3:])
            movie_dict['stars'] = directors + ' ' + actors
            movie_dict['stars'] = movie_dict['stars'].replace(',',' ')
        except Exception:
            movie_dict['duration'] = '100分钟'
            movie_dict['region'] = '中国大陆'
            movie_dict['release_time'] = '2020大陆上映'
            pass
        return movie_dict

    def download_img(self, img_url, name):
        try:
            img_filename = img_url.split('/')[-1]
            img_tail = img_filename.split('.')[-1]
            res = requests.get(url=img_url,
                               headers={'User-Agent':random.choice(ua_list)},
                               timeout=5).content
        except Exception as e:
            print(img_url + 'download failed')
            return

        filename = 'images/' + name + '.' + img_tail

        with open(filename, 'wb') as f:
            f.write(res)
            print('%s下载成功' % filename)


    def main(self):
        for type_index in range(1,4):
            for page in range(0,61,30):
                movie_list = self.parse_page(type_index,page)
                with open('MaoYanFilms.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(movie_list)

                time.sleep(random.randint(1, 3))
                print(type_index,page,'爬取结束')

if __name__ == '__main__':
    spider = MaoyanSpider()
    spider.main()
