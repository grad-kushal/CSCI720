import pandas as pd
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
            f.write(line+'\n')




