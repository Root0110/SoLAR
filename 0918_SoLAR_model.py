# coding   : utf-8
# @Time    :9/17/20 15:06
# @Author  :Xiaohan
# @FileName:SoLAR_model.py
# @SoftWare:PyCharm

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



def is_valid(new_value, down_limit, up_limit):
    if new_value <= up_limit and new_value >= down_limit:
        return True
    else:
        return False


def feature_update(old_raw, new_value, f_types, f_values, win_size):
    # Given old raw data and new value, calculate new feature values
    # Return a single updated feature
    # f_values = {'sum': , 'avg': ,'max': ,'min': ,'range': ,'var': }
    # get the last (win_size-1) numbers
    target_scan = list(old_raw[-1:-win_size:-1])
    # print('target:', target_scan)
    for f_type in f_types:
        if f_type == 'Average':
            f_values['Sum'] = sum(target_scan) + new_value
            f_values['Average'] = f_values['Sum'] / win_size
        elif f_type == 'Range':
            f_values['Max'] = max(target_scan)
            f_values['Min'] = min(target_scan)
            if new_value > f_values['Max']:
                f_values['Max'] = new_value
            if new_value < f_values['Min']:
                f_values['Min'] = new_value
            f_values['Range'] = f_values['Max'] - f_values['Min']
        elif f_type == 'Variance':
            # point level within in each scan window
            data_win = target_scan + [new_value]
            avg_list = [data_win[0]]
            var_list = [0]
            for i in range(1,win_size):
                avg_list.append(avg_list[i-1] + (data_win[i] - avg_list[i-1]) / (i+1))
                var_list.append(var_list[i-1] + (data_win[i] - avg_list[i-1]) * (data_win[i] - avg_list[i]))
            f_values['Variance'] = var_list[-1]
    return f_values


# Given a file containing 2 columns of data: timestamp, raw signal data
def plot_diff_updates(f_types):
    ts = []
    win = []
    sig = []
    fea = {'1': [], '2': [], '3': []}
    i = 0
    win_num = 0
    win_n_data = 4  # how many signal values each window contains
    scan_n_win = 3  # how many windows each scan contains
    tick_loc = []
    n = len(f_types)  # the number of feature plots
    f_values = {'Sum': 0, 'Average': 0, 'Max': 0, 'Min': 0, 'Range': 0, 'Variance': 0}

    def tick_location(win_num, tick_loc):
        # when the last element in one window is going to be read
        if win_num != 0 and win_num % scan_n_win == 0:  # at the end of one scan
            # tloc = win_num * win_n_data - 1
            tick_loc.append(win_num)
        return tick_loc

    def tick_function(win_num):
        tvalues = range(1, win_num // scan_n_win + 1)
        return tvalues

    plt.ion()
    fig = plt.figure(figsize=(5, 10))
    try:
        while True:
            plt.clf()
            data = pd.read_csv('/Users/xhw/PycharmProjects/InstaHub/graph_test1.csv')
            ts.append(data['time'][i])
            sig.append(data['signal'][i])
            ax1 = fig.add_subplot(n + 1, 1, 1)
            ax1.plot(ts, sig, 'g-')
            ax1.grid(ls='-.')
            ax1.set_title('Trendline Plot of Raw Signal Data')
            ax1.set_ylabel('Raw Signal Data')
            ax1.set_xlabel('Timestamp')

            if i % win_n_data != (win_n_data - 1):
                win.append(np.nan)
                # append nan for each feature value
                for j in range(n):
                    fea[str(j + 1)].append(np.nan)
            else:
                win_num += 1
                win.append(win_num)
                f_values = feature_update(data['signal'][:i], data['signal'][i], f_types, f_values, win_n_data)
                for j in range(n):
                    fea[str(j + 1)].append(f_values[f_types[j]])

                tick_loc = tick_location(win_num, tick_loc)

            for j in range(n):
                axx = fig.add_subplot(n + 1, 1, j + 2)
                axx.plot(win, fea[str(j + 1)], 'r.')
                axx_sub = axx.twiny()  # add minor x-axis
                axx.grid(axis='x', ls='-.')
                axx.tick_params(axis='x', which='major', labelsize=5)
                # axx.xaxis.set_ticklabels([])
                axx.set_title('Scatter Plot of Feature({}) Values'.format(f_types[j]))
                axx.set_ylabel('{}'.format(f_types[j]))
                axx.set_xlabel('Window_num', fontsize=6)
                x_major_locator = MultipleLocator(1)
                axx.xaxis.set_major_locator(x_major_locator)
                axx_sub.set_xlim(axx.get_xlim())
                axx_sub.set_xticks(tick_loc)
                new_ticks = tick_function(win_num)
                axx_sub.set_xticklabels(new_ticks)
                axx_sub.set_xlabel("Scan_num")

                plt.tight_layout()
            plt.show()
            i += 1
            plt.pause(0.5)
    except:
        plt.gca()
        plt.show()
    plt.ioff()
    plt.show()


plot_diff_updates(['Range', 'Average','Range'])
