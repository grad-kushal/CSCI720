import concurrent.futures
import json
import math
import os.path
from datetime import datetime

import matplotlib.pyplot as plotter
from concurrent.futures import ThreadPoolExecutor, as_completed


def read_data_with_thread(list_of_stations):
    # data = []
    intent_map = {0: [], 1: [], 2: []}              # dictionary to map speeds with intent
    for station in list_of_stations:
        if station != "Fig_Speed_Distributions_v04.gif" and not station.startswith("."):
            list_of_data_files = os.listdir(path + station)
            for data_file in list_of_data_files:
                # print(data_file);
                with open(path + station + "/" + data_file, "r") as file_object:        # open file
                    for val in file_object:
                        if not val.startswith("SPEED,INT"):             # header needs to be ignored
                            data_point = val.split(',')
                            # if intent_map.get(int(data_point[1])) is None:
                            #     intent_map[int(data_point[1])] = []
                            list_of_speeds_for_this_intent = intent_map.get(int(data_point[1]))
                            list_of_speeds_for_this_intent.append(round(float(data_point[0])))
    return intent_map


def read_data(dir):
    results = []
    list_of_stations = os.listdir(dir)
    partition_size = int(len(list_of_stations) / 3)
    partitions = [list_of_stations[0:partition_size], list_of_stations[partition_size: partition_size * 2],
                  list_of_stations[partition_size * 2:len(list_of_stations)]]               # divide the data set into 3 parts
    # print(partitions)
    start_time = datetime.now()
    with ThreadPoolExecutor(max_workers=3) as threads:  # Create 3 threads
        futures = [threads.submit(read_data_with_thread, partition) for partition in partitions]  # Submit tasks to the threads for execution
    for future in as_completed(futures):
        results.append(future.result())  # Read data from individual threads once they are complete
    print(datetime.now() - start_time)
    return results


if __name__ == '__main__':
    DIR = "/CS720_HW02_Data_Flag_of_2_Is_Speeders/"
    path = os.path.abspath(os.getcwd()) + DIR
    results = read_data(path)

    bins = [i for i in range(45, 85)]
    data = {0: [], 1: [], 2: []}

    counter = 0
    for result in results:              # Summary of individual thread data
        plotter.boxplot([result[0], result[1], result[2]], labels=['Slow', 'Normal', 'Reckless'])
        plotter.title("Thread: " + str(counter + 1))
        plotter.show()
        counter += 1

    for result in results:              # Collate the data into one dictionary
        data[0] += result[0]
        data[1] += result[1]
        data[2] += result[2]

    # print(len(data[0]))
    # print(len(data[1]))
    # print(len(data[2]))
    # print(min((data[0]) + (data[1]) + (data[2])))
    # print(max((data[0]) + (data[1]) + (data[2])))

    plotter.hist([data[0], data[1], data[2]], bins, color=['Yellow', 'Green', 'Red'], edgecolor='black',    #Histogram of the entire data
                 label=['Slow', 'Normal', 'Reckless'], histtype='barstacked')
    plotter.legend()
    plotter.xlabel('Speed')
    plotter.ylabel('Frequency')
    plotter.title("Entire Data")
    plotter.show()

    plotter.hist([data[0], data[1], data[2]], bins, color=['Yellow', 'Green', 'Red'], edgecolor='black',    #Histogram of the entire data
                 label=['Slow', 'Normal', 'Reckless'])
    plotter.legend()
    plotter.xlabel('Speed')
    plotter.ylabel('Frequency')
    plotter.title("Entire Data")
    plotter.show()

    plotter.hist([data[0] + data[1], data[2]], bins, color=['Green', 'Red'],                        #Histogram of speeders and non-speeders
                 label=["Trying to Speed", "Not trying to Speed"])
    plotter.legend()
    plotter.xlabel('Speed')
    plotter.ylabel('Frequency')
    plotter.title("Normal and Reckless")
    plotter.show()

    best_threshold = math.inf                       #initialize variables
    total_number_of_mistakes = math.inf

    data[0].sort()
    data[1].sort()
    data[2].sort()

    number_of_data_points = len(data[0] + data[1] + data[2])

    # print(data[2].index(46))
    tprs = []                   #initialize lists needed for ROC curve
    fprs = []
    tnrs = []
    fnrs = []
    n = len(data[0] + data[1])              # total non-speeders in the dataset
    p = len(data[2])                        # total speeders in the dataset

    for i in range(46, 85):                 # for each threshold
        non_speeders = list(data[0] + data[1])
        speeders = list(data[2])
        non_speeders.sort()
        speeders.sort()
                                            # calculate the following values
        number_of_false_positives = 0
        number_of_true_negatives = 0
        number_of_false_negatives = 0
        number_of_true_positives = 0

        for threshold_speed in non_speeders:
            if threshold_speed > i:
                number_of_false_positives += 1
            else:
                number_of_true_negatives += 1
        for threshold_speed in speeders:
            if threshold_speed <= i:
                number_of_false_negatives += 1
            else:
                number_of_true_positives += 1

        # del non_speeders[0:non_speeders.index(i) if i < 70 else len(non_speeders)]
        # number_of_false_positives = len(non_speeders)
        # # print(speeders)
        # del speeders[speeders.index(i) if i >= min(speeders) else 0:len(speeders)]
        # number_of_false_negatives = len(speeders)

        current_total_number_of_mistakes = number_of_false_negatives + number_of_false_positives

        if current_total_number_of_mistakes <= total_number_of_mistakes:        # If a new better threshold is found
            total_number_of_mistakes = current_total_number_of_mistakes
            best_threshold = i
            best_fpr = number_of_false_positives / n
            best_tpr = 1 - (number_of_false_negatives / p)
        # print("False positive rate for threshold " + str(i) + ": " + str(
        fprs.append(number_of_false_positives / n)
        # print("True positive rate for threshold " + str(i) + ": " + str(
        tprs.append(1 - (number_of_false_negatives / p))

    print(best_threshold)

    code = """def classify_based_on_threshold(threshold, data):             #new classifier content
    data_after_classification = {1: [], 2: []}
    for speed in data:
        if speed < threshold:
            data_after_classification[1].append(speed)
        else:
            data_after_classification[2].append(speed)
    return data_after_classification"""

    with open("HW_02_Kale_Kushal_Classifier.py", 'w') as code_file:
        code_file.write(code)

    from HW_02_Kale_Kushal_Classifier import classify_based_on_threshold

    classified_data = classify_based_on_threshold(best_threshold, data[0] + data[1] + data[2])

    with open('classified_data.json', 'w') as file:
        file.write(json.dumps(classified_data))

    plotter.plot(fprs, tprs)
    for i in range(0, len(fprs)):
        plotter.plot(fprs[i], tprs[i], marker='x', color='Red')
    plotter.plot(best_fpr, best_tpr, marker='o', color='darkgreen')
    plotter.title('ROC Curve')
    plotter.xlabel('FPR')
    plotter.ylabel('TPR')
    plotter.show()
