# coding   : utf-8
# @Time    :11/17/20 12:58 PM
# @Author  :Xiaohan
# @FileName:datalogger.py
# @SoftWare:PyCharm

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import datetime
import matplotlib.dates as mdates
import matplotlib
from datetime import datetime as dt


def basic(file_name):
    df_raw = pd.read_csv(file_name)
    df = df_raw.drop(columns=['DevEUI','ClientID'])
    return df


def combine_outdoor(df_room,outdoor_file):
    """
    Add hourly outdoor temperature and humidity to room dataframe
    :param df_room:
    :param outdoor_file: got from worldweather.com API service
    :return: dataframe with outdoor temp/humidity added
    """
    df_outdoor_all = pd.read_csv(outdoor_file)
    # generate the time key(date-hour) for joining tables
    df_outdoor_all['time_key_r'] = df_outdoor_all.date_time.apply(lambda x: x[:10] + '-' + x[11:13])
    df_outdoor = df_outdoor_all[['time_key_r', 'humidity', 'tempC']]
    df_room['time_key'] = df_room.Timestmp.apply(lambda x: x[:10] + '-' + x[11:13])
    df_room = df_room[(df_room['humidity'] != 0) & (df_room['temperature'] != 0)]
    cmb = df_room.merge(df_outdoor, left_on='time_key', right_on='time_key_r', how='left')
    cmb = cmb.rename(columns={'humidity_x': 'humidity', 'humidity_y': 'outdoor_humidity', 'tempC': 'outdoor_temperature'})
    return cmb


def convert_to_date(ts):
    """
    Given timestamp, parse to get datatime format info
    :param ts:
    :return: e.g. 09/21/2020
    """
    d = dt.strptime(ts[:16], '%Y-%m-%dT%H:%M')
    d = d.strftime('%m/%d/%Y-T%I:%M %p')
    return d[:10]


def date_to_week(date):
    if date.month == 9 and 21 <= date.day <= 27:
        return '09/21 - 09/27'
    elif (date.month == 9 and date.day >= 28) or (date.month == 10 and date.day <= 4):
        return '09/28 - 10/04'
    elif date.month == 10 and 5 <= date.day <= 11:
        return '10/05 - 10/11'
    elif date.month == 10 and 12 <= date.day <= 18:
        return '10/12 - 10/18'
    elif date.month == 10 and 19 <= date.day <= 24:
        return '10/19 - 10/24'

def convert_to_week_day(date):
    week = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    # return '0Monday', '1Tuesday' ... so that the order is normal
    return str(date.weekday()) + week[date.weekday()]

def preprocess(df):
    """
    Make necessary conversions for time/temp/humid features
    :param df:
    :return:
    """
    df['date'] = pd.to_datetime(df['Timestmp'])
    df['hour'] = df.date.apply(lambda x: x.hour)
    df['week_num'] = df['date'].apply(lambda x: date_to_week(x))
    df['DayWeek'] = df['date'].apply(lambda x:convert_to_week_day(x))
    df['convert_date'] = df['Timestmp'].apply(lambda x: convert_to_date(x))
    df['temperature(F)'] = df['temperature'].apply(lambda x: x * (9/5) + 32)
    df['outdoor_temperature(F)'] = df['outdoor_temperature'].apply(lambda x: x * (9/5) + 32)
    df['temperature_delta'] = df['temperature(F)'] - df['outdoor_temperature(F)']
    df['humidity_delta'] = df['humidity'] - df['outdoor_humidity']
    return df


def df_ht_hourly(df,fea,gb,io):
    """
    Group dataframe by hour and week/date/day_week
    :param df:
    :param fea:
    :param gb:
    :param io:
    :return:
    """
    df = df[df['convert_date']!='09/21/2020']
    if gb == 'week':
        key_gb = 'week_num'
    elif gb == 'date':
        key_gb = 'convert_date'
    elif gb == 'day_week':
        key_gb = 'DayWeek'

    if fea == 't':
        if io == 'i':
            key_val = 'temperature(F)'
        elif io == 'o':
            key_val = 'outdoor_temperature(F)'
    elif fea == 'h':
        if io == 'i':
            key_val = 'humidity'
        elif io == 'o':
            key_val = 'outdoor_humidity'
    temp = pd.DataFrame(df.groupby([key_gb, 'hour'])[key_val].mean())
    df_gb = pd.pivot_table(temp, values=key_val, index=[key_gb], columns=["hour"], fill_value=0)
    return df_gb


def rooms_df_4heatmap(df,fea,gb,room)


def is_weekday(date):
    nth_day = date.weekday()
    if nth_day <= 4:
        return 1
    else:
        return 0
def gt_preprocess(df_all,low,high):
    df_all['occupancy'] = df_all['illumW'].apply(lambda x: illum_occupancy_reverse(x,low,high))
    df_all['isWeekday'] = df_all['date'].apply(lambda x: is_weekday(x))
    df_model = df_all[['Timestmp','date','illumW','humidity','temperature','motion_rng','motion_var','isWeekday','hour','occupancy']]
    # new feature
    count_vac = len(df_model[df_model['occupancy']==1])
    count_occ = len(df_model[df_model['occupancy']==0])
    pct_of_vac = count_vac/(count_vac+count_occ)
    pct_of_occ = count_occ/(count_vac+count_occ)
    print("percentage of being vacant:", pct_of_vac)
    print("percentage of being occupied:", pct_of_occ)
    if (pct_of_vac - pct_of_occ) >= 0.1:
        print("imbalanced")
    df_model['rolling_mean'] = df_model['motion_rng'].rolling(5).mean()
    df_model.rolling_mean = np.where(df_model.rolling_mean.isnull(),df_model['rolling_mean'][4],df_model['rolling_mean'])
    df_model['rolling_var'] = df_model['motion_var'].rolling(5).mean()
    df_model.rolling_var = np.where(df_model.rolling_var.isnull(),df_model['rolling_var'][4],df_model['rolling_var'])
    return df_model



