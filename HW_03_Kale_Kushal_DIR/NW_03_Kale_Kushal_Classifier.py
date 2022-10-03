import os


def classify_based_on_threshold(threshold):  # new classifier content
    data = []
    data_after_classification = {1: [], 2: []}
    DIR = "/HW03__DATA__DATA__CS720__DATA/"
    path = os.path.abspath(os.getcwd()) + DIR
    NEWLINE = "\n"

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
