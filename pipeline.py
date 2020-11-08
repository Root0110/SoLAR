import pandas as pd
import matplotlib.pyplot as plt
from statistics import mode
import numpy as np


# get frequency during each second from time stamps
def findFreq(TS):
    firstT = int(TS[0][6:8]) # get the seconds
    cT = 1
    findMode = []
    for i in range(1,len(TS)):
        secondT = int(TS[i][6:8])
        if secondT-firstT != 1:
            cT = cT+1 # count
        else:
            findMode.append(cT)
            cT = 1
        firstT = secondT
        print(i,'    ',findMode)
    return mode(findMode)


def plotData(df,title,freq):
    ax = plt.gca()
    x_v = []
    for i in range(len(df['VacSignal'])):
        x_v.append(i/freq)
    df['time'] = x_v
    df.plot(kind='line',x='time', y='VacSignal',color='red',linewidth=2,figsize=(10,5),ax=ax)
    df.plot(kind='line',x='time', y='OccMinor',color='blue',linewidth=2,figsize=(10,5),ax=ax)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.show()


# Get Each Cycle within Whole Data
# get the 15s scan and 5min sleep window
def splitData(freq,scanLen,sleepLen,data):
    windowSize = (sleepLen + scanLen) * freq # length for all signals within one 'cycle'
    idxWinStart = []
    idxWinEnd = []
    c = 0
    for x in range(0,len(data),windowSize):
        idxWinStart.append(x)
        idxWinEnd.append(idxWinStart[c] + (scanLen * freq) - 1) # store scan part to cycle window
        c += 1
    print('starting cycle:',idxWinStart)
    print('starting cycle:', idxWinEnd)
    return idxWinStart,idxWinEnd


# individual scanning part
def windowSplit(windowSize,idxWinStart,idxWinEnd):
    # Split scan data into 3 windows
    winStart = []
    winEnd = []
    c = 0
    for y in range(idxWinStart,idxWinEnd,windowSize): #100
        winStart.append(y)
        winEnd.append(winStart[c] + windowSize)
        c += 1
    print('window split')
    print(winStart,winEnd)
    return winStart,winEnd



def featureCalc(freq, scanLength, sleepLength, winLength, data, s, f):
    allVariance = 0
    sc = 0
    features = []
    # scanwindows
    idxWinStart, idxWinEnd = splitData(freq, scanLength, sleepLength, data)
    windowSize = winLength * freq
    for x in range(len(idxWinStart)):
        # total scans
        sc = sc + 1
        currentScan = data.iloc[idxWinStart[x]:idxWinEnd[x]]
        ScanVar = currentScan.var()
        allVariance = (((sc - 1) * allVariance) + ScanVar) / sc
        # windows in scan
        WinStart, WinEnd = windowSplit(windowSize, idxWinStart[x], idxWinEnd[x])
        for y in range(len(WinStart)):
            currentWindow = data.iloc[WinStart[y]:WinEnd[y]]
            # cal feature
            if f == "mean*variance":
                features.append(currentWindow.mean() * allVariance)
            elif f == "mean":
                features.append(currentWindow.mean())
            elif f == "max":
                features.append(currentWindow.max())
            elif f == "min":
                features.append(currentWindow.min())
            elif f == "variance":
                features.append(currentWindow.var())
    return features


def handle_noise(df1):
    medianV = df1.loc[df1['VacSignal'] < 500, 'VacSignal'].median()
    medianO = df1.loc[df1['OccMinor'] < 500, 'OccMinor'].median()
    df1['VacSignal'] = df1['VacSignal'].mask(df1['VacSignal'] > 500, medianV)

    df1['OccMinor'] = df1['OccMinor'].mask(df1['OccMinor'] > 500, medianO)

    medianV = df1.loc[df1['VacSignal'] > 250, 'VacSignal'].median()
    medianO = df1.loc[df1['OccMinor'] > 250, 'OccMinor'].median()
    df1['VacSignal'] = df1['VacSignal'].mask(df1['VacSignal'] < 250, medianV)

    df1['OccMinor'] = df1['OccMinor'].mask(df1['OccMinor'] < 250, medianO)
    #     new_df=pd.DataFrame()
    #     new_df['VacSignal']=data['VacSignal'].rolling(5).mean()
    #     new_df['OccMinor']=data['OccMinor'].rolling(5).mean()
    #     new_df['TimeStamp']=data['TimeStamp']
    return df1


def plotDataNew(df, v, winLength):
    # plot the features
    ax = plt.gca()
    x_time = np.arange(0, len(df) * winLength, winLength)
    df['time'] = x_time
    df.plot(kind='line', x='time', y='VacSignal', color='red', linewidth=2, figsize=(20, 10), ax=ax)
    df.plot(kind='line', x='time', y='OccMinor', color='green', linewidth=2, figsize=(20, 10), ax=ax)
    for xc in x_time:
        plt.axvline(x=xc)
    plt.title(v, fontsize=14, fontweight='bold')
    plt.savefig(v + '.png')
    plt.show()

def noiseOption(df,withNoise):
    if withNoise=="yes":
        all_dataframe=[df]
        datatype=["With Noise"]
        df_h=pd.DataFrame()
    elif withNoise=="no":
        df_h=handle_noise(df)
        all_dataframe=[df_h]
        datatype=["Without Noise"]
    elif withNoise=="both":
        all_dataframe=[df]
        df1 = df.copy()
        df_h=handle_noise(df1)
        all_dataframe.append(df_h)
        datatype=["With Noise","Without Noise"]
    return df_h,datatype,all_dataframe


def main():
    alldata = ['MediumRoomAug.xlsx', 'SmallRoomAug.xlsx', 'BigRoomAug.xlsx']
    scanLength = int(input("Enter Scan Length in secs"))
    sleepLength = int(input("Enter Sleep Length in secs"))
    winLength = int(input("Enter Window Length in secs"))
    f = input("Enter feature you want to plot: Mean,Variance,Max,Min,mean*Variance ").lower()
    withNoise = input(
        "Enter 'yes' for graph with noise \nEnter 'no' for graph without noise \nEnter 'both' if you want to draw comparison").lower()
    signals = ['VacSignal', 'OccMinor']
    for x in range(len(alldata)):
        df_feats = pd.DataFrame()
        data = pd.read_excel(alldata[x])
        df = pd.DataFrame(data)
        print(alldata[x])
        df_h, datatype, all_dataframe = noiseOption(df, withNoise)
        # find freq
        freq = findFreq(df['TimeStamp'])
        c = 0
        for i in all_dataframe:
            plotData(i, alldata[x] + " " + datatype[c], freq)
            for s in signals:
                print(s)
                # storing feature values in array feats
                feats = featureCalc(freq, scanLength, sleepLength, winLength, i[s], s, f)
                df_feats[s] = feats
            # plotting new features
            plotDataNew(df_feats, alldata[x] + "" + f + " Feature" + " " + datatype[c], winLength)
            c += 1


if __name__ == '__main__':
    main()