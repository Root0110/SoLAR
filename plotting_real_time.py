import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np
import matplotlib.pyplot as plt


scan_win_num = 2
fig, ax = plt.subplots(3, 1, figsize=(3, 6))
x = [0, 1, 2, 3, 4, 5]
fea = {'0': [-3, -2, -1, -8, 0, 0], '1': [np.nan, 15, np.nan, 13, np.nan, 17], '2': [np.nan, 4, np.nan, 10, np.nan, 6]}

ax[0].plot(x,fea['0'])
ax[0].grid(ls='-.')
ax[0].set_title('Trendline Plot of Raw Signal Data')
ax[0].set_ylabel('Raw Signal Data')
ax[0].set_xlabel('Timestamp')


def tick_location(x):
    tloc = []
    for i in range(len(x)):
        if i % scan_win_num == 1:
            tloc.append(i)
    return np.array(tloc)


def tick_function(X):
    V = (X + 1) / scan_win_num
    return [z for z in V]


for i in range(1, 3):
    ax[i].plot(x, fea[str(i)], 'g.')
    ax_sub = ax[i].twiny()
    ax[i].grid(axis='x', ls='-.')
    ax[i].xaxis.set_ticklabels([])
    ax[i].set_title('Scatter Plot of Feature({}) Values'.format(i))
    ax[i].set_ylabel('{}'.format(i))

    new_tick_locations = tick_location(x)
    ax_sub.set_xlim(ax[i].get_xlim())
    ax_sub.set_xticks(new_tick_locations)
    ax_sub.set_xticklabels(tick_function(new_tick_locations))
    ax_sub.set_xlabel("Modified x-axis: Scan_num")

plt.tight_layout()
# ax.axes.xaxis.set_visible(False)
plt.show()