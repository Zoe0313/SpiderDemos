## 目录

- [链家二手房数据抓取案例（re）](#链家二手房数据抓取案例（re）)
- [猫眼电影数据抓取案例（xpath）](#猫眼电影数据抓取案例（xpath）)
- [智联招聘python岗位数据抓取案例（xpath）](智联招聘python岗位数据抓取案例（xpath）)
- [阿拉丁指数数据抓取案例](#阿拉丁指数数据抓取案例)
- [有道翻译破解案例](#有道翻译破解案例)
- [百度翻译破解案例](#百度翻译破解案例)


## **链家租房数据抓取案例（re）**

**目标**

```python
1、地址: 链家 - 租房
2、目标: 标题信息、区县、所在街道、房型、面积、朝向、月租金
```

**实现步骤**

**1、确定是否为静态页面**

```python
打开租房页面 -> 查看网页源码 -> 搜索关键字
```

**2、正则表达式re**

```python
1、基准re(匹配每个房源信息节点列表)
    '<p class="content__list--item--title twoline">.*?">(.*?)</a>'
    '.*?"content__list--item--des">.*?">(.*?)</a>.*?">(.*?)</a>'
    '(.*?)<span class="hide">.*?'
    '<span class="content__list--item-price"><em>(.*?)</span>'
2、依次遍历后每个房源信息的获取
```

**3、将抓取到的数据存入csv文件**



## **猫眼电影数据抓取案例（xpath）**

**目标**

```python
 1、地址: 猫眼电影 - 热门电影、即将上映、经典电影 - 翻页
 2、目标: 电影名称、上映时间、上映地区、电影时长、演员表、剧情、海报下载
```

**实现步骤**

**1、确定基准URL地址**

```python
Request URL(基准URL地址) ：https://maoyan.com/films?showType={}&offset={}
  showType - 1:热门电影 2:即将上映 3:经典电影
  offset - 页码 page*30
```

**2、获取电影信息的xpath表达式**

```python
1、基准xpath：匹配每个电影信息的节点对象
    //dl[@class="movie-list"]//dd
    
2、遍历对象列表，依次获取每个电影信息
   for dd in dd_list:
     电影名称 ：dd.xpath('.//div[@class="channel-detail movie-item-title"]/@title')[0].strip()
     电影评分 ：dd.xpath('.//div[@class="channel-detail channel-detail-orange"]/i/text()')[0].strip()
     详情界面url ：'https://maoyan.com' + dd.xpath('.//div[@class="movie-item"]/a/@href')[0]
```

**3、获取电影海报下载url的xpath表达式**

```python
1、请求二级页面URL
2、海报图片url的xpath表达式：
    //div[@class="avatar-shadow"]/img/@src
3、设置超时时间为5秒，请求下载海报信息并wb到本地文件中
```

**4、将抓取到的数据存入csv文件**



## **智联招聘python岗位数据抓取案例（xpath）**

**目标**

```python
1、地址: 智联招聘 - 地区：上海 - 搜索岗位：python
2、目标: 职位名称, 薪资, 工作经验, 更新时间, 学历要求, 岗位评分, 福利, 公司名称, 公司规模, 公司类型, 公司地址, 职位详情
```

**实现步骤**

**1、一级页面json地址   F12抓包（XHR）**

```python
1、Request URL(基准URL地址) ：https://fe-api.zhaopin.com/c/i/sou?{}
2、Query String(查询参数)
# 抓取的查询参数如下：
    'start': '0',# 页码变化规律：page*90
    'pageSize': '90',
    'cityId': '538',# 上海
    'workExperience': '-1',
    'education': '-1',
    'companyType': '-1',
    'employmentType': '-1',
    'jobWelfareTag': '-1',
    'kw': self.keyword,# 搜索关键字：Python
    'kt': '3#/'
```

**2、二级页面为静态页面 (URL在一级页面中可拿到)**

```python
1、Request URL(基准URL地址) ：一级页面的jobUrl
2、xpath获取职位详情：'//div[@class="describtion__detail-content"]//text()'
3、xpath获取公司地址：'//div[@class="job-address"]/div/span/text()'
```

**3、将抓取到的数据存入csv文件**



### 阿拉丁指数数据抓取案例

**目标**

```python
1、地址: 阿拉丁指数 - 排行榜 - 游戏
2、目标: 阿拉丁今日指数、成长指数、小程序名称、发行公司、小程序描述、阿拉丁月指数曲线表
```

**实现步骤**

**1、一级页面json地址   F12抓包（XHR）**

```python
1、Request URL(基准URL地址) ：https://zhishuapi.aldwx.com/Main/action/Dashboard/Homepage/data_list
2、Query String(查询参数)
# 抓取的查询参数如下：
  'type': 0,
  'typeid': 1,  # 小程序类型:游戏
  'date': 1,  # 1:日榜单  2:周榜单
  'size': 100, # 榜单数量
  'token': ''
```

**2、二级页面json地址 (id在变,在一级页面中可拿到)**

```python
1、Request URL(基准URL地址) ：https://zhishuapi.aldwx.com/Main/action/Miniapp/App/appDetails
2、Query String(查询参数)
# 抓取的查询参数如下：
  'id': app_id,  # 小程序id
  'token': ''
```

**3、将抓取到的数据存入csv文件**



### 有道翻译破解案例

**目标：破解有道翻译接口，抓取翻译结果**

**实现步骤**

**1、浏览器F12开启网络抓包,Network-All,页面翻译单词后找Form表单数据**

**2、在页面中多翻译几个单词，观察Form表单数据变化（有数据是加密字符串）**

```python
salt: 15614112641250
sign: 94008208919faa19bd531acde36aac5d
ts: 1561411264125
bv: f4d62a2579ebb44874d7ef93ba47e822 # bv的值不变
```

**3、刷新有道翻译页面，抓取并分析JS代码（本地JS加密）**

```javascript
搜索salt - 查看fanyi.min.js文件 - 找到如下JS代码：
    var r = function(e) {
        var t = n.md5(navigator.appVersion)
          , r = "" + (new Date).getTime()
          , i = r + parseInt(10 * Math.random(), 10);
        return {
            ts: r,
            bv: t,
            salt: i,
            sign: n.md5("fanyideskweb" + e + i + "n%A-rKaT5fb[Gy?;N5@Tj")
        }
    };
```

**4、用Python按同样方式加密生成加密数据**

```python
# ts : 经过分析为13位的时间戳，字符串类型
js代码实现:  "" + (new Date).getTime()
python实现:  str(int(time.time()*1000))

# salt
js代码实现:  r + parseInt(10 * Math.random(), 10);
python实现:  ts + str(random.randint(0,9))

# sign（设置断点调试，来查看 e 的值，发现 e 为要翻译的单词）
js代码实现: n.md5("fanyideskweb" + e + salt + "n%A-rKaT5fb[Gy?;N5@Tj")
python实现:
from hashlib import md5
s = md5()
s.update("fanyideskweb" + e + salt + "n%A-rKaT5fb[Gy?;N5@Tj".encode())
sign = s.hexdigest()
```

**5、将Form表单数据处理为字典，通过requests.post()的data参数发送**



### 百度翻译破解案例

**目标：破解百度翻译接口，抓取翻译结果数据**

**实现步骤**

**1、F12抓包,找到json的地址,观察Form表单数据**

```python
1、POST地址: https://fanyi.baidu.com/v2transapi
2、Form表单数据（多次抓取在变的字段）
   from: zh
   to: en
   sign: 54706.276099  #这个是如何生成的？
   token: a927248ae7146c842bb4a94457ca35ee 
    # 基本固定,但不同浏览器不一样,想办法获取
```

**2、抓取相关JS文件**

```python
搜索sign - 找到具体JS文件(index_c8a141d.js) - 格式化输出
```

**3、在JS中寻找sign的生成代码**

```python
1、在格式化输出的JS代码中搜索: sign: 找到如下JS代码：sign: m(a),
2、通过设置断点，找到m(a)函数的位置，即生成sign的具体函数
   # 1. a 为要翻译的单词
   # 2. 鼠标移动到 m(a) 位置处，点击可进入具体m(a)函数代码块
```

**4、生成sign的m(a)函数具体代码备份**

```python
baidu_trans_tool.js
```

**5、利用pyexecjs模块执行js代码**

```python
1、安装pyexecjs
   sudo pip3 install pyexecjs
2、安装js执行环境:nodejs
   sudo apt-get install nodejs
# 执行js代码流程
import execjs
with open('baidu_trans_tool.js','r') as f:
    js_data = f.read()
execjs_obj = execjs.compile(js_data)
sign = execjs_obj.eval('e("tiger")')
```