import requests
from bs4 import BeautifulSoup
import time as t
import pymysql

# 例子的url

def getm_insert():
    url = 'https://voice.hupu.com/nba'  # 虎扑nba新闻
    # 利用requests对象的get方法，对指定的url发起请求
    # 该方法会返回一个Response对象
    mystr_title = ''
    mystr_source = ''
    for k in range(1,10):
        res = requests.get(url+'/'+repr(k))
        # 通过Response对象的text方法获取网页的文本信息
        # print(res.text)

        soup = BeautifulSoup(res.text, 'lxml')

        # 找出class属性值为news-list的div
        news_list = soup.find('div', {'class': 'news-list'})
        # 找出news_list下的所有li标签
        news = news_list.find_all('li')
        news_id = []
        news_titles = []
        news_source = []
        news_time = []


        # 遍历news
        for j, i in enumerate(news):
            try:
                #提取新闻id
                raw_id = i.find('a', {'class': 'time'})['href'].strip()
                id = raw_id[raw_id.rfind('/')+1:len(raw_id)-5]
                # 提取新闻标题
                title = i.find('h4').get_text().strip()
                # 提取新闻来源
                source = i.find('span', {'class': 'comeFrom'}).find('a').get_text().strip()
                # 提取新闻时间
                time = i.find('a', {'class': 'time'})['title'].strip()
                # 存储爬取结果
                news_id.append(id)
                news_titles.append(title)
                news_source.append(source)
                mystr_source += source
                news_time.append(time)
                mystr_title += title
                sql = "REPLACE INTO data(id,title,source,time) VALUES (" + str(news_id[j]) + ", '"+news_titles[j]+"', '" + news_source[j]+"', '"+news_time[j]+"')"
                #print(sql)
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                except e:
                    # 如果发生错误则回滚
                    db.rollback()
                    print(e)
                    print(111)
                    print(sql)

                # print (i)
                print('新闻标号：', id)
                print('新闻标题：', title)
                print('新闻来源：', source)
                print('新闻时间：', time)

            except AttributeError as e:
                continue

    f = open('../ciyun/nba_news_title.txt', 'w')
    f.write(mystr_title)
    f.close()

    f = open('../ciyun/nba_news_source.txt', 'w')
    f.write(mystr_source)
    f.close()




if __name__ == '__main__':
    # 打开数据库连接
    db = pymysql.connect("10.96.99.60", "root", "", "hupu")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    while(1):
        getm_insert()
        t.sleep(60)
    db.close()

