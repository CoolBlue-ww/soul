import requests
from lxml import etree

# 目录的网页网址
URL = 'https://www.hongxiu.com/book/22211356000824002#Catalog'

"""
建立一个函数，
用来获取每一章节的超链接
"""


def get_link():
    source_code = requests.get(URL).text  # 获取网页源代码
    html = etree.HTML(source_code)  # 解析HTML代码
    links = html.xpath('//div[@class="volume"]/ul[@class="cf"]/li/a')
    return links


# 建立一个函数用来下载每一章节
def download(links):
    body_url = 'https://www.hongxiu.com/{}'.format(links)
    code = requests.get(body_url).text
    data = etree.HTML(code)
    title = data.xpath('//h1[@class="j_chapterName"]/text()')[0]
    p_list = data.xpath('//div[@class="ywskythunderfont"]/p')
    with open('小说three/%s.text' % title, 'wt', encoding='utf-8') as file:
        for p in p_list:
            content = p.xpath('./text()')[0]
            file.write(content + "\n")
    print("{}.text下载成功".format(title))


# 建立一个程序入口
def main():
    links = get_link()
    for l in links:
        href = l.xpath('./@href')[0]
        download(href)


if __name__ == '__main__':
    main()