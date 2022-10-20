import os


def read_data(file_path):
    data_point_list = []
    with open(file_path, "r") as file_object:  # open file
        for line in file_object:
            if not line.startswith("Age"):  # headers need to be ignored
                



if __name__ == '__main__':
    TRAINING_DATA_FILE = "/Abominable_Data_HW_LABELED_TRAINING_DATA__v770_2221.csv"
    path = os.path.abspath(os.getcwd())
    training_data = read_data(path + TRAINING_DATA_FILE)