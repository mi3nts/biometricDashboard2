import numpy as np
import math
from SelectFrequency import getAmplitudesByFrequencyBand
from SelectFrequency import getAmplitudeByFreqIndex
from SelectFrequency import getInterval
import scipy.signal as sps
from scipy import stats

# takes in the data from EEG, and calls the fourier transform
# and processes it so it can be passed into the plot/cmap

def getCmapByFreqVal(data, newdata, freqValue, globalMax):
    # delete first row
    data = np.delete(data, 0, 0)

    # add newdata as a row at the end of data. columns=electrodes rows=timestep
    data = np.vstack([data, newdata])
    data = np.transpose(data)

    # compute power spectrum of data
    f, ps = sps.welch(data, fs=26)
    #print("ps", ps)
    #print("f", f)

    extractAmplitude = []
    # delta freq band
    if(freqValue == -1):
        extractAmplitude = getAmplitudesByFrequencyBand(ps, 0)
    # theta freq band
    elif freqValue == -2:
        extractAmplitude = getAmplitudesByFrequencyBand(ps, 1)
    # alpha freq band
    elif freqValue == -3:
        extractAmplitude = getAmplitudesByFrequencyBand(ps, 2)
    # specific freq value wanted
    else:
        interval = [freqValue - 0.5, freqValue + 0.5]
        startIndex = -1
        endIndex = -1
        for i in range(len(f)):
            if interval[0] <= f[i] <= interval[1]:
                if startIndex == -1:
                    startIndex = i
                else:
                    endIndex = i

        print("start ", startIndex, f[startIndex],
              "end ", endIndex, f[endIndex])
        extractAmplitude = ps[:, startIndex:endIndex]

    temp = np.asarray(extractAmplitude)

    # temp holds mean of each row in extractAmplitude
    temp = np.mean(temp, axis=1)
    localMax = max(np.amax(temp), globalMax)

    for i in range(len(temp)):
        # normalize all amplitudes by the global max
        temp[i] = temp[i] / localMax
    return [temp, localMax, data]


def getCmapForZscores(data, newdata, freqValue):
    # delete first row of data
    data = np.delete(data, 0, 0)

    # add newdata as a row at the end of data. columns=electrodes rows=timestep
    data = np.vstack([data, newdata])
    data = np.transpose(data)

    # compute power spectrum of data
    f, ps = sps.welch(data, fs=26)
    print("ps", ps)

    extractAmplitude = []
    # delta freq band
    if(freqValue == -1):
        extractAmplitude = getAmplitudesByFrequencyBand(ps, 0)
    # theta freq band
    elif freqValue == -2:
        extractAmplitude = getAmplitudesByFrequencyBand(ps, 1)
    # alpha freq band
    elif freqValue == -3:
        extractAmplitude = getAmplitudesByFrequencyBand(ps, 2)
    # specific freq value wanted
    else:
        startIndex, endIndex = getInterval(f, freqValue)
        extractAmplitude = ps[:, startIndex:endIndex]

    temp = np.asarray(extractAmplitude)
    # temp holds mean of each row in extractAmplitude
    temp = np.mean(temp, axis=1)
    print("temp", temp)

    # square all values to make them 0 <= x <= 1
    temp = np.square(temp)
    # calculate zscores for the array
    zscoreArray = stats.zscore(temp)

    # next line creates positive and negative zscores, so if the value was between 0 to 0.5, it is
    # scaled to between -1 and 0, and if the value was between 0.5 and 1, it is scaled to between
    # 0 and 1
    zscoreArray = ((zscoreArray / np.amax(zscoreArray)) / 2) + 0.5
    return [zscoreArray, data]