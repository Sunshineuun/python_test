from pathlib import Path
from utils.oracle import OralceCursor

import xlsxwriter


class WriteXLSXCustom(object):
    def __init__(self, path):
        """
        1. 检查后缀，如果后缀不是[.xlsx]结束，增加后缀
        2. 检查出去文件名称之外，目录是否存在，如果不存在按照路径进行创建。根路径[C:]
        3.
        :param path:
        """
        if not str(path).endswith('.xlsx'):
            path += '.xlsx'

        dir = Path('C:/')
        for p in path.split('\\'):
            dir /= p
            if not dir.exists() \
                    and p.find('.') == -1 \
                    and path:
                dir.mkdir()

        self.path = str(dir)
        self.workbook = xlsxwriter.Workbook(self.path)  # 建立文件
        self.format = self.get_format()
        # 建立sheet， 可以work.add_worksheet('employee')来指定sheet名，但中文名会报UnicodeDecodeErro的错误
        self.sheet = self.workbook.add_worksheet()
        # 冻结
        self.sheet.freeze_panes(row=1, col=0)

        # 列宽
        self.sheet.set_column('A:Z', 23)

    def write_title(self, rowindex, _data):
        """

        :param rowindex:
        :param _data:
        :return:
        """
        self.sheet.write_row(rowindex, 0, _data, self.format)

    def write(self, rowindex, _data):
        """
        :param rowindex: 行号
        :param _data: 一行数据
        :return: 无返回值
        """
        # self.sheet.set_column(firstcol=0, lastcol=100000, width=25)
        # self.sheet.set_row(rowindex, 15)
        index = rowindex
        for d in _data:
            self.sheet.write_row(index, 0, list(d), self.format)
            index += 1

    def get_format(self):
        """
        https://xlsxwriter.readthedocs.io/format.html#format
        :return:
        """
        _format = self.workbook.add_format()
        _format.set_align('left')
        _format.set_align('top')  # 对齐方式
        # _format.set_text_wrap()  # 自动换行
        return _format

    def close(self):
        self.workbook.close()
