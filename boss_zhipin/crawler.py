#!/usr/bin/env python3
# coding: utf-8

# version: 0.2

'''
目前问题：
    融资那里有的公司写了三项（公司类型、融资、规模），有的公司只写了其中两项或一项，考虑如何进行拆分？

更远的要求：
    改进代码：使用协程or多线程or多进程
'''


import requests
from lxml import etree
import sys
import io
import csv
import random

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


class Crawler(object):
    '''some static method to avoid baned by sites.
    '''
    def __init__(self, url, propxies):
        self.url = url
        self.propxies = propxies

    @staticmethod
    def user_agent():
        '''return random User-Agent.'''
        USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]
        return random.choice(USER_AGENTS)

    @staticmethod
    def propxy(propxies=None):
        '''return a propxy ip.'''
        if not propxies:
            propxies = self.propxies
        if isinstance(propxies, list):
            return random.choice(propxies)
        else:
            return propxies

    @staticmethod
    def get_html(url=None):
        '''return response as html for xpath to select elements.'''
        if not url:
            url = self.url
        headers = self.user_agent()
        res = requests.get(url, headers=headers)
        html = etree.HTML(res.content)
        return html



def get_page_url():
    '''generate job pages for bioinformatics engineer.'''
    page = 1
    while True:
        url = "https://www.zhipin.com/job_detail/?query=生物信息分析&scity=100010000&industry={page}&position={page}".format(page=page)
        yield url
        page += 1


def get_res(url):
    '''return the etree.HTML(...) for xpath to extract elements'''
    headers = {'User-Agent': user_agent}
    # get all job pages for bioinformatics
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise SystemExit("Connection/HTTP Error: "+str(res.status_code))
    html = etree.HTML(res.content)
    return html


def job_skills(comp_url):
    '''get the skills requested by the job, such as perl, python, linux...
       then representing these skills with binary code 1,2,4...
       linux=1, perl=2, python=4, R=8, C++=16, C=32, matlab=64
    '''
    skills_code = {'linux': 1, 'Linux': 1, 'perl': 2, 'Perl': 2, 'python': 4, 'Python': 4,
                   'R': 8, 'C++': 16, 'c++': 16, 'C': 32, 'c': 32, 'matlab': 64, 'Matlab': 64,
                   'mysql': 128, 'Mysql': 128, 'Docker': 256, 'docker': 256}
    skills = []
    for url_ in comp_url:
        code = 0
        html = get_res(url_)
        job_description = html.xpath('//div[@class="job-detail"]/div[@class="detail-content"]/div[@class="job-sec"]/div[@class="text"]/text()')
        content = "".join(job_description)
        for skill in skills_code:
            if skill in content:
                code += skills_code[skill]
        skills.append(code)
    return skills


def parse_html():
    '''parse each page html to get detail content about every job.'''
    page_list = get_page_url()
    for page in page_list:
        html = get_res(page)
        # 职位名称
        job_name = html.xpath('//div[@class="job-title"]/text()')
        # 月薪
        salary = html.xpath('//span[@class="red"]/text()')
        # 公司名称
        company = html.xpath('//div[@class="info-company"]/div[@class="company-text"]/h3[@class="name"]/a/text()')
        # 工作点的(城市)、工作经验、学历
        al = html.xpath('//div[@class="job-primary"]/div[@class="info-primary"]/p/text()')
        company_address = [al[i].split()[0] for i in range(0, len(al), 3)]
        experience = [al[i] for i in range(1, len(al), 3)]
        degree = [al[i] for i in range(2, len(al), 3)]
        # 公司类型、融资、规模（有的公司未填写融资情况，故不好拆分）
        finance = html.xpath('//div[@class="info-company"]/div[@class="company-text"]/p/text()')
        # # 公司类型
        # company_type = [_finance[i] for i in range(0, len(_finance), 3)]
        # # 融资情况
        # finance = [_finance[i] for i in range(1, len(_finance), 3)]
        # # 公司规模
        # scale = [_finance[i] for i in range(2, len(_finance), 3)]
        ############################################################
        # homepage url of company
        c_url = html.xpath('//div[@class="job-primary"]/div[@class="info-primary"]/h3[@class="name"]/a/@href')
        company_url = ["https://www.zhipin.com"+_ for _ in c_url]
        skills_request = job_skills(company_url)
        yield job_name, salary, company, company_address, experience, degree, finance, skills_request


def write_to_csv():
    column_names = ['job_name', 'salary', 'company', 'company_address', 'experience', 'degree', 'finance', 'skills_request']
    # column_names = ['工作名称', '月薪', '公司', '公司地址', '工作经验', '学历', '融资情况', '职位技能要求']
    with open(r"C:\Users\sxuan\Desktop\boss_zhipin.csv", 'wt', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(column_names)
        job_detail = parse_html()
        for record in job_detail:
            f_csv.writerow(record)


# url = "https://www.zhipin.com/job_detail/?query=生物信息分析&scity=100010000&industry=1&position=1"
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
# res = requests.get(url, headers=headers)
# html = etree.HTML(res.content)

write_to_csv()
