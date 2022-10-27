import pandas as pd
import math


# -------------------------------------------------------------------------------------------------------------------

def calculate_gini_index(all_files, list_of_data, threshold, flag):
    # Case 1
    if flag == 0:

        node1 = []
        node2 = []

        i = 0
        for data in list_of_data:
            if data <= threshold:
                node1.append(all_files['ClassName'][i])
            else:
                node2.append(all_files['ClassName'][i])
            i = i + 1

        classA_node1 = 0
        classB_node1 = 0

        classA_node2 = 0
        classB_node2 = 0

        for val in node1:
            if val == 'Assam':
                classA_node1 += 1
            else:
                classB_node1 += 1

        for val in node2:
            if val == 'Assam':
                classA_node2 += 1
            else:
                classB_node2 += 1

        total_node1 = classA_node1 + classB_node1
        total_node2 = classA_node2 + classB_node2

        total = total_node1 + total_node2

        # Compute gini here
        if total_node1 != 0:
            gini_node1 = 1 - (((classA_node1 / total_node1) ** 2) + ((classB_node1 / total_node1) ** 2))
        else:
            gini_node1 = 1

        if total_node2 != 0:
            gini_node2 = 1 - (((classA_node2 / total_node2) ** 2) + ((classB_node2 / total_node2) ** 2))
        else:
            gini_node2 = 1

        weighted_gini_case1 = ((total_node1 / total) * gini_node1) + ((total_node2 / total) * gini_node2)

        return weighted_gini_case1

    else:

        i = 0
        node1 = []
        node2 = []

        for data in list_of_data:

            if data <= threshold:
                node2.append(all_files['ClassName'][i])
            else:
                node1.append(all_files['ClassName'][i])
            i = i + 1

        classA_node1 = 0
        classB_node1 = 0

        classA_node2 = 0
        classB_node2 = 0

        for val in node1:
            if val == 'Assam':
                classA_node1 += 1
            else:
                classB_node1 += 1

        for val in node2:
            if val == 'Assam':
                classA_node2 += 1
            else:
                classB_node2 += 1

        total_node1 = classA_node1 + classB_node1
        total_node2 = classA_node2 + classB_node2

        total = total_node1 + total_node2

        # Compute weighted gini index here
        if total_node1 != 0:
            gini_node1 = 1 - (((classA_node1 / total_node1) ** 2) + ((classB_node1 / total_node1) ** 2))
        else:
            gini_node1 = 1

        if total_node2 != 0:
            gini_node2 = 1 - (((classA_node2 / total_node2) ** 2) + ((classB_node2 / total_node2) ** 2))
        else:
            gini_node2 = 1

        weighted_gini_case2 = ((total_node1 / total) * gini_node1) + ((total_node2 / total) * gini_node2)
        return weighted_gini_case2


# -------------------------------------------------------------------------------------------------------------------

def unique_values(list_of_data):
    distinct_list = []
    for item in list_of_data:
        if item not in distinct_list:
            # Append the speed only if it is not already present in the distinct_list
            distinct_list.append(item)
    return distinct_list


# -------------------------------------------------------------------------------------------------------------------

def customized_rounding(value, rounding_factor):
    if rounding_factor == 2:

        if value % 2 == 1:
            return value - 1
        round_value_floor = math.floor(value)
        round_value_ceil = math.ceil(value)
        if round_value_floor % 2 == 0:
            return round_value_floor
        if round_value_ceil % 2 == 0:  # Could be replaced by else but wanted to be sure :P
            return round_value_ceil

    else:

        for i in range(1, rounding_factor + 1):
            test = value - i
            test_floor = math.floor(test)
            test_ceil = math.ceil(test)
            if test_floor % rounding_factor == 0:
                test1 = test_floor
                break
            if test_ceil % rounding_factor == 0:
                test1 = test_ceil
                break
        for i in range(1, rounding_factor + 1):
            test = value + i
            test_floor = math.floor(test)
            test_ceil = math.ceil(test)
            if test_floor % rounding_factor == 0:
                test2 = test_floor
                break
            if test_ceil % rounding_factor == 0:
                test2 = test_ceil
                break
        if abs(test1 - value) < abs(test2 - value):
            return test1
        else:
            return test2


