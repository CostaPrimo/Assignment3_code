import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

BBox = (10.068123000000002, 10.188866333333333, 56.17214000000001, 56.25717033333334)


def main():
    data = pd.read_csv('Biking.csv', encoding='utf-8').fillna(0)
    gt_lata = data['gt_lat'].iloc[0:].values
    gt_longa = data['gt_long'].iloc[0:].values
    plot(gt_longa, gt_lata)
    print("Choose where to exclude data: ")
    # 10.157, 56.21, 0.002
    exclude(data, float(input('Long: ')), float(input('Lat: ')), float(input('Margin: ')))


def exclude(data, long, lat, r):
    gt_lat = data['phone_lat'].iloc[0:].values
    gt_long = data['phone_long'].iloc[0:].values
    for x in range(len(gt_lat)):
        if lat + r > gt_lat[x] > lat - r and long + r > gt_long[x] > long - r:
            gt_lat[x] = gt_lat[x] + r * (lat/gt_lat[x])
            gt_long[x] = gt_long[x] + r * (long/gt_long[x])
    plot(medianFilter(gt_long), medianFilter(gt_lat))


def medianFilter(datatofilter):
    divideby = 10
    xs = math.ceil(len(datatofilter) / divideby)
    globalcount = 0
    filteredData = []
    for y in range(xs):
        toFilter = []
        filtered = False
        for z in range(divideby):
            if globalcount < len(datatofilter):
                toFilter.append(datatofilter[globalcount])
            globalcount += 1
        while not filtered:
            filteredcount = 0
            tempToFilter = []
            median = np.median(toFilter)
            diffs = []
            for x in toFilter:
                diffs.append(abs(x - median))
            avgdiff = np.mean(diffs)
            maxdiff = max(diffs)
            for x in toFilter:
                if abs(x - median) == maxdiff and maxdiff > avgdiff:
                    tempToFilter.append(median)
                else:
                    tempToFilter.append(x)
                    filteredcount += 1
            if not filteredcount < divideby:
                filtered = True
            else:
                toFilter = tempToFilter
        for x in toFilter:
            filteredData.append(x)
    return filteredData


def plot(long, lat):
    img = plt.imread('map.png')
    fig, ax = plt.subplots()
    ax.imshow(img, extent=BBox)
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])
    ax.plot(long, lat, linewidth=2, c='b')
    plt.show()


if __name__ == '__main__':
    main()
