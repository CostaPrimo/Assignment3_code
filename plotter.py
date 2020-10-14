import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def main():
    # Reading and setting data from CSV
    data = pd.read_csv('Biking.csv', encoding='utf-8').fillna(0)
    timeplot = data['#TimestampInMS'].iloc[0:].values
    p_lat = data['phone_lat'].iloc[0:].values
    p_long = data['phone_long'].iloc[0:].values
    gt_lat = data['gt_lat'].iloc[0:].values
    gt_long = data['gt_long'].iloc[0:].values
    # Plotting Raw data
    plot(p_long, p_lat, 'Raw Phone')
    plot(gt_long, gt_lat, 'Raw GT')
    # Plotting Mean Filtered data
    plot(meanFilter(p_long), meanFilter(p_lat), 'Mean Filtered Phone')
    plot(meanFilter(gt_long), meanFilter(gt_lat), 'Mean Filtered GT')
    # Plotting Median Filtered data
    plot(medianFilter(p_long), medianFilter(p_lat), 'Median Filtered Phone')
    plot(medianFilter(gt_long), medianFilter(gt_lat), 'Median Filtered GT')


# Method for Plotting
def plot(long, lat, name):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # Setting labels
    ax.set_title(name)
    ax.set_xlabel("Long")
    ax.set_ylabel("Lat")
    # Plotting Data
    ax.plot(long, lat, c='r', label='Data')
    leg = ax.legend()
    # Show plot
    plt.show()


def meanFilter(datatofilter):
    # Size of segments
    divideby = 10
    # Amount of Segments
    xs = math.ceil(len(datatofilter)/divideby)
    # Accessor variable
    globalcount = 0
    # Placeholder for filtered data
    filteredData = []
    for y in range(xs):
        # Placeholder for data to be filtered
        toFilter = []
        # Boolean for deciding if segment has been filtered
        filtered = False
        # Adding values to the toFilter list
        for z in range(divideby):
            if globalcount < len(datatofilter):
                toFilter.append(datatofilter[globalcount])
            globalcount += 1
        # Filtering the Data
        while not filtered:
            # Counter for checking filtered values
            filteredcount = 0
            # Placeholder for values in between re-filtering of data
            tempToFilter = []
            # Initial mean of the data
            mean = np.mean(toFilter)
            # Placeholder for the differences between values and the mean
            diffs = []
            # Calculating all the diffs
            for x in toFilter:
                diffs.append(abs(x-mean))
            # The avg diff
            avgdiff = np.mean(diffs)
            # The max diff
            maxdiff = max(diffs)
            # Actual filtering of data
            for x in toFilter:
                # If biggest diff and diff is bigger than avg, replace value with mean
                if abs(x-mean) == maxdiff and maxdiff > avgdiff:
                    tempToFilter.append(mean)
                # Else keep original value and count up filtercount
                else:
                    tempToFilter.append(x)
                    filteredcount += 1
            # If every value has been filtered stop the filter process
            if not filteredcount < divideby:
                filtered = True
            # Else replace toFilter with the placeholder and repeat.
            else:
                toFilter = tempToFilter
        # Add filtered data to the filteredData list.
        for x in toFilter:
            filteredData.append(x)
    # Return filtered data
    return filteredData


def medianFilter(datatofilter):
    # Size of segments
    divideby = 10
    # Amount of Segments
    xs = math.ceil(len(datatofilter) / divideby)
    # Accessor variable
    globalcount = 0
    # Placeholder for filtered data
    filteredData = []
    # Adding values to the toFilter list
    for y in range(xs):
        # Placeholder for data to be filtered
        toFilter = []
        # Boolean for deciding if segment has been filtered
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
            # Calculating all the diffs
            for x in toFilter:
                diffs.append(abs(x - median))
            # The avg diff
            avgdiff = np.mean(diffs)
            # The max diff
            maxdiff = max(diffs)
            # Actual filtering of data
            for x in toFilter:
                # If biggest diff and biggest diff is bigger than avg, replace value with median
                if abs(x - median) == maxdiff and maxdiff > avgdiff:
                    tempToFilter.append(median)
                # Else keep original value and count up filtercount
                else:
                    tempToFilter.append(x)
                    filteredcount += 1
            # If every value has been filtered stop the filter process
            if not filteredcount < divideby:
                filtered = True
            # Else replace toFilter with the placeholder and repeat.
            else:
                toFilter = tempToFilter
        # Add filtered data to the filteredData list.
        for x in toFilter:
            filteredData.append(x)
    # Return filtered data
    return filteredData


if __name__ == '__main__':
    main()
