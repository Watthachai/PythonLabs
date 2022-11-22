from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import customtkinter #TODO: ผมมีส่วนเสริมช่วยให้โปรแกรมสวยขึ้นถ้ายังไม่มีกรุณาติดตั้งก่อนนะครับด้วย pip install customtkinter 
from PIL import Image, ImageTk #TODO: อันนี้เป็นตัวช่วยให้โปรแกรมแสดงรูปภาพได้นะครับ ถ้ายังไม่มีกรุณาติดตั้งก่อนนะครับด้วย pip install pillow
import pandas as pd #TODO: ถ้ายังไม่มีให้ pip install pandas นะครับ
import matplotlib.pyplot as plt #TODO: ถ้ายังไม่มีให้ pip install matplotlib นะครับ
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import plotly.express as px #TODO: ถ้ายังไม่มีให้ pip install plotly นะครับ
import numpy as np #TODO: ถ้ายังไม่มีให้ pip install numpy นะครับ

root = tk.Tk()

window_width=1100
window_height=1000
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

select_dataset1 = tk.StringVar()

dataset_1 = ttk.Combobox(root, textvariable=select_dataset1, state='readonly')
dataset_1.set('No. of Arrivals')
dataset_1['values'] = ('No. of Arrivals', 'Length of Stay','Per Capita Spending Baht', 'Per Capita Spending USD','Tourism Receipts Mil. Baht', 'Tourism Receipts Mil. USD')
dataset_1.place(x=720, y=950, width=230, height=30)

def selected_dataset():
    global result_dataset
    result_dataset = select_dataset1.get()
    print(result_dataset)
    #place the combobox
    graph_chart = pd.read_csv('GraphVisualization/src/database/tourism-receipts-from-international-tourist-arrivals_2018.csv')
    #make a graph chart
    data_frame = pd.DataFrame(graph_chart)
    figure1 = plt.Figure(figsize=(8, 7), dpi=100)
    ax1 = figure1.add_subplot(111)
    graph_chart1 = FigureCanvasTkAgg(figure1, root)
    graph_chart1.get_tk_widget().place(x=250, y=200)

    data_frame = data_frame[['Country', f'{result_dataset} By GROUP TOUR', f'{result_dataset} By NON GROUP TOUR']].groupby('Country').sum().astype(float)
    data_frame.plot(kind='bar', legend=True, ax=ax1, fontsize=8)
    ax1.set_title('Country has arrive to Thailand VS. No. of Arrivals')
#button for graph chart
select_data_btn = customtkinter.CTkButton(master=root, text="Comfirm Data", command=selected_dataset, width=150, height=50, compound="left",
                                            fg_color="#00ADB5", hover_color="#C77C78")
select_data_btn.place(x=950, y=950)

back_btn = customtkinter.CTkButton(master=root, text="Back",command="" , width=150, height=50, compound="left",
                                            fg_color="#00ADB5", hover_color="#C77C78")
back_btn.place(x=250, y=940)

print(dataset_1)

root.mainloop()