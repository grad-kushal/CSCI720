from itertools import combinations
import numpy as np
import pandas as pd
import scipy


def computeCrossCorrelationCoefficient(data):

    # Let's get all the column names and create a list of it to iterate over later on
    column_names = list(data.columns.values)
    print("Column names: ", column_names)

    # Let's create a matrix of dimensions n x n where n is the number of attributes
    n = len(column_names)
    result = np.zeros(shape=(n,n))

    strongest_correlation = 0
    row_found = 'r'
    column_found = 'c'

    # Let's start populating our initial matrix with the appropriate coefficients here
    for row in range(n):
        for column in range(n):
            result[row][column] = round(scipy.stats.pearsonr(data[column_names[row]], data[column_names[column]])[0], 2)

            if column_names[row] == ' Chips' and column_names[column] == 'Cereal':
                print("Chips and cereal: ", result[row][column])

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
    result_cross_correlations = computeCrossCorrelationCoefficient(correlation_raw_data)
    print("Printing our cross correlation coeffient matrix: ")
    print(result_cross_correlations)


if __name__ == "__main__":
    main()