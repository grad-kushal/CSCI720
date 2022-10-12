import concurrent.futures
import json
import math
import os.path
from datetime import datetime

from concurrent.futures import ThreadPoolExecutor, as_completed


def read_data_with_thread(list_of_stations):
    # data = []
    intent_map = {0: [], 1: [], 2: []}  # dictionary to map speeds with intent
    for station in list_of_stations:
        if station != "Fig_Speed_Distributions_v04.gif" and not station.startswith(".") and not station.startswith(
                "VALIDATION_DATA"):
            list_of_data_files = os.listdir(path + station)
            for data_file in list_of_data_files:
                # print(data_file);
                with open(path + station + "/" + data_file, "r") as file_object:  # open file
                    for val in file_object:
                        if not val.startswith("SPEED,INT"):  # header needs to be ignored
                            data_point = val.split(',')
                            # if intent_map.get(int(data_point[1])) is None:
                            #     intent_map[int(data_point[1])] = []
                            list_of_speeds_for_this_intent = intent_map.get(int(data_point[1]))
                            list_of_speeds_for_this_intent.append(float(data_point[0]))
    return intent_map


def read_data(dir):
    results = []
    list_of_stations = os.listdir(dir)
    partition_size = int(len(list_of_stations) / 3)
    partitions = [list_of_stations[0:partition_size], list_of_stations[partition_size: partition_size * 2],
                  list_of_stations[partition_size * 2:len(list_of_stations)]]  # divide the data set into 3 parts
    # print(partitions)
    start_time = datetime.now()
    with ThreadPoolExecutor(max_workers=3) as threads:  # Create 3 threads
        futures = [threads.submit(read_data_with_thread, partition) for partition in
                   partitions]  # Submit tasks to the threads for execution
    for future in as_completed(futures):
        results.append(future.result())  # Read data from individual threads once they are complete
    print(datetime.now() - start_time)
    return results


if __name__ == '__main__':
    DIR = "/HW03__DATA__DATA__CS720__DATA/"
    path = os.path.abspath(os.getcwd()) + DIR
    results = read_data(path)

    bins = [i for i in range(45, 85)]
    data = {0: [], 1: [], 2: []}

    for result in results:  # Collate the data into one dictionary
        data[0] += result[0]
        data[1] += result[1]
        data[2] += result[2]

    thresholds = set()
    datalist = data[0] + data[1] + data[2]
    for item in datalist:
        thresholds.add(item)
    datalist = list(thresholds)

    best_threshold = math.inf  # initialize variables
    total_number_of_mistakes = math.inf

    data[0].sort()
    data[1].sort()
    data[2].sort()

    number_of_data_points = len(data[0] + data[1] + data[2])

    tprs = []  # initialize lists needed for ROC curve
    fprs = []
    tnrs = []
    fnrs = []
    n = len(data[0] + data[1])  # total non-speeders in the dataset
    p = len(data[2])  # total speeders in the dataset

    for i in thresholds:  # for each threshold
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

        current_total_number_of_mistakes = number_of_false_negatives + number_of_false_positives

        if current_total_number_of_mistakes <= total_number_of_mistakes:  # If a new better threshold is found
            total_number_of_mistakes = current_total_number_of_mistakes
            best_threshold = i
            best_fpr = number_of_false_positives / n
            best_tpr = 1 - (number_of_false_negatives / p)
        fprs.append(number_of_false_positives / n)
        tprs.append(1 - (number_of_false_negatives / p))

    print(best_threshold)

    code = """import os


def classify_based_on_threshold(threshold):  # new classifier content
    data = []
    data_after_classification = {1: [], 2: []}
    DIR = "/HW03__DATA__DATA__CS720__DATA/"
    path = os.path.abspath(os.getcwd()) + DIR
    NEWLINE = "\\n"

    with open(path + "VALIDATION_DATA_33.csv") as validation_file:
        for line in validation_file:
            if not line.startswith("SPEE"):
                data.append(float(line))
            

    with open(os.path.abspath(os.getcwd()) + "/NW_03_Kale_Kushal_RESULTS.csv", "w") as output_file:
        for speed in data:
            if float(speed) <= threshold:
                data_after_classification[1].append(speed)
                output_file.write("1" + NEWLINE)
            else:
                data_after_classification[2].append(speed)
                output_file.write("2" + NEWLINE)

    return data_after_classification
"""

    with open("NW_03_Kale_Kushal_Classifier.py", 'w') as code_file:
        code_file.write(code)

    from NW_03_Kale_Kushal_Classifier import classify_based_on_threshold

    classified_data = classify_based_on_threshold(best_threshold)
    print(classified_data)

    # with open('classified_data.json', 'w') as file:
    #     file.write(json.dumps(classified_data))

