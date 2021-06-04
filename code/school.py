import requests
import json
import csv
import time
from tqdm import tqdm


def create_csv():
    '''
    创建保存数据的文件
    :return:
    '''
    with open('../data/school.csv','w+',encoding='gbk',newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['学校','省份','城市','地址','水平层次','办学类别','办学类型','985',
                     '211','双一流','归属','开设专业链接'])


def get_json(url):
    '''
    请求获得 json
    :param url: 页数链接
    :return: 学校信息列表
    '''
    headers = {
        'Host': 'api.eol.cn',
        'Origin': 'https://gkcx.eol.cn',
        'Referer': 'https://gkcx.eol.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    json_txt = json.loads(response.text)
    items = json_txt['data']['item']
    return items


def get_info(items):
    '''
    提取数据
    :param items: 学校信息列表
    :return: 提取后的所有数据
    '''
    info = []
    for item in items:
        # 学校
        name = item.get('name','')
        # 省份
        province_name =item.get('province_name','')
        # 城市
        city_name = item.get('city_name', '')
        # 地址
        address = item.get('address', '')
        # 水平层次
        level_name = item.get('level_name', '')
        # 办学类别
        type_name = item.get('type_name', '')
        # 办学类型
        nature_name = item.get('nature_name', '')
        # 985
        f985 = item.get('f985', '')
        f985 = map_dict('f985',f985)
        # 211
        f211 = item.get('f211', '')
        f211 = map_dict('f211', f211)
        # 双一流
        dual_class_name = item.get('dual_class_name', '')
        # 归属
        belong = item.get('belong', '')
        # id，构造学校开设专业详情链接
        school_id = item.get('school_id', '')
        professional_url = 'https://gkcx.eol.cn/school/{}/professional'.format(str(school_id))

        info.append([name,province_name,city_name,address,level_name,type_name,
                     nature_name,f985,f211,dual_class_name,belong,professional_url])

    return info


def map_dict(k,v):
    '''
    映射对应的值
    :param k: 字段
    :param v: 提取得到的值
    :return: 正确的值
    '''
    if k == 'f985':
        if v == 1:
            return '是'
        else:
            return '否'
    if k == 'f211':
        if v == 1:
            return '是'
        else:
            return '否'


def write_to_csv(info):
    '''
    写入数据
    :param info: 学校数据
    :return:
    '''
    with open('../data/school.csv','a+',encoding='gbk',newline='') as f:
        wr = csv.writer(f)
        wr.writerows(info)


if __name__ == '__main__':
    urls = ['https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=&f985=&is_doublehigh=&is_dual_class=&keyword=&nature=&page={}&province_id=&ranktype=&request_type=1&school_type=&signsafe=&size=20&sort=view_total&top_school_id=[2858]&type=&uri=apidata/api/gk/school/lists'
            .format(str(i)) for i in range(1,144)]
    create_csv()
    pbar = tqdm(urls)
    for url in pbar:
        items = get_json(url)
        info = get_info(items)
        write_to_csv(info)
        time.sleep(1)