# -------------------------------------------------------------------------------------------------------------------
def recursiveSplit(all_files, attributes_list, attributes_selected, depth):
    # Stopping condition
    if depth > 23:
        attributes_selected.append("null")
        print("---------MAXIMUM DEPTH REACHED---------")
        return

    # Setting initial values to the three variables
    ultimate_best_threshold = 0
    ultimate_best_attribute = 'dummy'
    ultimate_least_gini_index = math.inf

    # Flag = 0 means more of a feature corresponds to being classified as Assam
    # Flag = 1 means less of a feature corresponds to being classified as Bhutan
    flag = 0

    # Let's try to find the best threshold for attribute 1 -> maybe RoundedAge

    for attribute in attributes_list:

        # Getting the unique attribute values for the attribute column chosen
        unique_thresholds = unique_values(all_files[attribute])

        # Sorting the unique attribute values for the attribute column chosen
        unique_thresholds.sort()

        # Setting the default values
        least_gini_index = math.inf
        best_threshold = 0

        # Iterating over every threshold value in the unique_threshold list obtained above
        for threshold in unique_thresholds:

            # Dealing with case 1
            gini_index1 = calculate_gini_index(all_files, all_files[attribute], threshold, 0)
            gini_index2 = calculate_gini_index(all_files, all_files[attribute], threshold, 1)

            if gini_index1 <= gini_index2:
                gini_index = gini_index1
                flag = 0
            else:
                gini_index = gini_index2
                flag = 1

            if gini_index <= least_gini_index:
                least_gini_index = gini_index
                best_threshold = threshold

        # print("Attribute: ", attribute)
        # print("Best threshold is: ", best_threshold)
        # print("Best gini index is: ", least_gini_index)
        # print("-------------------------------------")

        if least_gini_index <= ultimate_least_gini_index:
            ultimate_least_gini_index = least_gini_index
            ultimate_best_threshold = best_threshold
            ultimate_best_attribute = attribute

    print("----------------------------------------")

    print("Ultimate best attribute: ", ultimate_best_attribute)
    attributes_selected.append(ultimate_best_attribute)
    print("Ultimate least gini index: ", ultimate_least_gini_index)
    print("Ultimate best threshold value: ", ultimate_best_threshold)

    print("----------------------------------------")

    node1 = list()
    node2 = list()

    if flag == 0:
        node1.append(all_files[all_files[ultimate_best_attribute] <= ultimate_best_threshold])
        node2.append(all_files[all_files[ultimate_best_attribute] > ultimate_best_threshold])

    else:
        node1.append(all_files[all_files[ultimate_best_attribute] > ultimate_best_threshold])
        node2.append(all_files[all_files[ultimate_best_attribute] <= ultimate_best_threshold])

    node1_dataFrame = pd.concat(node1, axis=0, ignore_index=True)
    node2_dataFrame = pd.concat(node2, axis=0, ignore_index=True)

    # Stopping condition 1
    if len(node1_dataFrame) < 23 or len(node2_dataFrame) < 23:
        print("------MINIMUM NODE COUNT REACHED------")
        attributes_selected.append("null")
        return

    # print('Printing nodes: ')
    # print("Node 1: ")
    # print(node1_dataFrame)
    # print("Node 2: ")
    # print(node2_dataFrame)
    #
    # print("Printing node counts: ")
    # print("Count of node 1: ", len(node1_dataFrame))
    # print("Count of node 2: ", len(node2_dataFrame))

    if len(node1_dataFrame) < 23 or len(node2_dataFrame) < 23:
        print("------MINIMUM NODE COUNT REACHED------")
        attributes_selected.append("null")
        return

    # print('Printing nodes: ')
    # print("Node 1: ")
    # print(node1_dataFrame)
    # print("Node 2: ")
    # print(node2_dataFrame)
    #
    # print("Printing node counts: ")
    # print("Count of node 1: ", len(node1_dataFrame))
    # print("Count of node 2: ", len(node2_dataFrame))

    # For node 1
    print("ATTRIBUTES SELECTED: ", attributes_selected)

    # Checking for node 1
    assam_count = 0
    for i in range(len(node1_dataFrame)):
        if node1_dataFrame['ClassName'][i] == 'Assam':
            assam_count = assam_count + 1

    bhutan_count = len(node1_dataFrame) - assam_count

    total = assam_count + bhutan_count

    assam_percent = (assam_count / total) * 100
    bhutan_percent = (bhutan_count / total) * 100

    if assam_percent > 89 or bhutan_percent > 89:
        print("------MAXIMUM PERCENT REACHED------")
        attributes_selected.append("null")
        return

    else:
        print("$$ Performing left split for ", ultimate_best_attribute)
        print("Assam percent: ", assam_percent)
        print("Bhutan percent: ", bhutan_percent)
        recursiveSplit(node1_dataFrame, attributes_list, attributes_selected, depth + 1)

    # Checking for node 2
    assam_count = 0
    for i in range(len(node2_dataFrame)):
        if node2_dataFrame['ClassName'][i] == 'Assam':
            assam_count = assam_count + 1

    bhutan_count = len(node2_dataFrame) - assam_count

    total = assam_count + bhutan_count

    assam_percent = (assam_count / total) * 100
    bhutan_percent = (bhutan_count / total) * 100

    if assam_percent > 89 or bhutan_percent > 89:
        print("------MAXIMUM PERCENT REACHED------")
        attributes_selected.append("null")
        return

    else:
        print("$$ Performing right split for ", ultimate_best_attribute)
        print("Assam percent: ", assam_percent)
        print("Bhutan percent: ", bhutan_percent)
        recursiveSplit(node2_dataFrame, attributes_list, attributes_selected, depth + 1)


