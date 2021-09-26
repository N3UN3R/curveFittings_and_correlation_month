import csv
import os

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
        data[timestamp]['totalCosts'] = []
        data[timestamp]['totalTradedWatts'] = []

    with open(file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            for timestamp in data.keys():
                if row['timestamp'] == timestamp:
                    data[timestamp]['totalCosts'].append(row['totalCosts'])
                    data[timestamp]['totalTradedWatts'].append(row['totalTradedWatts'])

    return data


def get_saved_amouts(data):
    """ function that calculates the savings for all traded power
           :returns the saved amount and the kilowatts over a day
                    as lists"""

    saved_amount = []
    kilowatts_over_day = []

    for k,v in data.items():
        # calculate costs for a trading price of 30 ct/kWh
        regularCosts = float(v['totalTradedWatts'][0])*30
        # calculate costs for reached prices
        communityCosts = float(v['totalCosts'][0])
        # calculate savings
        safed = regularCosts - communityCosts
        saved_amount.append(safed)
        kilowatts_over_day.append(float(v['totalTradedWatts'][0]))

    return saved_amount, kilowatts_over_day



def main():
    dataInDir = os.listdir()
    filesToOpen = []
    for allFiles in dataInDir:
        if allFiles.startswith('07'):
            filesToOpen.append(allFiles)

    month_saved = []
    kilowatts_month = []

    for file in filesToOpen:
        print(file)
        data = get_day_data(file)
        saved_amount, kilowatts_over_day = get_saved_amouts(data)

        month_saved.append(sum(saved_amount))
        kilowatts_month.append(sum(kilowatts_over_day))

    print(sum(month_saved)/100)
    print(sum(kilowatts_month))

if __name__ == '__main__':
    main()