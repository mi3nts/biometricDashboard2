def getAmplitudesByFrequencyBand(ps, x):
    # if delta freq wanted
    if x == 0:
        return ps[:, 3:9]
    # if theta freq wanted
    elif x == 1:
        return ps[:, 10:19]
    # if alpha freq wanted
    elif x == 2:
        return ps[:, 20:29]


def getAmplitudeByFreqIndex(ps, x):
    return ps[: x]


def getInterval(f, freqValue):
    # gets the start and end indices of the ps array that
    # are +/- 0.5 away from the given frequency value. This freq
    # value is the one that the visualization will be generated for
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
    return [startIndex, endIndex]
