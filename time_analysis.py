import matplotlib
import matplotlib.pyplot as plt
import numpy as np

timesFile = open('times.txt')
timesContent = timesFile.readlines()
timesFile.close()

win_serial = []
win_multi = []
lin_serial = []
lin_multi = []

i = 0
while i < len(timesContent)-1:
    platform_type = timesContent[i]
    time = timesContent[i+1]
    if 'Windows' in platform_type:
        if 'serial' in platform_type:
            win_serial.append(float(time[:len(time)-1]))
        else:
            win_multi.append(float(time[:len(time)-1]))
    else:
        if 'serial' in platform_type:
            lin_serial.append(float(time[:len(time)-1]))
        else:
            lin_multi.append(float(time[:len(time)-1]))
    i += 2
    
print(win_serial)
print(win_multi)
print(lin_serial)
print(lin_multi)

labels = ['Windows', 'Linux (Chromebook)']
serial_means = np.around([np.mean(win_serial), np.mean(lin_serial)], decimals=3)
multi_means = np.around([np.mean(win_multi), np.mean(lin_multi)], decimals=3)

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, serial_means, width, label='Serial')
rects2 = ax.bar(x + width/2, multi_means, width, label='Multiprocessing')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Times (seconds)')
ax.set_title('Times by platform and execution type')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 0),  # no vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()
fig.savefig('times.png')
