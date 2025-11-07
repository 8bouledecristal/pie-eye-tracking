import csv
from time import sleep
filename = "../data/data.csv"
i = 0
while True :
    sleep(1)
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        last_row = None
        for row in reader:
            last_row = row
    print(i, last_row[0])
    i += 1