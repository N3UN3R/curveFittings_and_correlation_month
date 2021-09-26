import csv
import os
import numpy as np

def get_day_data(file):
    """ function that reads in the test data
        :returns a python dictionary which contains the
                 test data for each timestamp"""

    timestamps = []
    data = {}

    with open(file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            if row['timestamp'] not in timestamps:
                timestamps.append(row['timestamp'])

    for timestamp in timestamps:
        data[timestamp] = {}
        data[timestamp]['totalTradedWatts'] = []
        data[timestamp]['averagePrice'] = []
        data[timestamp]['maximumPrice'] = []
        data[timestamp]['minimumPrice'] = []
        data[timestamp]['runningTime'] = []
        data[timestamp]['numberOfProducers'] = []
        data[timestamp]['numberOfConsumers'] = []
        data[timestamp]['dataPrepTime'] = []
        data[timestamp]['usedReductions'] = []

    with open(file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            for timestamp in data.keys():
                if row['timestamp'] == timestamp:

                    data[timestamp]['totalTradedWatts'].append(float(row['totalTradedWatts']))
                    data[timestamp]['averagePrice'].append(float(row['averagePrice']))
                    data[timestamp]['maximumPrice'].append(float(row['maximumPrice']))
                    data[timestamp]['minimumPrice'].append(float(row['minimumPrice']))
                    data[timestamp]['runningTime'].append(float(row['runningTime']))

                    data[timestamp]['dataPrepTime'].append(float(row['dataPrepTime']))

                    data[timestamp]['numberOfProducers'].append(float(row['numberOfProducers']))
                    data[timestamp]['numberOfConsumers'].append(float(row['numberOfConsumers']))
                    data[timestamp]['usedReductions'].append(row['usedReductions'])

    return data


def get_day_price(data):
    """ function that receives the dictionary from
        get_day_data and returns a nested list of all
        reached average prices"""

    nestedTradingPrices = []
    for k,v in data.items():
        nestedTradingPrices.append(v['averagePrice'])

    return nestedTradingPrices


def get_day_producers(data):
    """ function that receives the dictionary from
        get_day_data and returns two lists:
        a nested list of all numbers of
        producers for each timestamp
        a list which contains the mean of the number of
        producers"""
    nestedproducer_numbers = []
    producerMean_ts = []

    for k, v in data.items():
        nestedproducer_numbers.append(v['numberOfProducers'])
        #using the numpy library to calculate the mean
        producerMean_ts.append(np.mean(v['numberOfProducers']))

    return nestedproducer_numbers, producerMean_ts


def get_day_runtimes(data):
    """ function that receives the dictionary from
        get_day_data and returns two lists:
        a nested list of all reached running times and
        a list of the mean reached running times"""

    nestedRunningTimes = []
    runTimeMean_ts = []

    for k,v in data.items():
        runTime = v['runningTime']
        nestedRunningTimes.append(runTime)
        # calculate the reached mean runtime using the numpy library
        runTimeMean_ts.append(np.mean(runTime))


    return nestedRunningTimes, runTimeMean_ts


def producer_to_price():
    """ this function creates the csv_file
        producer_to_price.csv which contains the
        number of producers matced to the reached prices"""

    dataInDir = os.listdir()
    filesToOpen = []
    for allFiles in dataInDir:
        if allFiles.startswith('07'):
            filesToOpen.append(allFiles)

    reachedPrice_days = []
    producerNumbers_days = []


    with open('producer_to_price.csv', 'w', newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['x_values','y_values'])

        for file in filesToOpen:
            data = get_day_data(file)
            day_producers, _ = get_day_producers(data)
            day_prices = get_day_price(data)

            for k, i in zip(day_producers, day_prices):
                for o, a in zip(k, i):
                    print(o, a)
                    print(type(o))
                    print(type(a))
                    row = [o, a]
                    thewriter.writerow(row)

            reachedPrice_days.append(day_prices)
            producerNumbers_days.append(day_producers)

    return 0


def producer_to_runtimes():
    """ this function creates the csv_file
        producer_to_runtimes.csv which contains the
        number of producers matced to the reached runtimes"""

    dataInDir = os.listdir()
    filesToOpen = []
    for allFiles in dataInDir:
        if allFiles.startswith('07'):
            filesToOpen.append(allFiles)

    producerNumbers_days = []
    runtime_days = []

    with open('producer_to_runtimes.csv', 'w', newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['x_values','y_values'])

        for file in filesToOpen:
            data = get_day_data(file)
            day_producers, _ = get_day_producers(data)
            day_runtimes, _ = get_day_runtimes(data)

            for k, i in zip(day_producers, day_runtimes):
                for o, a in zip(k, i):
                    print(o, a)
                    print(type(o))
                    print(type(a))
                    row = [o, a]
                    thewriter.writerow(row)

            runtime_days.append(day_runtimes)
            producerNumbers_days.append(day_producers)

    return 0


def main():

    #creating the csv-file producer_to_price.csv
    #print(producer_to_price())

    #create the csv-file producer_to_runtimes.csv
    print(producer_to_runtimes())


if __name__ == '__main__':
    main()