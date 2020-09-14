from utils.excel_utils import WriteXLSXCustom
from utils.oracle import OralceCursor

oracle_info = ""


def oracle_export(sql, file_path):
    """
    将SQL的查询结果导出到指定文件中去
    :param sql: oracle的查询脚本
    :param file_path: 目标文件的绝对路径
    :return:
    """
    cursor = OralceCursor(oracle_info=oracle_info)
    data = cursor.fech_all(sql)  # 执行sql语句

    xlsx = WriteXLSXCustom(file_path)
    xlsx.write_title(0, cursor.get_column_name())
    xlsx.write(1, data)
    xlsx.close()
