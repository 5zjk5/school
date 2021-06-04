import csv
import pandas as pd
from tqdm import tqdm
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_csv():
    '''
    创建保存数据文件
    :return:
    '''
    with open('../data/professional.csv','w+',newline='',encoding='gbk') as f:
        wr = csv.writer(f)
        wr.writerow(['学校','专业类别','专业名称','国家特色专业'])


def get_school_url():
    '''
    读取学校，url
    :return: 学校及 url
    '''
    df = pd.read_csv('../data/school.csv',encoding='gbk')
    school = list(df['学校'])
    urls = list(df['开设专业链接'])
    s_u = list(zip(school,urls))
    return s_u


def get_html(url):
    '''
    获取网页源码
    :param url:
    :return:
    '''
    driver.get(url)
    html = driver.page_source
    return html


def get_info(html):
    '''
    提取数据
    :param html: 网页 html 源码
    :return: 提取后的数据
    '''
    # 解析提取标签(国家特色专业，专业)
    html = etree.HTML(html)
    lab = html.xpath('//div[@class="professional_content"]')

    # 判断是否有国家特色专业，有标签数据数为2，无标签数为1
    if len(lab) == 2:
        tese = lab[0].xpath('.//div[@class="major_item"]/p/text()')
        pro_lab = lab[1]
    else:
        tese = []
        pro_lab = lab[0]

    # 提取类别专业,专业名称
    pro = pro_lab.xpath('.//tr')[1:]
    info = []
    for p in pro:
        kind = p.xpath('./td[1]/text()')[0]
        names = p.xpath('./td[2]//div[@class="major_item"]/p/text()')
        for n in names:
            info.append([kind,n])

    # 判断是否为国家特色专业
    for i in info:
        if i[1] in tese:
            i.append('是')
        else:
            i.append('')

    return info


def write_to_csv(info):
    '''
    保存数据
    :param info: 专业数据
    :return:
    '''
    with open('../data/professional.csv','a+',newline='',encoding='gbk') as f:
        wr = csv.writer(f)
        wr.writerows(info)


if __name__ == '__main__':
    create_csv()
    school_url = get_school_url()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    pbar = tqdm(school_url)
    for s_u in pbar:
        html = get_html(s_u[1])
        info = get_info(html)
        [i.insert(0,s_u[0]) for i in info]
        write_to_csv(info)
