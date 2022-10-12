import os


def classify_based_on_threshold(threshold):  # new classifier content
    data = list()
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
                if float(attr_list[2]) <= threshold:
                    result.append("y\n")
                else:
                    result.append("n\n")   
                    
            

    with open(os.path.abspath(os.getcwd()) + "/NW_04_Kale_Kushal_RESULTS.csv", "w") as output_file:
        for val in result:
            output_file.write(val)

