import pandas as pd
import numpy as np
from numpy.linalg import eig
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# ------------------------------------------------------------------------------------------------------------------

def read_data(filename):
    """
    Read the data from the file and return a pandas dataframe
    :param filename: Name of the file
    :return: dataframe
    """
    header_list = [i for i in range(1, 21)]
    data = pd.read_csv(filename, sep=',', names=header_list)
    return data


# ------------------------------------------------------------------------------------------------------------------

def compute_covariance_matrix(data):
    """
    Compute the covariance matrix of the data
    :param data: the pandas dataframe
    :return:    the covariance matrix numpy array
    """
    # Creating a numpy array of all the lists (all the columns in our dataset)
    data_cov = np.array([data.loc[:, i] for i in range(1, len(data.iloc[0]) + 1)])

    # Here, we will be computing a (20 x 20) covariance matrix
    covariance_matrix = np.cov(data_cov, bias=True)

    return covariance_matrix


# ------------------------------------------------------------------------------------------------------------------
def normalize_values(values):
    """
    Normalize the values in the list
    :param values: list to be normalized
    :return: normalized list
    """
    return values / sum(values)


# ------------------------------------------------------------------------------------------------------------------

def main():

    # Reading in the data
    data = read_data("HW_CLUSTERING_SHOPPING_CART_v2221A_NO_HEADER_and_no_ID_COLUMN.csv")

    # Computing the covariance matrix
    covariance_matrix = compute_covariance_matrix(data)

    # Computing the eigenvectors and eigenvalues of the full covariance matrix
    eigenvalues, eigenvectors = eig(covariance_matrix)

    # Let's sort the eigenvalues in descending order of their magnitude
    eigenvalues = list(eigenvalues)
    eigenvalues.sort(reverse=True)
    eigenvalues = np.array(eigenvalues)

    # Normalizing the eigenvalues here
    normalised_eigenvalues = normalize_values(eigenvalues)

    # Plotting the cumulative sum of the normalized eigenvalues
    cumulative_sum = np.cumsum(normalised_eigenvalues)
    plt.plot(cumulative_sum)
    plt.title('Cumulative sum of the normalized eigenvalues')
    plt.show()

    # Printing the first three eigenvectors
    print("\n-------------------------------------------------------------------------------------------------------")
    print("\nFirst three eigenvectors are as follows:\n")
    for i in range(3):
        print(eigenvectors[i])
        print("\n")
    print("\n-------------------------------------------------------------------------------------------------------")

    # Computing the first two principal components

    # Translate the data to a new reference origin
    mu = data.mean(0)
    # Subtract the center of mass
    new_data = data - mu
    # Compute the new covariance matrix
    new_covariance = np.cov(new_data, rowvar=False)
    # Compute the eigenvalues and eigenvectors
    ev, eg = np.linalg.eigh(new_covariance)
    # Compute the transpose of the eigenvectors
    eg = eg.T[::-1]  # eg= eg[:2].T[::-1]
    # Retrieving only the first two eigenvectors
    eg = eg[:2]
    # Computing the transpose of the two eigenvectors
    eg = eg.T
    # Computing the dot product of the data and the unit vector
    dot_product = np.dot(new_data, eg)
    # Projecting the points
    plt.scatter(dot_product[:, 0], dot_product[:, 1])
    plt.title('Scatter Plot of the Projected Points')
    plt.show()

    # Performing K-means on the data obtained above

    # Creating a model with 4 clusters and 1000 epochs.
    model = KMeans(n_clusters=4, n_init=1000)

    # Training the model
    model.fit(dot_product)

    # Making predictions based on our model
    predictions = model.predict(dot_product)

    # Separating the x and y co-ordinates of the points
    x_values = dot_product[:, 0]
    y_values = dot_product[:, 1]

    # Plotting the points
    plt.scatter(x_values, y_values, c=predictions)
    plt.title('KMeans using a Package')
    plt.show()

    # Finding the center of mass of each of the k clusters
    print("\nPrinting all k of the 2D vectors here: \n")
    cluster_centers = model.cluster_centers_
    i = 1
    for center in cluster_centers:
        print("Cluster " + str(i) + ": ", end="")
        print(center)
        i = i + 1

    print("\n-------------------------------------------------------------------------------------------------------")

    # Plotting the 2-D vectors on top of the k clusters
    x_centers = cluster_centers[:, 0]
    y_centers = cluster_centers[:, 1]
    plt.scatter(x_values, y_values, c=predictions)
    plt.scatter(x_centers, y_centers, marker='o', s=60, c='k')
    plt.show()

    # Here, we have to multiply the center of mass of all the clusters with the first two eigenvectors
    print("Re-projection")
    result = np.dot(cluster_centers, eg.T)
    for row in result:
        print(row)

    print("\n-------------------------------------------------------------------------------------------------------")


# ------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
