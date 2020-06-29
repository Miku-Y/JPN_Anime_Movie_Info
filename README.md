# JPN_Anime_Movie_Info
使用Python爬虫获取时光网日本动画电影TOP100信息并保存为Json文件

## 一.主题选择

使用python相关技术实现对某个网站的网页（自选）进行爬取，获得感兴趣的关键数据，并存储在json文件中。

## 二.相关技术流程

> 1.发起请求

> 2.获取响应内容

> 3.解析内容

> 4.保存数据

![R4bS.png](https://img.auxiz.com/R4bS.png)

## 三.反爬虫措施

本爬虫代码爬取的是时光网（<http://movie.mtime.com/list/1709.html>）的日本动画电影TOP100的部分电影信息。为了反爬虫，避免请求失败，requests.get()时需要添加headers（请求头参数）模拟成浏览器访问网站。

**Headers获取方法**（适用于Chrome浏览器）：

> 1.**打开榜单页面F12点击NetWork里的Doc选项--\>刷新页面--\>右键1709.html--\>copy--\>copy
as cURL**

> 2.打开<https://curl.trillworks.com/> 语法转换工具

> 3.粘贴已复制的cURL到左边输入框,直接转换成Python形式的请求

> 4.复制header={…}
 
## 四.分析网页

**1. 榜单一共有10页，除了第一页网址是\*/1709.html，后面9页的网址格式都是\*/1709-页数.html**

(第1页)

![RQdU.png](https://img.auxiz.com/RQdU.png)

(第2页)

![RfsD.png](https://img.auxiz.com/RfsD.png)

(第10页)

![RiLw.png](https://img.auxiz.com/RiLw.png)

**2. 每一个电影详细信息都有相应的页面，区别在于网址后面的电影ID**

![Rmru.png](https://img.auxiz.com/Rmru.png)

![Rt6q.png](https://img.auxiz.com/Rt6q.png)

**3. 按F12打开页面源码可以看到我们需要的电影导演、编剧、国家地区、发行公司信息都在\<dd
    class="__r_c_" pan="M14_Movie_Overview_BaseInfo"\>标签内**

>   **提示：抓取的页面的数据和浏览器看到的不一样！原因是很多网站中的数据都是通过js,ajax动态加载的，所以直接通过get请求获取的页面和浏览器显示的不同，可通过设置断点调试查看请求到的数据**

![Ry4d.png](https://img.auxiz.com/Ry4d.png)

**4. 完整电影名称在a标签内，不利于查找，可以选择查找它的父级\<div
    class="db_cover \__r_c_" pan="M14_Movie_Overview_Cover"\>**

![RAjA.png](https://img.auxiz.com/RAjA.png)

## 五.运行效果

![RBOe.gif](https://img.auxiz.com/RBOe.gif)

![Rb0Y.png](https://img.auxiz.com/Rb0Y.png)
