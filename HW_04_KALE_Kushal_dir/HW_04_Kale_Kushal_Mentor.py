import concurrent.futures
import json
import math
import os.path
from datetime import datetime

from concurrent.futures import ThreadPoolExecutor, as_completed


def read_data_with_thread(list_of_stations):
    # Brightness,Weight,Precip,LaneChanges,Speed,PulledOver
    maps = list()

    # dictionaries to map attribute values with the classification
    brightness_classification_map = {'y\n': [], 'n\n': []}
    weight_classification_map = {'y\n': [], 'n\n': []}
    precip_classification_map = {'y\n': [], 'n\n': []}
    lanechanges_classification_map = {'y\n': [], 'n\n': []}
    speed_classification_map = {'y\n': [], 'n\n': []}
    maps.append(brightness_classification_map)
    maps.append(weight_classification_map)
    maps.append(precip_classification_map)
    maps.append(lanechanges_classification_map)
    maps.append(speed_classification_map)

    for station in list_of_stations:
        if station != "Fig_Speed_Distributions_v04.gif" and not station.startswith(".") and not station.startswith(
                "Validation"):
            list_of_data_files = os.listdir(path + station)
            for data_file in list_of_data_files:
                with open(path + station + "/" + data_file, "r") as file_object:  # open file
                    for val in file_object:
                        if not val.startswith("RecID"):  # headers need to be ignored
                            attr_list = val.split(',')
                            attr_list.pop(0)
                            for i in range(0, len(maps)):
                                current_map = maps[i]
                                current_class = attr_list[-1]
                                list_of_values_for_this_attribute = current_map.get(current_class)
                                list_of_values_for_this_attribute.append(float(attr_list[i]))
    return maps


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
    DIR = "/CS_720_Data_for_HW04/"
    path = os.path.abspath(os.getcwd()) + DIR
    results = read_data(path)

    attribute_names = ['brightness', 'weight', 'precip', 'lanechanges', 'speed']

    bins = [i for i in range(45, 85)]
    data = list()

    overall_least = math.inf

    # dictionaries to map attribute values with the classification
    brightness_classification_map = {'y\n': [], 'n\n': []}
    weight_classification_map = {'y\n': [], 'n\n': []}
    precip_classification_map = {'y\n': [], 'n\n': []}
    lanechanges_classification_map = {'y\n': [], 'n\n': []}
    speed_classification_map = {'y\n': [], 'n\n': []}
    data.append(brightness_classification_map)
    data.append(weight_classification_map)
    data.append(precip_classification_map)
    data.append(lanechanges_classification_map)
    data.append(speed_classification_map)

    for result in results:  # Collate the data into one dictionary
        for i in range(len(data)):
            current_map = data[i]
            map_to_add = result[i]
            current_list = current_map.get('y\n')
            current_list.extend(map_to_add.get('y\n'))
            current_map['y\n'] = current_list
            current_list = current_map.get('n\n')
            current_list.extend(map_to_add.get('n\n'))
            current_map['n\n'] = current_list

    thresholds = [set(), set(), set(), set(), set()]
    best_thresholds = list()
    least_no_of_mistakes = list()


    invert_flag = False
    # Find the best threshold and the least number of mistakes for each attribute in data
    for i in range(len(data)):
        datalist = data[i]['y\n'] + data[i]['n\n']

        for item in datalist:                       # Get unique thresholds by adding in set
            thresholds[i].add(item)

        best_thresholds.append(math.inf)            # initialize variables
        total_number_of_mistakes = math.inf

        data[i]['y\n'].sort()
        data[i]['n\n'].sort()

        number_of_data_points = len(data[i]['y\n'] + data[i]['n\n'])

        tprs = []  # initialize lists needed for ROC curve
        fprs = []
        tnrs = []
        fnrs = []
        n = len(data[i]['n\n'])  # total non-speeders in the dataset
        p = len(data[i]['y\n'])  # total speeders in the dataset

        tmp = list(thresholds[i])
        tmp.sort()
        for current_threshold in tmp:               # for each threshold, calculate the number of mistakes
            tickets = list(data[i]['y\n'])
            tickets_not = list(data[i]['n\n'])
            tickets.sort()
            tickets_not.sort()
        # calculate the following values
            number_of_false_positives = 0
            number_of_true_negatives = 0
            number_of_false_negatives = 0
            number_of_true_positives = 0

            for threshold_value in tickets_not:
                if threshold_value > current_threshold:
                    number_of_false_positives += 1
                else:
                    number_of_true_negatives += 1
            for threshold_value in tickets:
                if threshold_value <= current_threshold:
                    number_of_false_negatives += 1
                else:
                    number_of_true_positives += 1

            number_of_mistakes = number_of_false_positives + number_of_false_negatives # This is left mistakes1
            number_of_corrects = number_of_true_positives + number_of_true_negatives # This is right mistakes2
            current_total_number_of_mistakes = min(number_of_true_positives, number_of_false_positives) + min(number_of_true_negatives, number_of_false_negatives)

            if current_total_number_of_mistakes <= total_number_of_mistakes:  # If a new better threshold is found, assign the values accordingly
                total_number_of_mistakes = current_total_number_of_mistakes
                best_thresholds[i] = current_threshold
                if number_of_mistakes <= overall_least:
                    invert_flag = False;
                    overall_least = number_of_mistakes;
                elif number_of_corrects <= overall_least:
                    overall_least = number_of_corrects
                    invert_flag = True;
                best_fpr = number_of_false_positives / n
                best_tpr = 1 - (number_of_false_negatives / p)
            fprs.append(number_of_false_positives / n)
            tprs.append(1 - (number_of_false_negatives / p))
        least_no_of_mistakes.append(total_number_of_mistakes)

    print("Thresholds by attributes:\t\t\t\t" + str(best_thresholds))
    print("Least number of mistakes by attributes:\t" + str(least_no_of_mistakes))

    best_attr_to_split_on = least_no_of_mistakes.index(min(least_no_of_mistakes))
    print("Best attribute to split on:\t\t\t\t" + attribute_names[best_attr_to_split_on])

    code = """import os


def classify_based_on_threshold(threshold, attr_index, invert_flag):  # new classifier content
    data = list()
    print("Threshold provided to the classifier: \t" + str(threshold))
    brightness_classification_map = {'y\\n': [], 'n\\n': []}  # dictionary to map speeds with intent
    weight_classification_map = {'y\\n': [], 'n\\n': []}
    precip_classification_map = {'y\\n': [], 'n\\n': []}
    lanechanges_classification_map = {'y\\n': [], 'n\\n': []}
    speed_classification_map = {'y\\n': [], 'n\\n': []}
    data.append(brightness_classification_map)
    data.append(weight_classification_map)
    data.append(precip_classification_map)
    data.append(lanechanges_classification_map)
    data.append(speed_classification_map)
    
    data_after_classification = {'y\\n': [], 'n\\n': []}
    DIR = "/CS_720_Data_for_HW04/"
    path = os.path.abspath(os.getcwd()) + DIR
    NEWLINE = "\\n"
    result = []

    with open(path + "Validation_33.csv") as validation_file:
        for line in validation_file:
            if not line.startswith("RecID"):
                attr_list = line.split(',')
                attr_list.pop(0)
                if invert_flag:
                    if float(attr_list[attr_index]) <= threshold:
                        result.append("y\\n")
                    else:
                        result.append("n\\n")   
                else:
                    if float(attr_list[attr_index]) <= threshold:
                        result.append("n\\n")
                    else:
                        result.append("y\\n")   
                    
            

    with open(os.path.abspath(os.getcwd()) + "/NW_04_Kale_Kushal_RESULTS.csv", "w") as output_file:
        for val in result:
            output_file.write(val)

"""

    with open("NW_04_Kale_Kushal_Classifier.py", 'w') as code_file:
        code_file.write(code)

    from NW_04_Kale_Kushal_Classifier import classify_based_on_threshold
    print(invert_flag)
    classify_based_on_threshold(best_thresholds[least_no_of_mistakes.index(min(least_no_of_mistakes))], best_attr_to_split_on, invert_flag)

