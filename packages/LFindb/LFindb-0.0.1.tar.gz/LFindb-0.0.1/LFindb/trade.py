# -*- coding:utf-8 -*- 
import pandas as pd

from .mysql_db import Mysqldb
from .config import CONFIG

def get_hist_price(*, symbol='', start_date='', end_date='', adjust='qfq', fields='*'):
    db = Mysqldb(user_demo = CONFIG['USER'], password_demo = CONFIG['PASSWORD'], 
                 host_demo = CONFIG['HOST'], database_demo = CONFIG['DATABASE'])
    tablename = 'histprice_demo'
    if adjust != 'qfq':
        print("目前只提供前复权价格")
        return
    if symbol == None:
        print("重新输入查询代码")
        return
    if fields == "*":
        sql_native = f"select * from {tablename}" 
    else:
        if isinstance(fields, list):
            fields_new = ','.join(fields)
            sql_native = "select %s from %s" % (fields_new, tablename)
    if start_date:
        sql_date_start = "date > '%s'" % start_date
    else:
        sql_date_start = "date > '1990-01-01'"
    if end_date:
        sql_date_end = "date < '%s'" % end_date
    else:
        sql_date_end = "date < '2050-01-01'"
    if symbol == None:
        sql = sql_native + ' where ' + sql_date_start + ' and ' + sql_date_end
    else:
        if isinstance(symbol, list):
            sql_symbol = "( symbol = "
            for i in range(len(symbol)):
                if i+1 == len(symbol):
                    sql_symbol = sql_symbol + "'%s' )" % symbol[i]
                    break
                sql_symbol = sql_symbol + "'%s' or symbol = " % symbol[i]
            
        else:
            sql_symbol = "symbol = %s" % symbol
    
    sql = sql_native + ' where ' + sql_date_start + ' and ' + sql_date_end + ' and ' + sql_symbol + ';'
    data_list = db.query(sql)
    db.close()
    data_df = pd.DataFrame(data_list)
    if fields == "*":
        data_df.columns = ['date', 'open', 'high', 'low', 'close', 'symbol', '_']
        data_df.drop(['_'], axis=1, inplace=True)
    else:
        data_df.columns = fields
    return data_df


def get_hist_price_close(*, symbol='', start_date='', end_date='', adjust='qfq'):
    config = {
        'symbol': symbol,
        'start_date': start_date,
        'end_date': end_date,
        'fields': ['date', 'close', 'symbol']
    }
    data_return = get_hist_price(**config) 
    data_return = data_return.pivot(index=["date"], columns=['symbol'], values=['close'])
    return data_return['close']