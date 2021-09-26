import csv
import numpy as np
from matplotlib import pyplot as plt
import scipy.optimize
# determine quality of the fit
from sklearn.metrics import r2_score



def get_producers_and_price(file):
    """ function that gets the producers and runtime from
        the prepared csv files

        :returns 2 lists the number of producers and the reached
                 prices"""
    producer_number = []
    reached_price = []

    with open (file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            if row[0] != 'x_values' and row[1] != 'y_values':
                producer_number.append(float(row[0]))
                reached_price.append(float(row[1]))


    return producer_number, reached_price


def get_producers_to_price(producer_number, reached_price):
    """ function that transforms the lists from get
        producers and price into a dictionary"""

    producer_price_dict = {}
    counter = 0
    while counter < len(producer_number):
        x_value = producer_number[counter]
        y_value = reached_price[counter]

        if x_value not in producer_price_dict.keys():

            producer_price_dict[x_value] = []
            producer_price_dict[x_value].append(y_value)

        else:
            producer_price_dict[x_value].append(y_value)
        counter += 1

    if 0.0 in producer_price_dict.keys():
        del producer_price_dict[0.0]

    return producer_price_dict



def sort_values(producer_price_dict):
    """ function that sorts the dictionary keys and data
        this is necessary for plotting the data later on"""

    sorted_price_data = []
    sorted_price_means = []
    sorted_producer_numbers = sorted(producer_price_dict.keys())

    for values in sorted_producer_numbers:
        sorted_price_data.append(producer_price_dict[values])
        sorted_price_means.append(np.mean(producer_price_dict[values]))



    return sorted_price_means, sorted_price_data, sorted_producer_numbers


#---------------------- curve fitting -----------------------------------
# defining an exponential funktion to fit the cref
def fitting_function(x,m,t,b):
    return m * np.exp(-t * x) + b


def fitting_and_plotting(sorted_producer_numbers,sorted_price_means,producer_number, reached_price):
    """ function that calculates a fitted function using the sciPy library
            :returns the plotted data and curve fitting function using matplotlib"""

    sorted_producer_numbers = np.array(sorted_producer_numbers)
    sorted_price_means = np.array(sorted_price_means)
    producer_number = np.array(producer_number)
    reached_price = np.array(reached_price)

    params, cv = scipy.optimize.curve_fit(fitting_function, sorted_producer_numbers, sorted_price_means)

    m, t, b = params

    r2_value = r2_score(sorted_price_means, fitting_function(sorted_producer_numbers, m, t, b))

    #plotting the data
    plt.scatter(producer_number, reached_price, color='deepskyblue', alpha=0.01, marker='.', edgecolors=None,
                rasterized=True)
    plt.plot(sorted_producer_numbers, sorted_price_means, color='r')
    plt.plot(sorted_producer_numbers, fitting_function(sorted_producer_numbers, m, t, b), color='black')

    # set axes label
    plt.xlabel("Anzahl an Producer-Haushalten")
    plt.ylabel("Erreichter Strompreis [ct]")

    #set title
    plt.title('Simplex: Producer-Haushalte und erreichter Strompreis')

    fig = plt.gcf()
    fig.set_size_inches(8, 5)

    plt.ylim(21, 24)
    plt.xlim(1, 16)

    print("R2", r2_value)

    print(params)

    # saving as svg graphic
    fig.savefig("producer_price_scalable.svg")
    fig.savefig("producer_price_scalable.pdf")

    plt.show()


    return 0




def main():

    file = 'producer_to_price.csv'
    producer_number, reached_price = get_producers_and_price(file)
    producer_price_dict = get_producers_to_price(producer_number, reached_price)

    sorted_price_means, sorted_price_data, sorted_producer_numbers = sort_values(producer_price_dict)
    abbildung = fitting_and_plotting(sorted_producer_numbers,sorted_price_means,producer_number, reached_price)

    print(len(reached_price))

if __name__ == '__main__':
    main()