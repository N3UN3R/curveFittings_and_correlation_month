import csv
import os
import numpy as np
from matplotlib import pyplot as plt
import ast


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


def write_daydata_to_csv(data):
    """ function that creates the csv-file
            producer_to_reductions.csv which contains
            the number of producers matched to the used reductions"""

    with open('producer_to_reductions.csv', 'a', newline='') as f:
        thewriter = csv.writer(f)

        for k, v in data.items():
            #just return the first entry as the number of producers is always the same
            numberOfProducers = v['numberOfProducers'][0]

            for i in v['usedReductions']:
                temp_usedReductions = ast.literal_eval(i)
                temp = []
                temp.append(temp_usedReductions)

            usedReductions = temp[0]

            if isinstance(usedReductions, dict):

                numberOf_localDistance = usedReductions['lokalDistance']
                numberOf_netCostDifference = usedReductions['netCostDifference']
                numberOf_konzessionsDifference = usedReductions['konzessionsDifference']
                numberOf_pairs = usedReductions['numberOfPairs']

                row = [numberOfProducers, numberOf_localDistance, numberOf_konzessionsDifference,numberOf_netCostDifference,numberOf_pairs]

                thewriter.writerow(row)

    return 0


def main():

    with open('producer_to_reductions.csv', 'w', newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['numberOfProducers','numberOf_localDistance','numberOf_konzessionsDifference',
                            'numberOf_netCostDifference','numberOf_pairs'])

    dataInDir = os.listdir()
    filesToOpen = []
    for allFiles in dataInDir:
        if allFiles.startswith('07'):
            filesToOpen.append(allFiles)

    for file in filesToOpen:
        print(file)
        data = get_day_data(file)
        write_daydata_to_csv(data)

if __name__ == '__main__':
    main()