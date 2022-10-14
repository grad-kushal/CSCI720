import os


def classify_based_on_threshold(threshold, attr_index, invert_flag):  # new classifier content
    data = list()
    print("Threshold provided to the classifier: 	" + str(threshold))
    brightness_classification_map = {'y\n': [], 'n\n': []}  # dictionary to map speeds with intent
    weight_classification_map = {'y\n': [], 'n\n': []}
    precip_classification_map = {'y\n': [], 'n\n': []}
    lanechanges_classification_map = {'y\n': [], 'n\n': []}
    speed_classification_map = {'y\n': [], 'n\n': []}
    data.append(brightness_classification_map)
    data.append(weight_classification_map)
    data.append(precip_classification_map)
    data.append(lanechanges_classification_map)
    data.append(speed_classification_map)
    
    data_after_classification = {'y\n': [], 'n\n': []}
    DIR = "/CS_720_Data_for_HW04/"
    path = os.path.abspath(os.getcwd()) + DIR
    NEWLINE = "\n"
    result = []

    with open(path + "Validation_33.csv") as validation_file:
        for line in validation_file:
            if not line.startswith("RecID"):
                attr_list = line.split(',')
                attr_list.pop(0)
                if invert_flag:
                    if float(attr_list[attr_index]) <= threshold:
                        result.append("y\n")
                    else:
                        result.append("n\n")   
                else:
                    if float(attr_list[attr_index]) <= threshold:
                        result.append("n\n")
                    else:
                        result.append("y\n")   
                    
            

    with open(os.path.abspath(os.getcwd()) + "/NW_04_Kale_Kushal_RESULTS.csv", "w") as output_file:
        for val in result:
            output_file.write(val)

