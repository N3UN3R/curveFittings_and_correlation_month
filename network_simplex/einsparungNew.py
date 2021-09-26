import csv

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



def main():
    data = get_day_data('07_01.csv')

    safed_amount = []
    kilowatts_over_day = []

    for k,v in data.items():
        # calculate costs for a trading price of 30 ct/kWh
        regularCosts = float(v['totalTradedWatts'][0])*30
        # calculate costs for reached prices
        communityCosts = float(v['totalCosts'][0])
        # calculated savings
        safed = regularCosts - communityCosts
        safed_amount.append(safed)
        kilowatts_over_day.append(float(v['totalTradedWatts'][0]))

    print("Die Einsparung des Algorithmus beträgt für den Tag")
    print(sum(safed_amount)/100)
    print("Euro")
    print("Insgesamt wurden innerhalb dieses Tages")
    print(sum(kilowatts_over_day))
    print("Kilowattstunden Strom gehandelt")

if __name__ == '__main__':
    main()