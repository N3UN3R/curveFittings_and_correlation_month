import csv
import numpy as np
from matplotlib import pyplot as plt
import scipy.optimize
# determine quality of the fit
from sklearn.metrics import r2_score


def get_producers_and_price(file):
    """ function that gets the producers and runtime from
        the prepared csv files

        :returns a list of the number of producers
                 a list of the reached runtimes"""
    producer_number = []
    runtime = []

    with open (file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            if row[0] != 'x_values' and row[1] != 'y_values':
                producer_number.append(float(row[0]))
                runtime.append(float(row[1]))

    return producer_number, runtime


def get_producers_to_runtime(producer_number, runtime):
    """ function that transforms the lists from get
        producers and price into a dictionary"""

    producer_runtime_dict = {}
    counter = 0
    while counter < len(producer_number):
        x_value = producer_number[counter]
        y_value = runtime[counter]

        if x_value not in producer_runtime_dict.keys():

            producer_runtime_dict[x_value] = []
            producer_runtime_dict[x_value].append(y_value)

        else:
            producer_runtime_dict[x_value].append(y_value)
        counter += 1

    if 0.0 in producer_runtime_dict.keys():
        del producer_runtime_dict[0.0]

    return producer_runtime_dict


def sort_values(producer_runtime_dict):
    """ function that gets the dictionary from
        get_producers_to_runtime and sorts the dictionary.
        This is necessary for plotting the data later on
        :returns 3 lists: the sorted runtime_means, the sorted_producer_numbers
                          and the sorted runtimes"""

    sorted_runtime_data = []
    sorted_runtime_means = []
    sorted_producer_numbers = sorted(producer_runtime_dict.keys())

    for values in sorted_producer_numbers:
        sorted_runtime_data.append(producer_runtime_dict[values])
        sorted_runtime_means.append(np.mean(producer_runtime_dict[values]))

    return sorted_runtime_means, sorted_runtime_data, sorted_producer_numbers


def correlation_producers_runtime(sorted_producer_numbers,sorted_runtime_means,producer_number, runtime):
    """ function that does a correlation analysis using the sciPy library and plots the data using
            matplotlib
            :returns the plotted data"""

    sorted_producer_numbers = np.array(sorted_producer_numbers)
    sorted_runtime_means = np.array(sorted_runtime_means)
    producer_number = np.array(producer_number)
    runtime = np.array(runtime)

    fig2 = plt.figure(21, figsize=(10, 4.8))
    korrelationsmatrix = np.corrcoef(producer_number, runtime)

    # calculate needed for linear
    slope, intercept, r, p, stderr = scipy.stats.linregress(producer_number, runtime)

    print("slope")
    print(slope)
    print("intercept")
    print(intercept)
    print("r-value")
    print(r)
    print("p-value")
    print(p)
    print("r-squared:", r ** 2)

    #plotting the data
    plt.scatter(producer_number, runtime, color='deepskyblue', alpha=0.01, marker='.', edgecolors=None,
                rasterized=True)
    plt.plot(sorted_producer_numbers, sorted_runtime_means, color='r')
    plt.plot(producer_number, slope * producer_number + intercept, color='black')

    plt.title('revidierter Simplex: Producer-Haushalte und Laufzeit')

    fig = plt.gcf()
    fig.set_size_inches(8, 5)

    plt.margins(x=0)
    plt.xlabel("Anzahl an Producer-Haushalten")
    plt.ylabel("Laufzeit [s]")
    plt.ylim(0,1)
    plt.xlim(1, 16)

    # saving as svg graphic
    fig.savefig("korrelation_producer_runtime_scalable.pdf")
    fig.savefig("korrelation_producer_runtime_scalable.svg")

    plt.show()

    return producers_and_runtime


def main():

    file = 'producer_to_runtime.csv'

    producer_number, runtime = get_producers_and_price(file)
    producer_price_dict = get_producers_to_runtime(producer_number, runtime)

    sorted_runtime_means, sorted_runtime_data, sorted_producer_numbers = sort_values(producer_price_dict)
    abbildung = correlation_producers_runtime(sorted_producer_numbers, sorted_runtime_means, producer_number, runtime)

    print(abbildung)


if __name__ == '__main__':
    main()