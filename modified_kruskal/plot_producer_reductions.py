import csv
import numpy as np
from matplotlib import pyplot as plt
import scipy.optimize
# determine quality of the fit
from sklearn.metrics import r2_score



def get_producers_and_data(file):
    """ function that gets the producers and runtime from
        the prepared csv files

        :returns 5 lists"""
    producer_number = []
    numberOf_localDistance = []
    numberOf_konzessionsDifference = []
    numberOf_netCostDifference = []
    numberOf_pairs = []

    with open (file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            if row[0] != 'numberOfProducers':
                producer_number.append(float(row[0]))
            if row[1] != 'numberOf_localDistance':
                numberOf_localDistance.append(float(row[1]))
            if row[2] != 'numberOf_konzessionsDifference':
                numberOf_konzessionsDifference.append(float(row[2]))
            if row[3] != 'numberOf_netCostDifference':
                numberOf_netCostDifference.append(float(row[3]))
            if row[4] != 'numberOf_pairs':
                numberOf_pairs.append(float(row[4]))

    return producer_number, numberOf_localDistance, numberOf_konzessionsDifference,numberOf_netCostDifference, numberOf_pairs


def get_producers_to_data(producer_number, numberOf_localDistance,
                          numberOf_konzessionsDifference, numberOf_netCostDifference,
                          numberOf_pairs):
    """ function that transforms the lists from get
        producers and price into a dictionary"""

    producer_price_dict = {}
    counter = 0
    while counter < len(producer_number):
        producerNumber = producer_number[counter]
        localDistance = numberOf_localDistance[counter]
        konzession = numberOf_konzessionsDifference[counter]
        netCost = numberOf_netCostDifference[counter]
        pairs = numberOf_pairs[counter]


        if producerNumber not in producer_price_dict.keys():
            producer_price_dict[producerNumber] = {}
            producer_price_dict[producerNumber]['localDistance'] = []
            producer_price_dict[producerNumber]['konzession'] = []
            producer_price_dict[producerNumber]['netCost'] = []
            producer_price_dict[producerNumber]['pairs'] = []
            producer_price_dict[producerNumber]['localDistance'].append(localDistance)
            producer_price_dict[producerNumber]['konzession'].append(konzession)
            producer_price_dict[producerNumber]['netCost'].append(netCost)
            producer_price_dict[producerNumber]['pairs'].append(pairs)

        else:
            producer_price_dict[producerNumber]['localDistance'].append(localDistance)
            producer_price_dict[producerNumber]['konzession'].append(konzession)
            producer_price_dict[producerNumber]['netCost'].append(netCost)
            producer_price_dict[producerNumber]['pairs'].append(pairs)
        counter += 1

    if 0.0 in producer_price_dict.keys():
        del producer_price_dict[0.0]

    return producer_price_dict


def sort_values(producer_price_dict):
    """ function that sorts the dictionary keys and data
        this is necessary for plotting the data later on"""

    sorted_producer_numbers = sorted(producer_price_dict.keys())
    mean_localDistance = []
    mean_konzessionsDifference = []
    mean_netCostDifference = []
    mean_numberOf_pairs = []

    for values in sorted_producer_numbers:
        mean_localDistance.append(np.mean(producer_price_dict[values]['localDistance']))
        mean_konzessionsDifference.append(np.mean(producer_price_dict[values]['konzession']))
        mean_netCostDifference.append(np.mean(producer_price_dict[values]['netCost']))
        mean_numberOf_pairs.append(np.mean(producer_price_dict[values]['pairs']))

    return sorted_producer_numbers,mean_localDistance, mean_konzessionsDifference, mean_netCostDifference, mean_numberOf_pairs


def plot_producer_localDistance(sorted_producer_numbers, mean_localDistance,producer_number, numberOf_localDistance):
    """ function that plots the use of local distance
           to reduce the power price"""

    # set axes label
    plt.xlabel("Anzahl an Producer-Haushalten")
    plt.ylabel("Anzahl eingesetzter lokaler Zusammenhang")

    fig = plt.gcf()
    fig.set_size_inches(8, 5)

    # set title
    plt.title('mod. Kruskal: Producer - lokaler Zusammenhang')

    plt.plot(producer_number, numberOf_localDistance, '.', color='blue', alpha=0.1)
    plt.plot(sorted_producer_numbers, mean_localDistance)

    plt.ylim(0, 40)
    plt.xlim(1, 17)

    # saving as svg graphic
    fig.savefig("producer_local_scalable.svg")
    fig.savefig("producer_local_scalable.pdf")

    plt.show()

    return  0



def plot_producer_netCost(sorted_producer_numbers, mean_netCostDifference,producer_number, numberOf_netCostDifference):
    """ function that plots the use of net cost differences
                to reduce the power price"""

    # set axes label
    plt.xlabel("Anzahl an Producer-Haushalten")
    plt.ylabel("Anzahl eingesetzter Netzentgeltdifferenzen")

    fig = plt.gcf()
    fig.set_size_inches(8, 5)

    # set title
    plt.title('mod. Kruskal: Producer - Netzentgeltdifferenzen')

    plt.plot(producer_number, numberOf_netCostDifference, '.', color='blue', alpha=0.1)
    plt.plot(sorted_producer_numbers, mean_netCostDifference)

    plt.xlim(1, 17)
    plt.ylim(0, 90)

    # saving as svg graphic
    fig.savefig("producer_netCost_scalable.svg")
    fig.savefig("producer_netCost_scalable.pdf")

    plt.show()

    return  0


def plot_producer_KonzCost(sorted_producer_numbers, mean_konzessionsDifference,producer_number, numberOf_konzessionsDifference):
    """ function that plots the use of konzession Cost differences
                   to reduce the power price"""

    # set axes label
    plt.xlabel("number of producers")
    plt.ylabel("number of netCost Pairs")

    fig = plt.gcf()
    fig.set_size_inches(8, 5)

    # set title
    plt.title('mod. Kruskal: Producer - Konzessionsabgabendifferenzen')

    plt.plot(producer_number, numberOf_konzessionsDifference, '.', color='blue', alpha=0.1)
    plt.plot(sorted_producer_numbers, mean_konzessionsDifference)

    plt.ylim(0, 60)
    plt.xlim(1, 17)

    # saving as svg graphic
    fig.savefig("producer_konz_scalable.svg")
    fig.savefig("producer_konz_scalable.pdf")

    plt.show()

    return  0

def main():
    file = 'producer_to_reductions.csv'

    producer_number, numberOf_localDistance, numberOf_konzessionsDifference,numberOf_netCostDifference, numberOf_pairs = get_producers_and_data(file)


    producer_price_dict  = get_producers_to_data(producer_number, numberOf_localDistance, numberOf_konzessionsDifference,numberOf_netCostDifference, numberOf_pairs)

    sorted_producer_numbers,mean_localDistance, mean_konzessionsDifference, mean_netCostDifference, mean_numberOf_pairs = sort_values(producer_price_dict)

    # plots the use of local distance
   # showdata = plot_producer_localDistance(sorted_producer_numbers, mean_localDistance,producer_number, numberOf_localDistance)
    # plots the use of net Cost differences
    #showdata1 = plot_producer_netCost(sorted_producer_numbers, mean_netCostDifference,producer_number, numberOf_netCostDifference)
    # plots the use of konzessions Cost differences
    showdata2 = plot_producer_KonzCost(sorted_producer_numbers, mean_konzessionsDifference,producer_number, numberOf_konzessionsDifference)

    print(showdata2)

if __name__ == '__main__':
    main()