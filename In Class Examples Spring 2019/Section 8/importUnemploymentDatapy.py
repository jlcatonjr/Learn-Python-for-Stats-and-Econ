import csv
with open("unemploymentData.csv", "rb") as csvfile:
    data = csv.DictReader(csvfile)#, delimiter=',', quotechar='|')
    for row in data:
        print(row)