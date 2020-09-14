# -*- coding: UTF-8 -*-
import os
import traceback

import cx_Oracle
from utils import mlogger

logger = mlogger.mlog
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
os.environ['path'] = 'D:\Downloads\devsoft\oracle\instantclient_11_2'
ORACLE_INFO = 'KBMS/KBMSwfm@192.168.3.99:1521/orcl'


class OralceCursor(object):
    def __init__(self, oracle_info=None):
        """
        :param oracle_info: 格式如下：{user}/{pd}@{ip}/{sid}
        """
        if not oracle_info:
            oracle_info = ORACLE_INFO

        self.cursor = cx_Oracle.connect(oracle_info, encoding='utf-8')
        self.oracle_cursor = self.cursor.cursor()
        if self.fech_all('SELECT 1 FROM dual')[0][0] != 1:
            raise Exception('Database connection failed')
        logger.info('The database connection was successful. {}'.format(oracle_info))

    def execute_sql_params(self, sql, params):
        try:
            temp = []
            if type(params[0]) == list:
                temp = params
            else:
                temp.append(params)

            count = self.oracle_cursor.executemany(sql, temp)
            self.cursor.commit()
            return count
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            self.cursor.rollback()
            return 0

    def execute_sql(self, sql):
        try:
            count = self.oracle_cursor.execute(sql)
            self.cursor.commit()
            return count
        except Exception as e:
            logger.error(e)
            self.cursor.rollback()
            return 0

    def fech_all(self, sql, params=None):
        if params is None:
            self.oracle_cursor.execute(sql)
        else:
            self.oracle_cursor.execute(sql, params)
        data = self.oracle_cursor.fetchall()
        return data

    def insert_sql(self, sql):
        try:
            count = self.oracle_cursor.execute(sql)
            self.cursor.commit()
            return count
        except Exception as e:
            logger.error(e)
            self.cursor.rollback()
            return 0

    def description(self):
        return self.oracle_cursor.description

    def get_column_name(self):
        des = self.description()
        name = []
        for d in des:
            name.append(d[0])
        return name

if __name__ == '__main__':
    """
        任务调度
    """
    cursor = OralceCursor()
