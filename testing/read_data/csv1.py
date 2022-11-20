import csv

#filename = 'testing/read_data/tbl_traffic_bycar.csv'
filename = 'GraphVisualization/src/database/tourism-receipts-from-international-tourist-arrivals_2018.csv'
with open(filename, encoding="utf8") as f:
    reader = csv.reader(f)
    header_row = next(reader)
    for index, column_header in enumerate(header_row):
        print(index, column_header)


