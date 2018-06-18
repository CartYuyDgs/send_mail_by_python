

import requests
import re
from lxml import etree

'''
@Get_url类用来爬取网页数据，
@author:yuy
@data: 2018-6-18
@返回：以列表的形式返回，
@参数：需要爬取的url

'''
class Get_url():
    def __init__(self,url):
        self.response = requests.get(url)
        self.html = etree.HTML(self.response.text)
    '''
    @获取凤凰资讯的信息
    '''
    def getFhUrlInfo(self):
        texts = []
        if self.response.status_code == 200:
            self.response.encoding = self.get_UrlCoding(self.response)
            fh_divs = self.html.xpath('//div[@class="box01"]/div[not(@class="next")]')
            for div in fh_divs:
                text = div.xpath(".//a[@class='t_css']/text()")[0]
                text_url = div.xpath('.//a[@class="t_css"]/@href')[0]
                texts.append(text)
                texts.append(text_url)
            return texts
    '''
    @设置爬取到的信息格式
    '''
    def get_UrlCoding(self,data):
        charset = 'utf-8'
        if data.encoding.lower() == 'utf-8' or data.encoding == 'utf8':
            return 'utf-8'
        if data.encoding.lower() == 'gb2312':
            return 'gb2312'
        if data.encoding.lower() == 'gbk':
            return 'gbk'
        if data.encoding.lower() == 'gb18030':
            return 'GB18030'
        m = re.compile('<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?', re.I).search(data.text)
        if m and m.lastindex == 2:
            charset = m.group(2).lower()
        return charset

    '''
    @获取python资讯信息
    '''
    def getPythonNew(self):
        texts = []

        python_li = self.html.xpath('//div[@class="news-hot"]/ul/li')
        for li in python_li:
            text_con = li.xpath('.//a/text()')[0]
            url = li.xpath('.//a/@href')[0]

            texts.append(text_con)
            texts.append(url)
        return texts
    '''
    @python 基础，高级，框架教程
    '''
    def getBaseUrlInfo(self):
        texts = []
        title_strs = self.html.xpath('//div[contains(@class,"cat-area")]')
        for index,title_str in enumerate(title_strs):
            if index <= 2:
                header = title_str.xpath('.//h5[@class="box-head"]/a/text()')[0]
                first_content = title_str.xpath('.//div[@class="content"]/p//a/text()')[0]
                first_content_url = title_str.xpath('.//div[@class="content"]/p//a/@href')[0]
                texts.append("\n@@****************************\n")
                texts.append(header)
                texts.append(first_content)
                texts.append(first_content_url)
                other_content_lis = title_str.xpath('.//div[@class="content"]/ul/li')
                for other_content_li in other_content_lis:
                    content_text = other_content_li.xpath('./a/text()')[0]
                    context_url = other_content_li.xpath('./a/@href')[0]
                    texts.append(content_text)
                    texts.append(context_url)

            else:
                continue
        return texts

'''
@调试main函数
'''
def main():
    url = "http://www.pythontab.com/"
    url_fh = "http://tech.ifeng.com/listpage/6899/1/list.shtml"
    #get_url = Get_url(url_fh)
    get_url = Get_url(url)
    #resp = get_url.getPythonNew()
    resp = get_url.getBaseUrlInfo()
    print(resp)

if __name__ == '__main__':
    main()