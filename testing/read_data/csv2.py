import csv

filename = 'tbl_traffic_bycar.csv'
tolls = []
with open(filename, encoding="utf8") as f:
    reader = csv.reader(f)
    header_row = next(reader)
    tolls = []
    brk = 0
    while True:
        toll = []
        toll_d = []
        for i in range(3):
            try:
                line = next(reader)
            except StopIteration:
                brk = 1
                break
            name = line[1]
            toll_d.append([line[2],line[3]])
        if brk == 1:
            break
        toll.append(name)
        toll += toll_d
        tolls.append(toll)
print(tolls)

