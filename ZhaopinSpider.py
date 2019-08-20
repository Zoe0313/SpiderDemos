import requests
from urllib import parse
import csv
import time
import random
from lxml import etree
from fake_useragent import UserAgent

class ZhaopinSpider(object):
    def __init__(self, keyword):
        self.keyword = keyword

        referer_url = 'https://sou.zhaopin.com/?jl=538&kw={}&kt=3'.format(parse.quote(keyword))

        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://sou.zhaopin.com',
            'Referer': referer_url,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

        self.params = {
            'start': '0',
            'pageSize': '90',
            'cityId': '538',# 上海
            'workExperience': '-1',
            'education': '-1',
            'companyType': '-1',
            'employmentType': '-1',
            'jobWelfareTag': '-1',
            'kw': self.keyword,
            'kt': '3#/'
        }

    def parse_html(self,page):
        self.params['start'] = page * 90
        query_string = parse.urlencode(self.params)
        url = 'https://fe-api.zhaopin.com/c/i/sou?{}'.format(query_string)
        print('正在抓取: ', url)

        html = requests.get(url,headers=self.headers).json()
        if 200==html['code']:
            job_list = html['data']['results']
            csv_list = []
            for job in job_list:
                try:
                    d = {}
                    d['jobName'] = job['jobName'] #职位名称
                    d['salary'] = job['salary'] #薪资
                    d['exp'] = job['workingExp']['name'] #工作经验
                    d['time'] = job['updateDate'] #更新时间
                    d['edu'] = job['eduLevel']['name'] #学历要求
                    d['jobType'] = job['emplType'] #全职、兼职
                    d['score'] = job['score'] #岗位评分
                    d['jobUrl'] = job['positionURL'] #岗位详情链接
                    d['welfare'] = ','.join(job['welfare']) #福利
                    company_dict = job['company']
                    d['companyName'] = company_dict['name'] #公司名称
                    d['companySize'] = company_dict['size']['name'] #公司规模
                    d['companyType'] = company_dict['type']['name'] #公司类型
                    d['companyUrl'] = company_dict['url'] #公司详情url

                    post_tuple = self.parse_sub_html(d['jobUrl'])

                    print('job:',d['jobName'])

                    t = (d['jobName'],d['salary'],d['exp'],d['time'],d['edu'],d['score'],d['welfare'],d['companyName'],d['companySize'],d['companyType'],d['jobUrl'],d['companyUrl']) + post_tuple

                    csv_list.append(t)
                except Exception:
                    continue
            return csv_list

    def parse_sub_html(self, post_url):
        sub_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': post_url,
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

        res = requests.get(post_url, headers=sub_headers, timeout=2)
        html = res.content.decode('utf-8', 'ignore')
        parse_html = etree.HTML(html)
        detail_list = parse_html.xpath('//div[@class="describtion__detail-content"]//text()')

        job_detail = ''
        for detail in detail_list:
            job_detail += detail.strip()
        address = ''
        a_list = parse_html.xpath('//div[@class="job-address"]/div/span/text()')
        if len(a_list)>0:
            address = a_list[0].strip()

        print("address:",address,len(detail_list))
        return (address,job_detail)

    def main(self):
        with open(self.keyword + '岗位列表.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(('职位名称', '薪资', '工作经验', '更新时间', '学历要求', '岗位评分', '福利', '公司名称', '公司规模', '公司类型', '岗位链接', '公司链接', '公司地址', '职位详情'))
            # 默认抓取前2页职位列表，要是某一页无信息，则中断
            for page in range(1):
                result = self.parse_html(page)
                if not result:
                    break

                writer.writerows(result)
                time.sleep(random.uniform(1,3))


if __name__=='__main__':
    kw = input('请输入要搜索的职位：')
    if kw:
        spider = ZhaopinSpider(kw)
        spider.main()