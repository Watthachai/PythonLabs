import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
#headers = ['Country','No. of Arrivals','Length of Stay','Per Capita Spending','Tourism Receipts']
#import data from csv file with pandas
df = pd.read_csv('GraphVisualization/src/database/tourism-receipts-from-international-tourist-arrivals_2018.csv')
pd.set_option('display.max_row', 100)
#limit data to 10 rows
df = df.head(10)
#sumtoal of No. of Arrivals
sum=0


print(sum)
print(df)
#print(df['Country'] +"    "+ df['No. of Arrivals'])
df1 = pd.DataFrame(df)
figure1 = plt.Figure(figsize=(8, 7), dpi=100)
ax1 = figure1.add_subplot(111)
graph_bar = FigureCanvasTkAgg(figure1, root)
graph_bar.get_tk_widget().place(x=250, y=200)
df1 = df1[['Country', 'Length of Stay']].groupby('Country').sum()
df1.plot(kind='bar', legend=True, ax=ax1)
ax1.set_title('Country has arrive to Thailand VS. Length of Stay')

#root.mainloop()