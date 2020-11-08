import csv
import random
import time

ts = 0
signal = 200
#feature = 100
fieldnames = ['time', 'signal']
with open('graph_test1.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:
    with open('graph_test1.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        info = {
            'time': ts,
            'signal': signal,
            #'feature': feature
        }
        csv_writer.writerow(info)
        print(ts, signal)
        ts += 1

        signal += random.randint(-10, 10)
        #feature += random.randint(-50, 50)
    time.sleep(1)

