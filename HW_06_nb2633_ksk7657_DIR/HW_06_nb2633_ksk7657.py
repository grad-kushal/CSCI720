import math
import time

import numpy as np
import pandas as pd
import scipy
from scipy.spatial.distance import pdist, squareform


def eudistance_new(v1, v2):
    distance = [(p - q) ** 2 for p, q in zip(v1, v2)]
    distance = math.sqrt(sum(distance))
    return distance


def calculate_euclidean_distance(point_1, point_2):
    # point_1 = np.delete(point_1, 0)
    # point_2 = np.delete(point_2, 0)
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


def combine_clusters(clusters, combining_clusters):
    cluster_id_new = min(combining_clusters)
    cluster_id_obsolete = max(combining_clusters)
    new_cluster_points = list()
    new_cluster_points.extend(clusters[combining_clusters[0]][0])
    new_cluster_points.extend(clusters[combining_clusters[1]][0])
    new_cluster_vector = (clusters[combining_clusters[0]][1] + clusters[combining_clusters[1]][1]) / 2
    # new_cluster_vector = np.zeros(len(clusters[0][1]))
    # for point in new_cluster_points:
    #     new_cluster_vector = new_cluster_vector + point
    # new_cluster_vector = new_cluster_vector / len(new_cluster_points)
    clusters[cluster_id_new] = (new_cluster_points, new_cluster_vector)
    # print("Removing cluster:", cluster_id_obsolete + 1)
    clusters.pop(cluster_id_obsolete)
    return cluster_id_obsolete


def calculate_distance_matrix(vals):
    new_points_list = []
    for val in vals:
        new_points_list.append(val[1])
    distances = pdist(np.array(new_points_list), metric='euclidean')
    distances = squareform(distances)
    return distances


def create_dist_dict(clusters, distances):
    result = dict()
    i = 0
    for cluster1 in clusters.values():
        j = 0
        for cluster2 in clusters.values():
            result[int(cluster1[1][0] - 1)] = {int(cluster2[1][0] - 1): distances[i][j]}
            j += 1
        i += 1
    return result


def partB(data):
    clusters = dict()
    data_without_ids = data.iloc[:, 1:]
    print(len(data))
    for i in range(1, len(data_without_ids) + 1):
        clusters[i - 1] = ([data_without_ids.iloc[i - 1]], data_without_ids.iloc[i - 1])
    # print(clusters)
    merges = []
    removed = []
    smaller_cluster_in_each_iteration = []
    while len(clusters) != 1:
        distance_min = math.inf
        for key1 in clusters.keys():
            cluster1 = clusters[key1]
            for key2 in clusters.keys():
                cluster2 = clusters[key2]
                if key1 != key2:
                    distance = eudistance_new(cluster1[1], cluster2[1])
                    if distance < distance_min:
                        distance_min = distance
                        combining_clusters = (key1, key2)
        if len(clusters) < 10:
            print("Merging:", combining_clusters[0] + 1, "and", combining_clusters[1] + 1)
            print("Prototype of cluster", min(combining_clusters) + 1, ": ")
            print("     Size:-------------", len(clusters[combining_clusters[0]][0]),
                  " + ", len(clusters[combining_clusters[1]][0]))
            np.set_printoptions(suppress=True)
            np.set_printoptions(precision=2)
            np.set_printoptions(linewidth=np.inf)
            print("     Centre of Mass:---", np.array(clusters[min(combining_clusters)][1]))
            print("Cluster Sums by Attribute:", np.sum((clusters[min(combining_clusters)][0]), axis=0))
        merges.append(combining_clusters)
        smaller_cluster_in_each_iteration.append(
            combining_clusters[0] + 1 if len(clusters[combining_clusters[0]][0]) < len(
                clusters[combining_clusters[1]][0])
            else combining_clusters[1] + 1)
        removed.append(combine_clusters(clusters, combining_clusters) + 1)

    print("________________________________________________________________________________________________________________")
    print("Last 10 smallest clusters merged:    ", smaller_cluster_in_each_iteration[-10:])
    print("Merge Order:                         ", merges)
    print("Final Cluster Size:                  ", len(clusters[0][0]))
    print("Final cluster COM:                   ", np.array(clusters[0][1]))
    # print(removed)


def partA(data):
    # Retrieving only the required columns for computing the correlations
    # Note that we are discarding the ID column in this step
    correlation_raw_data = data.iloc[:, 1:]

    # Calculating the cross correlation coefficients of all the attributes
    result_cross_correlations = compute_cross_correlation_coefficient(correlation_raw_data)

    print("Printing our cross correlation coefficient matrix: ")
    print(result_cross_correlations)


def main():
    # Call a function which will read in all the data
    # filename = 'sample.csv'
    filename = 'HW_CLUSTERING_SHOPPING_CART_v2221A.csv'
    data = readData(filename)

    # partA(data)

    print("\n-------------------------------------------------------------------------------------------------------")

    start = time.time()
    partB(data)
    end = time.time()
    print("Time: ", end - start)


if __name__ == "__main__":
    main()
