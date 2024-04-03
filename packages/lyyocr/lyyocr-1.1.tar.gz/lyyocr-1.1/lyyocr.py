import MyTT
import numpy as np
import time
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from tqdm import tqdm
from MyTT import *


i=0
pbar=tqdm(total=100)
# 计算filter_str的值
# 计算filter_str的值

def pd_calculate_filter(group, filter_condition_dict, local_dict_str=None):
    local_dict = eval(local_dict_str) 
    result_column ,filter_str= list(filter_condition_dict.items())[0]
    try:
        # 使用 pd.eval 计算表达式的值
        #result = eval(filter_str.upper(), {'__builtins__': None}, local_dict)
        result = pd.eval(filter_str.upper(), local_dict= local_dict)
        group[result_column] = result
    except Exception as e:
        print(f"Error evaluating filter_str: {e}")
        group[result_column] = np.nan

    # 更新进度条
    global i, pbar
    i += 1
    if i % 53 == 0:
        pbar.update(1)
        if i > 5300:
            pbar.close()
    return group[group[result_column]==True]



def calculate_filter(group, filter_condition_dict,local_dict_str=None):
    local_dict = eval(local_dict_str) 
    # 使用局部变量字典计算表达式的值
    result_column ,filter_str= list(filter_condition_dict.items())[0]

    try:
        print("filter_str=", filter_str,"")
        # 将表达式转换为大写可能会导致变量名不匹配，因此我们保持原样
        result = eval(filter_str.upper(), {'__builtins__': None}, local_dict)
        group[result_column] = result
    except Exception as e:
        print(f"Error evaluating filter_str: {e}")
        group['filter_value'] = np.nan

    # 更新进度条
    global i, pbar
    i += 1
    if i % 53 == 0:
        pbar.update(1)
        if i > 5300:
            pbar.close()
    return group[group[result_column]==True]


# 计算加权平均值
def calculate_weighted_average(df, value_columns:list, weight_column:str):
    """ 计算加权平均值
    :param df: 包含数据的DataFrame
    
    return: 返回一个字典，包含每个列的加权平均值
    """
    weighted_averages = {}
    total_weight = df[weight_column].sum()
    
    if total_weight > 0:
        for column in value_columns:
            weighted_averages[column] = (df[column] * df[weight_column]).sum() / total_weight
    else:
        for column in value_columns:
            weighted_averages[column] = np.nan
    
    return weighted_averages



def get_last_true_row(group,  filter_value_column="filter_value"):
    """
    找到dataframe中每个分组的最后一天filter_value为True的行

    """
    last_day = group['day'].max()
    last_true_row = group[(group['day'] == last_day) & (group[filter_value_column])]
    return last_true_row.iloc[-1:] if not last_true_row.empty else pd.DataFrame()

def select_stocks(df, formula_text, result_queue=None,use_tqdm=True, debug=False)->list[dict]:
    """选股公式

    Args:
        df (_type_): pd.dataframe
        formula_text (_type_): str, like "c>o"
        result_queue (_type_): queue to store result
        use_tqdm (bool, optional): _description_. Defaults to True.
        debug (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: 选中的股票列表
    """
    grouped = df.groupby("code")  if not isinstance(df, pd.core.groupby.DataFrameGroupBy) else df
    iterator = tqdm(grouped, total=len(grouped), desc="Processing stocks") if use_tqdm else grouped
    selected_stocks = []
    for i, (code, group) in enumerate(iterator, start=1):
        # 将 DataFrame 中的列赋值给本地变量
        c=C = close = CLOSE = group["close"].values
        l=L = low= LOW = group["low"].values
        h=H = high=HIGH = group["high"].values
        o=O = open = OPEN = group["open"].values
        v=V = vol=VOL = group["volume"].values
        cg = chonggao =CG = group["chonggao"].values

        # 解析选股语句并计算
        try:
            BUY = eval(formula_text.upper())
            if BUY[-1]:  # 如果最后一个值为 True，则选中该股票
                stock_info = {"code": code, "date": group["dayint"].max(), "condition": formula_text}  # 假设有一个名为 lyystk 的对象，其中包含 code_name_dict 字典  # 假设 group 的索引是日期
                selected_stocks.append(stock_info)
                if result_queue is not None: result_queue.put(stock_info)
                
        except Exception as e:
            print(f"Error evaluating formula for stock {code}: {e}")
        if use_tqdm:
            iterator.set_description(f"Processing stock {code}")

    if use_tqdm:
        iterator.close()
    if debug: print("选出的股票信息：", selected_stocks)

    return selected_stocks





def filter_dataframe(dfall, conditions):
    # 添加条件表达式，用df.query来筛选，返回符合条件的行
    condition_str = " & ".join(conditions)
    print("condition_str=", condition_str)
    df_filtered = dfall.query(condition_str)

    return df_filtered


def cala_curve_fit(data=None):
    # 用最小二乘法确定方程的系列。
    # 数据点列表（排除inf值）
    data = np.array([(2, 10), (5, 8), (10, 6), (20, 2), (30, 0), (50, -0.9)])

    # 定义模型函数
    def func(x, a, b):
        return a * x + b

    # 使用curve_fit进行拟合
    popt, pcov = curve_fit(func, data[:, 0], data[:, 1])

    # 输出结果
    print('最佳拟合参数: a =', popt[0], ', b =', popt[1])

    # 绘制结果
    plt.scatter(data[:, 0], data[:, 1], color='black')
    plt.plot(data[:, 0], func(data[:, 0], *popt), color='red')
    plt.show()


def calc_score():
    # x值和y值
    x = np.array([2, 5, 10, 20, 30])
    y = np.array([10, 8, 6, 2, 1])

    # 使用numpy的polyfit函数进行最小二乘拟合
    coefficients = np.polyfit(x, y, 1)
    print(coefficients)
    return coefficients


def calc_value_by_price(x):
    #价值计算1，股价
    return -0.32 * x + 9.7

    # 测试
    print(calc_value_price(10))  # 输出: 5.342105263157895

def calc_value_by_chonggao(x):
    #冲高的计算：
    #昨日量，昨日量在最近5天名次，昨日冲高，昨日高位持续次数，昨日尾盘打压
    
    return (x)


def calc_value_by_market_value(x):

    pass


def score_by_price(df):
    pass


if __name__ == "__main__":
    n = 3
    r = calc_value_price(4)

    print("result = ", r)
    """
    成功：选股测试
    """
    filter_txt = "v/MA(v,5)> 2"
    #selected_stock = lyyformula.select_stocks(df, filter_txt)
    #print(selected_stock)