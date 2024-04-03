import os
import sys

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 14
project_path = file_path[0:end]
sys.path.append(project_path)
from mns_common.db.MongodbUtil import MongodbUtil
import mns_common.constant.db_name_constant as db_name_constant
import mns_common.component.trade_date.trade_date_common_service_api as trade_date_common_service_api

mongodb_util = MongodbUtil('27017')
import pandas as pd
from io import StringIO
from functools import lru_cache


# 开盘啦概念操作类

# 获取单个股票所有概念数据
@lru_cache(maxsize=None)
def get_symbol_all_kpl_concept(symbol):
    query = {'symbol': symbol}
    return mongodb_util.find_query_data(db_name_constant.KPL_BEST_CHOOSE_INDEX_DETAIL, query)


# 获取有效同花顺概念代码
@lru_cache(maxsize=None)
def get_kpl_all_concept():
    query = {}
    kpl_best_choose_index = mongodb_util.find_query_data(db_name_constant.KPL_BEST_CHOOSE_INDEX, query)
    return kpl_best_choose_index


if __name__ == '__main__':
    df = get_kpl_all_concept()
    print(1)
