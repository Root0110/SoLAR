import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def get_new()


def is_valid(new_value, down_limit, up_limit):
    if new_value < down_limit or new_value > up_limit:
        return False
    else:
        return True


def plot_realtime():
    def animate(i):
        data = pd.read_csv('/Users/xhw/PycharmProjects/InstaHub/graph_test1.csv')
        x = data['time']
        y1 = data['signal']
        y2 = data['feature']
        plt.cla()
        plt.plot(x, y1, label='signal')
        plt.plot(x, y2, label='feature')
        plt.legend(loc='upper left')
        plt.tight_layout()
    ani = FuncAnimation(plt.gcf(), animate, interval=1000)
    plt.tight_layout()
    plt.show()


def feature_update(new_value, f_type, f_values, scan_count, window_limit, down_limit, up_limit):
    # f_values = {'sum': , 'avg': ,'max': ,'min': ,'range': ,'var': }
    if not is_valid(new_value,down_limit, up_limit):
        get_new()
        return
    plot_realtime()
    scan_count += 1  # scan count
    # update point_level_features
    if f_type == 'Average':
        f_values['sum'] += new_value
        # update scan_level features
        if scan_count > window_limit:
            f_values['avg'] = f_values['sum']/scan_count
            plot_realtime()
            f_values['sum'], f_values['avg'], scan_count,= 0,0,0
    elif f_type == 'Range':
        if new_value > f_values['max']:
            f_values['max'] = new_value
        if new_value < f_values['min']:
            f_values['min'] = new_value
        if scan_count > window_limit:
            f_values['range'] = f_values['max'] - f_values['min']
            plot_realtime()
            f_values['max'], f_values['min'], f_values['range'],scan_count = 0,0,0,0
    elif f_type == 'Variance':
        # no point_level feature need to be updated
        # update scan_level_feature
        if scan_count > window_limit:
            avg_old = f_values['avg']
            avg_new = (f_values['sum'] + new_value)/scan_count
            f_values['var'] += (new_value - avg_old) * (new_value - avg_new)
    return f_values

def continuous_plot():
    x = []
    y = []
    i = 0
    plt.ion()



def plot_raw():
    x = []
    y = []
    i = 0
    plt.ion()
    try:
        while True:
            plt.clf()
            data = pd.read_csv('/Users/xhw/PycharmProjects/InstaHub/graph_test1.csv')
            # plot the first figure
            x.append(data['time'][i])
            y.append(data['signal'][i])
            fig1 = plt.subplot(2, 1, 1)
            fig1.set_title('Trendline Plot of Raw Signal Data')
            fig1.set_ylabel('Signal Data')
            plt.plot(x, y, 'g-')
            i += 1
            plt.pause(1)
    except:
        plt.gca()
        plt.show()
    plt.tight_layout()
    plt.ioff()
    plt.show()


def feature_upd(new_data, curr_sum):
    curr_sum += new_data
    return curr_sum

def plot_feature():
    x = []
    y = []
    f = []
    i = 0
    curr_sum = 0
    scan_count = 0
    plt.ion()
    try:
        while True:
            data = pd.read_csv('/Users/xhw/PycharmProjects/InstaHub/graph_test1.csv')
            scan_count += 1
            x.append(data['time'][i])
            y.append(data['signal'][i])
            fig2 = plt.subplot(2, 1, 2)
            fig2.set_title('Scatter Plot of Feature Values')
            fig2.set_ylabel('Feature Values')
            fig2.set_xlabel('Timestamp')
            # when the scan_count reaches the window_size, plot scan_level features
            # this func would be called in another func, which checks whether scan_count=window_size
            curr_sum = feature_upd(y[i], curr_sum)
            f.append(curr_sum / scan_count)
            print(f)

            # feature[] only contains the scan_level values, less than the number of point_level values
            # f.append(data['feature'][i // 5])
            # print('*',f)
            fig2.plot(x, f, 'r.')
            plt.tight_layout()
            i += 1
            plt.pause(1)
    except:
        plt.gca()
        plt.show()

    plt.tight_layout()
    plt.ioff()
    plt.show()




class SlidingWindow:
    def __init__(self):
        self.curr_max = 0
        self.curr_min = 0
        self.mean = 0
        self.var = 0
        self.downLimit = float('inf')
        self.upLimit = float('inf')

    def group_update(self, store_dict, new_ts, new_signal_data, feature):
        if not self.is_valid(new_signal_data): # if not valid, move to the next one
            return
        init_ts = store_dict['timestamp'][0]
        if int(new_ts[6:8]) - int(init_ts[6:8]) <= time_period:
            store_dict['signal_data'].append(new_signal_data)
            self.feature_update(store_dict['signal_data'],feature)
        else:  # reset
            store_dict['signal_data'] = []
            store_dict['timestamp'] = []

    def feature_update(self,signal_data,feature):
        new = signal_data[-1]
        if feature == 'Range':
            if new > self.curr_max:
                self.curr_max = new
            if new < self.curr_min:
                self.curr_min = new
        elif feature == 'Average':
            self.mean = sum(signal_data)/len(signal_data)
        elif feature == 'Variance':
            self.var = np.var(signal_data)

    def plot(self,store_dict):
        plt.plot(store_dict['timestamp'], store_dict['signal_data'], linestyle="dashed", color="red")

