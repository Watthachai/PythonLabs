import csv
import pygal

filename = 'GraphVisualization/src/database/tourism-receipts-from-international-tourist-arrivals_2018.csv'
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
            toll_d.append(int(line[3]))
        if brk == 1:
            break
        toll.append(name)
        toll += toll_d
        tolls.append(toll)
#print(tolls)

horizontal_chart = pygal.HorizontalBar()
horizontal_chart.title = 'Number of Vehicle at Toll Gate in 2564 Chart'
for i in tolls:
    horizontal_chart.add(i[0],i[1:])
horizontal_chart.render_to_file('horizontal_line_chart.svg')

