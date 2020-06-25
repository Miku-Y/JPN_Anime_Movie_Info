import requests
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm

"""
使用方法：
填写下面的header信息后运行即可
榜单页面：http://movie.mtime.com/list/1709.html
1.(Google Chrome)
  打开榜单页面F12点击NetWork里的Doc选项-->刷新页面-->右键1709.html-->copy-->copy as cURL
2.打开 https://curl.trillworks.com/ 网站工具
3.粘贴已复制的cURL到左边输入框,直接转换成Python形式的请求
4.复制header信息并粘贴下面到相应位置
ps：反爬虫，模拟成浏览器访问网站，避免请求失败
"""


def headers():
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    }
    return headers


# 获取Top100动漫的id
def get_ids():
    ids = []
    # 向网站发起请求，并获取响应对象
    response_one = requests.get('http://movie.mtime.com/list/1709.html',
                                headers=headers(), verify=False)
    # text属性获取响应内容（字符串）网站源码
    html_one = response_one.text
    # BeautifulSoup是用来从HTML或XML中提取数据的Python库。
    soup_one = BeautifulSoup(html_one, 'lxml')  # 选择lxml作为解析器
    # 筛选出html里面类名为“top_nlist”的div标签元素内容，返回list
    id_info = soup_one.select('div[class="top_nlist"]')  # # 这个属性所在的div标签内是电影排行信息
    # 设置匹配格式，()表示匹配后只保留括号的内容，\d+ 表示多个任意数字
    patt = r'<a href="http://movie.mtime.com/(\d+)/'
    # 正则表达式re.findall()方法能够以列表的形式返回能匹配的字符串
    # patt“需要匹配的字符串格式”  str(id_info)“在这个字符串中查找”  re.S“匹配包括换行在内的所有字符”
    id_one = re.findall(patt, str(id_info), re.S)
    # 将第一页排行榜的电影id存入ids列表
    for item in id_one:
        ids.append(item)

    for num in range(2, 11):
        # 总共10页数据，通过.format(num)替换{}为页数来实现榜单翻页，向网站发起请求
        response = requests.get('http://movie.mtime.com/list/1709-{}.html'.format(num),
                                headers=headers(), verify=False)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        id_info = soup.select('div[class="top_nlist"]')
        patt = r'<a href="http://movie.mtime.com/(\d+)/'
        id_one = re.findall(patt, str(id_info), re.S)
        for item in id_one:
            ids.append(item)
    print('Top100动漫的id已获取:')
    print(ids)
    # 将获取到的100个电影id列表返回
    return ids


# 获取动漫的导演和编剧等信息
def get_movie_info(id):
    # 通过.format(id)替换{}为id来实现向指定电影详细页面发起请求
    response = requests.get('http://movie.mtime.com/{}/'.format(id), headers=headers())
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    # 筛选出html里面有属性为pan="M14_Movie_Overview_BaseInfo"的dd标签元素内容，返回list
    info_name = soup.select('dd[pan="M14_Movie_Overview_BaseInfo"]')  # 这个属性所在的dd标签内是电影信息
    # 在info_name中查找，(.*?)遇到开始和结束就进行截取，只保留括号的内容
    info_names = re.findall(r'</strong>(.*?)</a>', str(info_name), re.S)
    data = []
    try:
        # 选择info_names列表的每条信息，用split()以指定字符进行切片，并选择最后一个切片，即需要的电影信息
        director = str(info_names[0]).split('target="_blank">')[-1]  # 导演
        playwriter = str(info_names[1]).split('target="_blank">')[-1]  # 编剧
        section = str(info_names[2]).split('target="_blank">')[-1]  # 发行地区
        company = str(info_names[3]).split('target="_blank">')[-1]  # 发行公司
        movie_info = soup.select('div[class="db_cover __r_c_"]')
        movie_name = re.findall(r'title="(.*?)">', str(movie_info), re.S)  # 提取电影名称
        # 将列表内的内容赋值给movie_title(相当于去除列表符号)
        movie_title = movie_name[0]
        # 将上面获取到的电影信息放入字典
        info = {
            '电影名': movie_title,
            '导演': director,
            '编剧': playwriter,
            '国家地区': section,
            '发行公司': company
        }
        data.append(info)
    except IndexError:
        pass
    return data


def write2json(lists):
    with open('./T100数据.json', 'w', encoding='utf-8') as f:
        # ensure_ascii=False 不使用用ASCII编码，防止中文乱码
        json.dump(lists, f, ensure_ascii=False)
    print("保存成功")


if __name__ == '__main__':
    ids = get_ids()
    list_all = []
    print('正在获取动漫详细信息...')
    # 在for循环体中用tqdm()包裹迭代器实现进度条效果
    for i in tqdm(ids):
        # 将获取到的每一条数据列表合并
        list_all.extend(get_movie_info(i))
    # 将数据列表转为Json格式存储
    write2json(list_all)
