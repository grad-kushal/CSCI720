from itertools import combinations
import numpy as np
import pandas as pd
import scipy


def calculate_euclidean_distance(point_1, point_2):
    return np.sqrt(np.sum(np.square(point_2 - point_1)))


def compute_cross_correlation_coefficient(data):
    """
    This function generates an n x n matrix with all the cross correlational coefficient values in it.
    It also computes the answers to the questions from Part A of the homework.
    :param data: This data frame has only the attributes which are necessary
    for generating the cross correlational co-efficient values
    :return: We will be returning the computed Matrix from this function
    """

    print("\n-------------------------------------------------------------------------------------------------------")

    # Let's get all the column names and create a list of it to iterate over later on
    column_names = list(data.columns.values)
    print("\nColumn names: ", column_names)

    print("\n-------------------------------------------------------------------------------------------------------")

    print("\nLet's answer questions from Part A here: ")

    # Let's create a matrix of dimensions n x n where n is the number of attributes
    n = len(column_names)
    result = np.zeros(shape=(n, n))

    strongest_correlation = 0
    fish_strongly_related_with = 0
    fish_attribute = 'f'

    veggies_value = 0
    veggies_attribute = 'v'

    row_found = 'r'
    column_found = 'c'

    # Let's start populating our initial matrix with the appropriate coefficients here
    for row in range(n):
        for column in range(n):

            result[row][column] = round(scipy.stats.pearsonr(data[column_names[row]], data[column_names[column]])[0], 2)

            if row != column and abs(result[row][column]) >= strongest_correlation:
                strongest_correlation = abs(result[row][column])
                row_found = column_names[row]
                column_found = column_names[column]

            if column_names[row] == ' Chips' and column_names[column] == 'Cereal':
                print("\n(b) Cross correlation coefficient of Chips and Cereal: ", result[row][column])

            if column_names[row] == '  Fish' and column_names[column] != '  Fish' and \
                    result[row][column] >= fish_strongly_related_with:
                fish_strongly_related_with = result[row][column]
                fish_attribute = column_names[column]

            if column_names[row] == 'Vegges' and column_names[column] != 'Vegges' and \
                    result[row][column] >= veggies_value:
                veggies_value = result[row][column]
                veggies_attribute = column_names[column]

            if column_names[row] == '  Milk' and column_names[column] == 'Cereal':
                print("\n(e) Milk and Cereal have a co-efficient value of " + str(result[row][column]))

    print(
        "\n(a) Most strongly cross-correlated attributes: " + row_found + " and " + column_found + " with a co-efficient of " + str(
            strongest_correlation))

    print("\n(c) Fish is most strongly related with " + fish_attribute + " with a co-efficient value of "
          + str(fish_strongly_related_with))

    print("\n(d) Veggies are most strongly cross-correlated with " + veggies_attribute +
          " with a co-efficient value of " + str(veggies_value))

    print("\n-------------------------------------------------------------------------------------------------------")

    return result


def readData(filename):
    """
    This function is responsible for reading in the data into a pandas data frame
    :param filename: Path of the file which needs to be read
    :return: returns data which is a pandas data frame object
    """
    return pd.read_csv(filename)


def main():
    # Call a function which will read in all of the data
    filename = 'HW_CLUSTERING_SHOPPING_CART_v2221A.csv'
    data = readData(filename)

    # Retrieving only the required columns for computing the correlations
    # Note that we are discarding the ID column in this step
    correlation_raw_data = data.iloc[:, 1:]

    # Calculating the cross correlation coefficients of all the attributes
    result_cross_correlations = compute_cross_correlation_coefficient(correlation_raw_data)

    print("Printing our cross correlation coeffient matrix: ")
    print(result_cross_correlations)

    print("\n-------------------------------------------------------------------------------------------------------")


if __name__ == "__main__":
    main()
