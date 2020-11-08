# @Author: Hannah Wang
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


data = pd.read_csv('/Users/xhw/PycharmProjects/InstaHub/graph_test1.csv')
sig = data['signal'][:10]
f_values = {'Sum': 0, 'Average': 0, 'Max': 0, 'Min': 0, 'Range': 0, 'Variance': 0}
feature_update(sig,data['signal'][10],['Variance'], f_values,3)





# Given a file containing 2 columns of data: timestamp, raw signal data
def plot_diff_updates(f_types):
    ts = []
    win = []
    sig = []
    fea = {'1': [], '2': [], '3': []}
    i = 0
    win_num = 0
    win_size = 3
    n = len(f_types)
    f_values = {'Sum': 0, 'Average': 0, 'Max': 0, 'Min': 0, 'Range': 0, 'Variance': 0}
    plt.ion()
    try:
        while True:
            plt.clf()
            data = pd.read_csv('/Users/xhw/PycharmProjects/InstaHub/graph_test1.csv')
            ts.append(data['time'][i])
            sig.append(data['signal'][i])
            fig1 = plt.subplot(n+1, 1, 1)
            plt.plot(ts, sig, 'g-')
            fig1.set_title('Trendline Plot of Raw Signal Data')
            fig1.set_ylabel('Raw Signal Data')
            fig1.set_xlabel('Timestamp')

            if i % win_size != (win_size - 1):
                win.append(np.nan)
                # append nan for each feature value
                for j in range(n):
                    fea[str(j + 1)].append(np.nan)
            else:
                win_num += 1
                win.append(win_num)
                f_values = feature_update(data['signal'][:i], data['signal'][i], f_types, f_values, win_size)
                for j in range(n):
                    fea[str(j + 1)].append(f_values[f_types[j]])
            for j in range(n):
                plt.subplot(n+1, 1, j+2)
                plt.plot(win, fea[str(j+1)], 'r.')
            '''fig2 = plt.subplot(2, 1, 2)
            plt.plot(win, fea, 'r.')
            fig2.set_title('Scatter Plot of Feature({}) Values'.format(f_type))
            fig2.set_ylabel('{}'.format(f_type))
            fig2.set_xlabel('Window')
            plt.tight_layout()'''
            plt.show()
            i += 1
            plt.pause(1)
    except:
        plt.gca()
        plt.show()
    plt.ioff()
    plt.show()

#plot_diff_updates(['Range','Average'])







def test_multiplt():
    x = [1, 2, 3, 4]
    y = [[20, 40, 45, 12], [-20, -40, -45, -12], [2, 3, 0, 4]]
    '''for i in range(3):
        fig = plt.figure(figsize=(5,5))
        fig.add_subplot(2,2, i+1)
        #fig = plt.subplot(3,1,i+1)
        plt.plot(x,y[i],'g.')
        plt.tight_layout()
        plt.draw()
        plt.rcParams["figure.figsize"] = (5,15)
    plt.show()'''
    fig, ax = plt.subplots(2, 3, sharex='col', sharey='row')
    for i in range(2):
        for j in range(3):
            ax[i, j].text(0.5, 0.5, str((i, j)),
                          fontsize=18, ha='center')
            plt.show()

#test_multiplt()
