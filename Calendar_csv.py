import requests
import json
import csv
import datetime

# 定义一个列表变量存放所有数据
shtData = []

def go(y, m):
    url = f"https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query={str(y)}年{str(m)}月&co=&resource_id=39043&t=1601954930239&ie=utf8&oe=gbk&format=json&tn=wisetpl&_=1601950837128"
    response = json.loads(requests.request("GET", url).text)
    for i in response['data'][0]['almanac']:
        # 因为每次请求 api 会返回当月以及前后两个月的信息，所以判断月份是查询月则继续
        if i['month'] == str(m):
            # 按照 term > desc > value 的优先级，依次判断是否有值及是否长度超过了4，根据优先级显示
            if i['term'] and len(i['term']) <= 4:
                day_yl = i['term']
            else:
                if 'desc' in i.keys() and i['desc'] and len(i['desc']) <= 4:
                    day_yl = i['desc']
                else:
                    if 'value' in i.keys() and i['value'] and len(
                            i['value']) <= 4:
                        day_yl = i['value']
                    else:
                        if i['lDate'] == '初一':
                            # 若判断是十一月与十二月，则分别显示冬月与腊月
                            if i['lMonth'] == '十一':
                                day_yl = '冬月'
                            elif i['lMonth'] == '十二':
                                day_yl = '腊月'
                            else:
                                # 非十一月与十二月，则显示当前阴历月份
                                day_yl = i['lMonth'] + '月'
                        else:
                            # 如果这天不是初一，则正常显示当天阴历
                            day_yl = i['lDate']

            # 如果月份是个位数，则前边补 0 ，这样方便直接粘贴在表格中不会错位
            month = '0' + i['month'] if len(i['month']) == 1 else i['month']
            # 如果日为个位数，则补 0 ，目的同上
            day = ('0' + i['day']) if len(i['day']) == 1 else i['day']
            # 存入数据至全局变量
            shtData.append([i['year'], month + '\t', day + '\t', day_yl])


def goRange(y1, m1, y2, m2):
    for y in range(y1, y2 + 1):
        if y1 == y2 and m2 < m1:
            print('日期错误！')
        else:
            allRange = range(m1, m2 + 1) if y1 == y2 else range(
                m1, 13) if y == y1 else range(1, m2 +
                                              1) if y == y2 else range(1, 13)
            for m in allRange:
                go(y, m)


if __name__ == "__main__":
    y1 = int(input('请输入起始年份 (如 2021)：'))
    m1 = int(input('请输入起始月份 (如 9)：'))
    y2 = int(input('请输入结束年份 (如 2022)：'))
    m2 = int(input('请输入结束月份 (如 12)：'))

    goRange(y1, m1, y2, m2)

    with open(datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv',
              'w') as f:
        #创建csv文件的写入对象
        writer = csv.writer(f)
        #写一行,格式:['第1个单元格数据', '第2个单元格数据']
        writer.writerow(['年', '月', '日', '节日/阴历'])
        #写入多行
        #格式：[(第1行数据), (第2行数据), (第3行数据)]
        #备注:可以用元祖包裹一行，也可以用列表包裹一行
        writer.writerows(shtData)
