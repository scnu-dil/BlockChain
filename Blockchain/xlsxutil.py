import xlrd
import json

def read_xlsx(filename):
    # 打开excel文件
    data1 = xlrd.open_workbook(filename)
    # 读取第一个工作表
    table = data1.sheets()[0]
    # 统计行数
    n_rows = table.nrows
    data = []
    # 属性：班级、学号、姓名
    for v in range(1, n_rows - 1):
        # 每一行数据形成一个列表
        values = table.row_values(v)
        # 列表形成字典
        data.append({'class_name': values[0],
                     'user_id': values[1],
                     'user_name': values[2],
                     })
    # 返回所有数据
    return data


if __name__ == '__main__':
    d = []
    # # 循环打开每个excel
    # for i in range(1, 16):
    #     d1 = read_xlsx('./excel data/' + str(i) + '.xlsx')
    #     d.extend(d1)
    d1 = read_xlsx('user.xlsx')
    d.extend(d1)
    # 写入json文件
    with open('user.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(d, ensure_ascii=False, indent=2))

    # name = []
    # # 微信id写文件
    # f1 = open('wechat_id.txt', 'w')
    # for i in d:
    #     if i['wechat_id'] not in name:
    #         name.append(i['wechat_id'])
    #     f1.writelines(i['wechat_id'])
    #     f1.writelines('\n')

    # print(len(name))
