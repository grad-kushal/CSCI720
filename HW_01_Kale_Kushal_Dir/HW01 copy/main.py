# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import math
import os
import numpy as np
import matplotlib.pyplot as plotter


def read_data(path):
    data = []
    list_of_stations = os.listdir(path)
    for station in list_of_stations:
        if not station.startswith("."):
            list_of_data_files = os.listdir(path + station)
            for data_file in list_of_data_files:
                # print(data_file);
                file_object = open(path + station + "/" + data_file, "r")
                for val in file_object:
                    if float(val) < 40 or float(val) >= 80:
                        continue
                    data.append(float(val))
    return data;


# This methods gives the minimum threshold either with or without regularization.
def binarize_using_otsus_method(bins, thresholds, data, regularization_flag):
    data.sort()
    min_cost = math.inf
    total = 89055
    current_sum_of_frquencies = 0
    threshold_offset = 1
    mixed_vars = []
    best_threshold = 0
    for index in range(1, len(thresholds)):
        current_sum_of_frquencies += bins[index - 1]
        #print(current_sum_of_frquencies)
        weight_left = current_sum_of_frquencies / total
        weight_right = (total - current_sum_of_frquencies) / total

        speed_index = data.index(index + data[0])

        variance_left = np.var(data[0:speed_index])
        variance_right = np.var(data[speed_index:89055])
        mixed_variance = weight_left * variance_left + weight_right * variance_right

        mixed_vars.append(mixed_variance)

        if regularization_flag:
            regularization = abs(current_sum_of_frquencies - (total - current_sum_of_frquencies)) / 50
            # print("REG:" + str(regularization))
            cost = mixed_variance + regularization
        else:
            cost = mixed_variance

        if cost < min_cost:
            min_cost = cost
            best_threshold = index
        index += 1

    return best_threshold + data[0]-threshold_offset, mixed_vars, min_cost


if __name__ == '__main__':
    DIR = "/TrafficStation_Data_for_720/"
    data = read_data(os.path.abspath(os.getcwd()) + DIR)
    print(os.path.abspath(os.getcwd()))
    bins = []
    thresholds = set(data)
    for i in range(0, 40):
        bins.append(0)
    for speed in data:
        bin = speed - 40
        bins[math.floor(bin)] += 1

    # Otsus method without regularization
    best_threshold, mixed_vars, min_cost = binarize_using_otsus_method(bins, thresholds, data, False)
    print("Best: " + str(best_threshold))


    # Otsus method with regularization
    best_threshold_with_reg, mixed_vars_with_reg, min_cost_with_reg = binarize_using_otsus_method(bins, thresholds, data, True)
    print("Best with Reg: " + str(best_threshold_with_reg))


    # Partition into 3 clusters
    under = data[0: data.index(best_threshold)]
    over = data[data.index(best_threshold): 89055]

    thresholds_under = set(under)
    #print(len(thresholds_under))
    thresholds_over = set(over)
    #print(len(thresholds_over))

    threshold1, mixed_vars_under, min_cost_under = binarize_using_otsus_method(bins, thresholds_under, under, False)

    threshold2, mixed_vars_over, min_cost_over = binarize_using_otsus_method(bins, thresholds_over, over, False)

    first = data[0: data.index(best_threshold)]
    second = data[data.index(best_threshold): data.index(threshold2)]
    third = data[data.index(threshold2): 89055]

    b = [i for i in range(40, 80)]
    plotter.hist([under, over], b, color=['Green', 'Red'], edgecolor='black', label=['Under', 'Over'])
    plotter.xlabel('Speed')
    plotter.ylabel('Frequency')
    plotter.show()

    b = [i for i in range(40, 80)]
    plotter.hist([first, second, third], b, color=['Blue', 'Green', 'Red'], edgecolor='black',
                 label=['Under', 'At', 'Over'])
    plotter.xlabel('Speed')
    plotter.ylabel('Frequency')
    plotter.show()

    plotter.plot([i for i in range(40, 79)], mixed_vars)
    plotter.plot(best_threshold, min(mixed_vars), marker='x', color='Red')
    plotter.xlabel('speed')
    plotter.ylabel('mixed variance')
    plotter.show()
