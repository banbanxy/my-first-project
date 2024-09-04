import requests

# 功能一
def search():
    while True:
        keyword = input('请输入关键词：')
        params = {
           'keyWord': keyword,
            'maxNum': '10'
        }
        
        res = requests.post('http://www.cninfo.com.cn/new/information/topSearch/query',params = params)
        res_json = res.json()
        
        if not res_json:
            print('请重新输入关键词')
            continue
        
        data = []
        for row in res_json:
            if row['category'] == 'A股':
                data.append(row)
                
        dict = {}
        index = 1
        for row in data:
            print(f'''序号-{index} 股票名称-{row['zwjc']}''')
            dict[str(index)] = row
            index += 1
            
        while True:
            num = input('请输入序号：')
            if num in dict:
                return dict[num]
            else:
                print('请重新输入序号')
                continue

# 功能二
def select(code,orgID):
    category_dict = {
        '1': 'category_ndbg_szsh;',
        '2': 'category_bndbg_szsh;',
        '3': 'category_rcjy_szsh;'
    }

    while True:
        numbers = input('请输入搜索类型序号：1、年报 2、半年报 3、日常经营：（输入序号，如：1）')
        if numbers in category_dict:
            category = category_dict[numbers]
            break
        else:
            print('输入有误，请重新输入')

    start = input('请输入搜索范围起始时间（例如 2021-01-01）：')
    end = input('请输入搜索范围结束时间（例如 2021-07-01）：')

    if code[0] == '6':
        column = 'sse'
        plate = 'sh'
    else:
        column = 'szse'
        plate = 'sz'

    page_num = 1
    pdf_list = []

    while True:
        data = {
            'stock': f'{code},{orgID}',
            'tabName': 'fulltext',
            'pageSize': '30',
            'pageNum': str(page_num),
            'category': category,
            'seDate': f'{start}~{end}',
            'column': column,
            'plate': plate,
            'searchkey': '',
            'secid': '',
            'sortName': '',
            'sortType': '',
            'isHLtitle': ''
        }

        r = requests.post('http://www.cninfo.com.cn/new/hisAnnouncement/query', data=data)
        r_json = r.json()


        if not r_json['announcements']:
            print('无搜索结果！')
            break

        for i in r_json['announcements']:
            pdf_list.append([i['announcementTitle'], i['adjunctUrl']])

        # 结束循环条件
        if r_json.get('hasMore') == 'false':
            break

        page_num += 1

        return pdf_list

# 功能三
def download(list):
    for row in list:
        path = 'http://static.cninfo.com.cn/' + row[1]
        name = row[0] + '.pdf'
        res = requests.get(path)
        
        with open(f"D:/日常/code/风变编程/爬虫/生成结果/股票/{name}",'wb') as f:
            f.write(res.content)
            print(f'{name}已下载')

# 功能整合
def main():
    # 搜索股票，获取股票id信息等
    info = search()
    code = info['code']
    orgID = info['orgId']
    # 输入各个参数，筛选报告
    list = select(code,orgID)
    # 下载报告
    pdf = download(list)

main()
