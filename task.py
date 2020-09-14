import json
import re

from utils.common import oracle_export


def export_b216():
    """
    协助周依导出B216的数据
    :return:
    """
    sql = """
            SELECT ITEM_NAME        项目名称,
                   ID               规则代码,
                   ITEM_CODE        项目代码,
                   ITEM_CONNOTATION 项目内涵,
                   EXCEPT_CONTENT   除外内容,
                   UNIT             单位,
                   DSC              说明
            FROM KBMS_VFLC_ITEMS_GJYBJ
            ORDER BY ITEM_CODE
            """
    file_path = 'D:/Temp/temp.xlsx'
    oracle_export(sql, file_path)


def change_file_data():
    """
    药品说明书-人群用药2.sql;药品说明书辅助信息.sql;
     脚本替换特殊字符转换
    ID=3355（2544 2485） 的数据，因为某个字段的值过长，所以导指插入时，报字段过长
    :return:
    """
    """
    药品说明书-人群用药2.sql
    start_width = 'INSERT INTO MY_TABLE (ID, WOMAN_MEDICINE, CHILDREN_MEDICINE, ELDERLY_MEDICINE) VALUES '
    s[86:]
    """
    """
    药品说明书辅助信息.sql;
    start_width = 'INSERT INTO MY_TABLE(ID, MEDICINE_BELLYFUL, PHARMACOLOGY_POISONS, MEDICINE_DYNAMICS, QUALITY, STORE, PACKING, VALID_PERIOD, EXECUTE_STANDARD) VALUES '
    """
    base_file_path = 'C:\\Users\\qiushengming\\IdeaProjects\\KBMS\\tkdbup\\药品\\'
    start_width = 'INSERT INTO MY_TABLE(ID, WOMAN_MEDICINE, CHILDREN_MEDICINE, ELDERLY_MEDICINE) VALUES '
    writ_file_path = base_file_path + '药品说明书-人群用药2.sql'
    writ_file_path_big_data = base_file_path + '药品说明书辅助信息_big.sql'
    read_file_path = base_file_path + '药品说明书-人群用药.sql'
    content = read_file(read_file_path)
    new_line = ''
    new_lines = []
    new_lines_big = []
    index = 0
    dic = {
        '2000': 0,
        '1500': 0,
        '1000': 0,
        '500': 0,
        '1': 0
    }
    for c in content:
        if c.startswith('INSERT INTO') \
                or c.startswith('insert into'):
            index += 1
            new_line = start_width + replace_special_characters_to_blank(new_line[len(start_width):])

            new_lime_len = len(new_line)
            if new_lime_len > 2000:
                dic['2000'] += 1
                # print('--', index, new_lime_len)
                # new_lines_big.append(new_line)
                # new_line = new_line[:new_line.index(",'")] + ",'','','','','','','','');\n"
            elif 1500 < new_lime_len < 1999:
                dic['1500'] += 1
            elif 1000 < new_lime_len < 1499:
                dic['1000'] += 1
            elif 500 < new_lime_len < 999:
                dic['500'] += 1
            elif 0 < new_lime_len < 499:
                dic['500'] += 1

            new_lines.append(new_line)
            new_line = ''
            new_line += c
        else:
            new_line += c
    new_lines.append('--分界线-------------------------------')
    writ_file(writ_file_path, new_lines)
    # writ_file(writ_file_path_big_data, new_lines_big)
    print(dic)


def count_comma():
    file_path = 'C:\\Users\\qiushengming\\IdeaProjects\\KBMS\\tkdb\\药品\\药品说明书-人群用药2.sql'
    content = read_file(file_path)
    index = 0
    for c in content:
        index += 1
        num = c.count(',')
        if num != 6:
            print(c)


def read_file(filepath):
    content = []
    with open(filepath, encoding='UTF-8') as fp:
        content = fp.readlines()
    return content


def writ_file(filepath, _data):
    if list != type(_data):
        return

    with open(filepath, 'w', encoding='utf-8') as fp:
        fp.writelines(_data)


def replace_special_characters_to_blank(_s):
    """
    将文本中的换行符号提出，但是结尾加一个换行符
    331082200410144487

    :param _s:
    :return:
    """
    pattern1 = re.compile(r'null')
    out = re.sub(pattern1, "''", _s)
    pattern2 = re.compile(r'([\n ])')
    out = re.sub(pattern2, '', out)
    pattern = re.compile(r'<[0-9a-zA-Z/=", \-;.#:()\[\]&_!%*\'宋体仿等线微软雅黑点击放大]+>')
    out = re.sub(pattern, '', out)
    if len(out) < 10:
        return ''

    return out + '\n'


if __name__ == '__main__':
    config = {
        'curstart': '1',
        'index': '1',
        'isRequestEnd': '1',
        'response_status_code': '200'
    }
    s = json.dumps(config)
    print(s)
    pass
