import pandas as pd
import numpy as np
from numpy.linalg import eig
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# ------------------------------------------------------------------------------------------------------------------

def readData(filename):
    header_list = [i for i in range(1, 21)]
    data = pd.read_csv(filename, sep=',', names=header_list)
    return data


# ------------------------------------------------------------------------------------------------------------------

def computeCovarianceMatrix(data):

    # Creating a numpy array of all the lists (all the columns in our dataset)
    data_cov = np.array([data.loc[:, i] for i in range(1, len(data.iloc[0]) + 1)])

    # Here, we will be computing a (20 x 20) covariance matrix
    covariance_matrix = np.cov(data_cov, bias=True)

    return covariance_matrix


# ------------------------------------------------------------------------------------------------------------------
def normalizeValues(values):
    return values / sum(values)


# ------------------------------------------------------------------------------------------------------------------

def main():

    # We will start by reading in the data
    data = readData("HW_CLUSTERING_SHOPPING_CART_v2221A_NO_HEADER_and_no_ID_COLUMN.csv")

    # Next, let's compute the covariance matrix
    covariance_matrix = computeCovarianceMatrix(data)

    # Let's compute the eigenvectors and eigenvalues of the full covariance matrix
    eigenvalues, eigenvectors = eig(covariance_matrix)

    # I think the eigenvalues that we get here are already sorted in a descending order

    # Let's sort the eigenvalues in terms of highest to lowest absolute value
    # To do that, let's convert the np array to a list first
    eigenvalues = list(eigenvalues)
    eigenvalues.sort(reverse=True)

    # Converting our list back to an np array
    eigenvalues = np.array(eigenvalues)

    # Let's normalize the eigenvalues here
    normalised_eigenvalues = normalizeValues(eigenvalues)

    # Now, we will plot the cumulative sum of the normalized eigenvalues
    cumulative_sum = np.cumsum(normalised_eigenvalues)
    plt.plot(cumulative_sum)
    plt.title('Cumulative sum of the normalized eigenvalues')
    plt.show()

    # Let's print the first three eigenvectors
    print("\n-------------------------------------------------------------------------------------------------------")
    print("\nFirst three eigenvectors are as follows:\n")
    for i in range(3):
        print(eigenvectors[i])
        print("\n")
    print("\n-------------------------------------------------------------------------------------------------------")

    # Let's try projecting our data somehow

    # # Approach 1:
    # # Translate the data to a new reference origin
    # mu = data.mean(0)
    # # Subtract the center of mass
    # new_data = data - mu
    # # Get the first two vectors
    # eigenvectors = [eigenvectors[0], eigenvectors[1]]
    # # Normalize the vectors ( convert to a unit vector)
    # eigenvectors = normalizeValues(eigenvectors)
    # # Compute the dot product of the new data and the unit vector
    # Z = np.dot(new_data, eigenvectors.T)
    # # Plot the points on a scatter plot
    # plt.scatter(Z[:, 0], Z[:, 1])
    # plt.show()

    # Approach 2:
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

    # Let's move on to performing K-means on the data obtained above

    # Our data is stored in dot_product

    # Here, we are creating a model with 4 clusters and 1000 epochs.
    model = KMeans(n_clusters=4, n_init=1000)

    # Next, we have to train the model. Let's do that here-
    model.fit(dot_product)

    # Now, we should make predictions based on our model
    predictions = model.predict(dot_product)

    # Next, we will separate the x and y co-ordinates
    x_values = dot_product[:, 0]
    y_values = dot_product[:, 1]

    plt.scatter(x_values, y_values, c=predictions)
    plt.title('KMeans using a Package')
    plt.show()

    # Now, let's try to find the center of mass of each of the k clusters
    print("\nPrinting all k of the 2D vectors here: \n")
    cluster_centers = model.cluster_centers_
    i = 1
    for center in cluster_centers:
        print("Cluster "+str(i)+": ", end="")
        print(center)
        i = i + 1

    print("\n-------------------------------------------------------------------------------------------------------")

    # Plotting the 2-D vectors on top of the k clusters
    x_centers = cluster_centers[:, 0]
    y_centers = cluster_centers[:, 1]
    plt.scatter(x_values, y_values, c=predictions)
    plt.scatter(x_centers, y_centers, marker='o', s=60, c='k')
    plt.show()

    # Okay - what next? - Let's work on re-projection now, shall we?
    # Here, we have to multiply the center of mass of all the clusters with the first two eigenvectors

    print("--TESTT--")
    print("Eigenvectors: ")
    print(eg)
    print(eg.shape)  # (20 x 2)

    print("Cluster centers: ")
    print(cluster_centers)
    print(cluster_centers.shape)  # (4 x 2)

    # print("Printing the multiplication")
    # result = np.dot(cluster_centers, eg.T)
    #
    # for row in result:
    #     print(row)

# ------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