# -------------------------------------------------------------------------------------------------------------------


def main():
    # Step 1: Read the entire data into a pandas data frame
    filepath = "Abominable_Data_HW_LABELED_TRAINING_DATA__v770_2221.csv"
    df = pd.read_csv(filepath)

    # Step 2: Create a attributes list to iterate over later on
    attributes = ['Age', 'Ht', 'TailLn', 'HairLn', 'BangLn', 'Reach', 'EarLobes', 'ClassName', 'ClassID']

    # -------------------------------------------------------------------------------------------------------------------
    # Let's work on calculating the ape factor here
    # Ape factor = Reach / Ht

    # Let's begin by creating an empty list
    ape_factor_list = []

    for i in range(len(df)):
        ape_factor_value = df['Reach'][i] - df['Ht'][i]
        ape_factor_list.append(ape_factor_value)

    # Let's add this derived attribute to our main dataframe
    df['ApeFactor'] = ape_factor_list

    # -------------------------------------------------------------------------------------------------------------------

    # Let's round all the attributes here
    # We will begin by creating empty lists
    rounded_age = []
    rounded_tail_ln = []
    rounded_hair_ln = []
    rounded_bang_ln = []
    rounded_reach = []
    rounded_earlobes = []
    rounded_ht = []
    rounded_ape_factor = []

    for i in range(len(df)):
        rounded_age.append(customized_rounding(df['Age'][i], 2))
        rounded_ht.append(customized_rounding(df['Ht'][i], 4))
        rounded_tail_ln.append(customized_rounding(df['TailLn'][i], 2))
        rounded_hair_ln.append(customized_rounding(df['HairLn'][i], 2))
        rounded_bang_ln.append(customized_rounding(df['BangLn'][i], 2))
        rounded_reach.append(customized_rounding(df['Reach'][i], 2))
        # We will be treating EarLobes differently since rounding these values (which are only 0s and 1s)
        # will result in rounding off to 0s and NaNs respectively. To surpass this issue,
        # we will be rounding 1s to 2s here and 0s will be retained.
        if df['EarLobes'][i] == 1:
            rounded_earlobes.append(2)
        else:
            rounded_earlobes.append(0)
        rounded_ape_factor.append(customized_rounding(df['ApeFactor'][i], 2))

    attributes_list = ['RoundedAge', 'RoundedHt', 'RoundedTailLn', 'RoundedHairLn', 'RoundedBangLn', 'RoundedReach',
                       'RoundedEarLobes', 'RoundedApeFactor']

    all_files = pd.DataFrame()
    all_files['RoundedAge'] = rounded_age
    all_files['RoundedHt'] = rounded_ht
    all_files['RoundedTailLn'] = rounded_tail_ln
    all_files['RoundedHairLn'] = rounded_hair_ln
    all_files['RoundedBangLn'] = rounded_bang_ln
    all_files['RoundedReach'] = rounded_reach
    all_files['RoundedEarLobes'] = rounded_earlobes
    all_files['RoundedApeFactor'] = rounded_ape_factor
    all_files['ClassName'] = df['ClassName']

    # Setting initial values to the three variables
    ultimate_best_threshold = 0
    ultimate_best_attribute = 'dummy'
    ultimate_least_gini_index = math.inf
    attributes_selected = []

    # Flag = 0 means more of a feature corresponds to being classified as Assam
    # Flag = 1 means less of a feature corresponds to being classified as Bhutan
    flag = 0

    # Let's try to find the best threshold for attribute 1 -> maybe RoundedAge

    for attribute in attributes_list:

        # Getting the unique attribute values for the attribute column chosen
        unique_thresholds = unique_values(all_files[attribute])

        # Sorting the unique attribute values for the attribute column chosen
        unique_thresholds.sort()

        # Setting the default values
        least_gini_index = math.inf
        best_threshold = 0

        # Iterating over every threshold value in the unique_threshold list obtained above
        for threshold in unique_thresholds:

            # Dealing with case 1
            gini_index1 = calculate_gini_index(all_files, all_files[attribute], threshold, 0)
            gini_index2 = calculate_gini_index(all_files, all_files[attribute], threshold, 1)

            if gini_index1 <= gini_index2:
                gini_index = gini_index1
                flag = 0
            else:
                gini_index = gini_index2
                flag = 1

            if gini_index <= least_gini_index:
                least_gini_index = gini_index
                best_threshold = threshold

        # print("Attribute: ", attribute)
        # print("Best threshold is: ", best_threshold)
        # print("Best gini index is: ", least_gini_index)
        # print("-------------------------------------")

        if least_gini_index <= ultimate_least_gini_index:
            ultimate_least_gini_index = least_gini_index
            ultimate_best_threshold = best_threshold
            ultimate_best_attribute = attribute

    print("----------------------------------------")

    print("Ultimate best attribute: ", ultimate_best_attribute)
    attributes_selected.append(ultimate_best_attribute)
    print("Ultimate least gini index: ", ultimate_least_gini_index)
    print("Ultimate best threshold value: ", ultimate_best_threshold)
    print("----------------------------------------")

    node1 = list()
    node2 = list()

    if flag == 0:
        node1.append(all_files[all_files[ultimate_best_attribute] <= ultimate_best_threshold])
        node2.append(all_files[all_files[ultimate_best_attribute] > ultimate_best_threshold])

    else:
        node1.append(all_files[all_files[ultimate_best_attribute] > ultimate_best_threshold])
        node2.append(all_files[all_files[ultimate_best_attribute] <= ultimate_best_threshold])

    node1_dataFrame = pd.concat(node1, axis=0, ignore_index=True)
    node2_dataFrame = pd.concat(node2, axis=0, ignore_index=True)

    # Stopping condition 1
    if len(node1_dataFrame) < 23 or len(node2_dataFrame) < 23:
        print("STOP THE COUNT")

    # print('Printing nodes: ')
    # print("Node 1: ")
    # print(node1_dataFrame)
    # print("Node 2: ")
    # print(node2_dataFrame)
    #
    # print("Printing node counts: ")
    # print("Count of node 1: ", len(node1_dataFrame))
    # print("Count of node 2: ", len(node2_dataFrame))

    # Checking for node 1
    assam_count = 0

    for i in range(len(node1_dataFrame)):
        if node1_dataFrame['ClassName'][i] == 'Assam':
            assam_count = assam_count + 1

    bhutan_count = len(node1_dataFrame) - assam_count

    total = assam_count + bhutan_count

    assam_percent = (assam_count / total) * 100
    bhutan_percent = (bhutan_count / total) * 100

    print("Assam percent: ", assam_percent)
    print("Bhutan percent: ", bhutan_percent)

    if assam_percent > 89 or bhutan_percent > 89:
        print('Stopping condition b!!!')
        return

    else:
        print("$$ Performing left split for ", ultimate_best_attribute)
        recursiveSplit(node1_dataFrame, attributes_list, attributes_selected, 2)

    # Checking for node 2
    assam_count = 0

    for i in range(len(node2_dataFrame)):
        if node2_dataFrame['ClassName'][i] == 'Assam':
            assam_count = assam_count + 1

    bhutan_count = len(node2_dataFrame) - assam_count

    total = assam_count + bhutan_count

    assam_percent = (assam_count / total) * 100
    bhutan_percent = (bhutan_count / total) * 100

    print("Assam percent: ", assam_percent)
    print("Bhutan percent: ", bhutan_percent)

    if assam_percent > 89 or bhutan_percent > 89:
        print('Stopping condition b!!!')
        return

    else:
        print("$$ Performing right split for ", ultimate_best_attribute)
        recursiveSplit(node2_dataFrame, attributes_list, attributes_selected, 2)

    print("Attributes selected: ", attributes_selected)

    # Generating the classifier file

    c = '''import pandas as pd
import csv
import math


def customized_rounding(value, rounding_factor):

    if rounding_factor == 2:
        if value % 2 == 1:
            return value - 1
        round_value_floor = math.floor(value)
        round_value_ceil = math.ceil(value)
        if round_value_floor % 2 == 0:
            return round_value_floor
        if round_value_ceil % 2 == 0:  # Could be replaced by else but wanted to be sure :P
            return round_value_ceil

    else:

        for index in range(1, rounding_factor + 1):
            test = value - index
            test_floor = math.floor(test)
            test_ceil = math.ceil(test)
            if test_floor % rounding_factor == 0:
                test1 = test_floor
                break
            if test_ceil % rounding_factor == 0:
                test1 = test_ceil
                break
        for index in range(1, rounding_factor + 1):
            test = value + index
            test_floor = math.floor(test)
            test_ceil = math.ceil(test)
            if test_floor % rounding_factor == 0:
                test2 = test_floor
                break
            if test_ceil % rounding_factor == 0:
                test2 = test_ceil
                break
        if abs(test1 - value) < abs(test2 - value):
            return test1
        else:
            return test2


def classifier_model():

    # Importing the validation data
    df_validate_this_data = list()
    df_validate_this_data.append(pd.read_csv('Abominable_VALIDATION_Data_FOR_STUDENTS_v770_2221.csv'))
    # Converting the validation data into a data frame and concatenating all of the data into a single data frame
    df = pd.concat(df_validate_this_data, axis=0, ignore_index=True)

    # main_data = list()
    #
    # for i in range(len(df)):
    #     if df['ClassID'][i] == 1:
    #         main_data.append('+1')
    #     else:
    #         main_data.append('-1')

    ape_factor_list = []

    for i in range(len(df)):
        ape_factor_value = df['Reach'][i] - df['Ht'][i]
        ape_factor_list.append(ape_factor_value)

    # Let's add this derived attribute to our main dataframe
    df['ApeFactor'] = ape_factor_list
    rounded_age = []
    rounded_tail_ln = []
    rounded_hair_ln = []
    rounded_bang_ln = []
    rounded_reach = []
    rounded_earlobes = []
    rounded_ht = []
    rounded_ape_factor = []

    for i in range(len(df)):
        rounded_age.append(customized_rounding(df['Age'][i], 2))
        rounded_ht.append(customized_rounding(df['Ht'][i], 4))
        rounded_tail_ln.append(customized_rounding(df['TailLn'][i], 2))
        rounded_hair_ln.append(customized_rounding(df['HairLn'][i], 2))
        rounded_bang_ln.append(customized_rounding(df['BangLn'][i], 2))
        rounded_reach.append(customized_rounding(df['Reach'][i], 2))
        # We will be treating EarLobes differently since rounding these values (which are only 0s and 1s)
        # will result in rounding off to 0s and NaNs respectively. To surpass this issue,
        # we will be rounding 1s to 2s here and 0s will be retained.
        if df['EarLobes'][i] == 1:
            rounded_earlobes.append(2)
        else:
            rounded_earlobes.append(0)
        rounded_ape_factor.append(customized_rounding(df['ApeFactor'][i], 2))

    all_files = pd.DataFrame()
    all_files['RoundedAge'] = rounded_age
    all_files['RoundedHt'] = rounded_ht
    all_files['RoundedTailLn'] = rounded_tail_ln
    all_files['RoundedHairLn'] = rounded_hair_ln
    all_files['RoundedBangLn'] = rounded_bang_ln
    all_files['RoundedReach'] = rounded_reach
    all_files['RoundedEarLobes'] = rounded_earlobes
    all_files['RoundedApeFactor'] = rounded_ape_factor

    class_list = list()

    # Creating the if else ladder:
    for i in range(len(all_files)):
        if all_files['RoundedApeFactor'][i] <= 4:
            if all_files['RoundedHairLn'][i] <= 10:
                print('-1')
                class_list.append('-1')
            else:
                print('+1')
                class_list.append('+1')
        else:
            if all_files['RoundedHt'][i] <= 172:
                if all_files['RoundedBangLn'][i] <= 4:
                    if all_files['RoundedApeFactor'][i] <= 6:
                        if all_files['RoundedHairLn'][i] <= 8:
                            if all_files['RoundedReach'][i] <= 134:
                                print('-1')
                                class_list.append('-1')
                            else:
                                print('+1')
                                class_list.append('+1')
                        else:
                            if all_files['RoundedHairLn'][i] <= 10:
                                if all_files['RoundedReach'][i] <= 138:
                                    if all_files['RoundedTailLn'][i] <= 8:
                                        print('-1')
                                        class_list.append('-1')
                                    else:
                                        print('+1')
                                        class_list.append('+1')
                                else:
                                    if all_files['RoundedTailLn'][i] <= 2:
                                        print('-1')
                                        class_list.append('-1')
                                    else:
                                        print('+1')
                                        class_list.append('+1')
                            else:
                                print('+1')
                                class_list.append('+1')
                    else:
                        print('+1')
                        class_list.append('+1')
                else:
                    print('+1')
                    class_list.append('+1')
            else:
                if all_files['RoundedApeFactor'][i] <= 6:
                    print('-1')
                    class_list.append('-1')
                else:
                    print('+1')
                    class_list.append('+1')

    # print("Printing class list: ", class_list)
    #
    # print(len(class_list))
    #
    # print("Printing main data: ", main_data)
    #
    # print(len(main_data))

    # Test confusion matrix:
    # correctly_classified_assam = 0
    # incorrectly_classified_assam = 0
    #
    # correctly_classified_bhutan = 0
    # incorrectly_classified_bhutan = 0

    # for i in range(len(main_data)):
    #
    #     if main_data[i] == '+1':
    #
    #         if class_list[i] == '+1':
    #             correctly_classified_assam += 1
    #         else:
    #             incorrectly_classified_assam += 1
    #     else:
    #         if class_list[i] == '-1':
    #             correctly_classified_bhutan += 1
    #         else:
    #             incorrectly_classified_bhutan += 1

    # Printing things out to fill the confusion matrix

    # print(correctly_classified_assam)
    # print(incorrectly_classified_assam)
    #
    # print("------")
    #
    # print(correctly_classified_bhutan)
    # print(incorrectly_classified_bhutan)

    # Writing into the output result csv file
    print(class_list)

    with open('HW05_EMail1_EMail2_MyClassifications.csv', 'w') as f:

        # Creating the csv writer file
        for line in class_list:
            f.write(line+'\\n')




'''
    # Creating the output trained classifier file
    with open('HW_05_nb2633_ksk7657_Classifier.py', 'w') as file_name:
        file_name.write(c)

    # Importing the above created trained classifier file
    from HW_05_nb2633_ksk7657_Classifier import classifier_model

    classifier_model()





# -------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
