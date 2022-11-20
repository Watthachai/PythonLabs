import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter
from tkinter import *
from PIL import Image, ImageTk
import pandas as pd 
from tkinter import filedialog
import csv

class App:
    def __init__(self, root):
        #setting title
        root.title("Data Analysis KMITL")
        icon = PhotoImage(file = 'GraphVisualization/src/images/icon.png')
        root.iconphoto(False, icon)
        
        #setting window size
        width=1100
        height=1000
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
        def exit_btn():
            #askyesno is a function that return true if user click yes
            if messagebox.askyesno("ออกโปรแกรม?","คุณต้องการออกจากโปรแกรมจริงหรือ?"):
                root.destroy()
            
        def read_file():
            """This Function will open the file explorer and assign the chosen file path to label_file"""
            result_data = filedialog.askopenfilename(initialdir="/",
                                                title="Select A File",
                                                filetype=(("csv ดรสำห", "*.csv"),("xlsx files", "*.xlsx"),("All Files", "*.*")))
            label_file["text"] = result_data
            print()
            print("File Path: ", result_data, "Type: ", type(result_data))
            return None
        
        def load_data():
            """If the file selected is valid this will load the file into the Treeview"""
            file_path = label_file["text"]
            try:
                excel_filename = r"{}".format(file_path)
                if excel_filename[-4:] == ".csv":
                    df = pd.read_csv(excel_filename)
                else:
                    df = pd.read_excel(excel_filename)

            except ValueError:
                tk.messagebox.showerror("Information", "The file you have chosen is invalid")
                return None
            except FileNotFoundError:
                tk.messagebox.showerror("Information", f"No such file as {file_path}")
                return None

            clear_data()
            result_data_table["column"] = list(df.columns)
            result_data_table["show"] = "headings"
            for column in result_data_table["columns"]:
                result_data_table.heading(column, text=column) # let the column heading = column name

            df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
            for row in df_rows:
                result_data_table.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
            return None


        def clear_data():
            result_data_table.delete(*result_data_table.get_children())
            return None
        
        # Creating Frame
        menu_frame_bg = "#222831"
        data_frame_bg = "#393E46"
        menuframe = Frame(height=1000, width=200, background=menu_frame_bg, bd=1, relief=FLAT)
        menuframe.place(x=0, y=0)
        dataframe = Frame(height=1000, width=1100, background=data_frame_bg, bd=1, relief=FLAT)
        dataframe.place(x=200, y=0)
        
        # For setting THEME!! of my component naja
        #images
        logo = PhotoImage(file = 'GraphVisualization/src/images/logo.png')
        # customtkinter.set_default_color_theme("green")
        data_table_image = ImageTk.PhotoImage(Image.open('GraphVisualization/src/images/data_table_image.png').resize((50,50), Image.ANTIALIAS))
        pie_chart_image = ImageTk.PhotoImage(Image.open('GraphVisualization/src/images/pie_chart_image.png').resize((50,50), Image.ANTIALIAS))
        cancel_image = ImageTk.PhotoImage(Image.open('GraphVisualization/src/images/cancel.png').resize((50,50), Image.ANTIALIAS))

        ############################################################   Menuframe ############################################################
            # Use CTkButton instead of tkinter Button because ความสวยงามยังไงล่ะ
            #   Button Menuframe
        menu_datatable_btn = customtkinter.CTkButton(master=root, image=data_table_image, command="", text="Data Table", width=150, height=50, compound="left", 
                                                    fg_color="#00ADB5", hover_color="#C77C78")
        menu_datatable_btn.pack(padx=2, pady=5)

        data_analysis_btn = customtkinter.CTkButton(master=root, image=pie_chart_image, command="", text="Data Analysis", width=150, height=50, compound="left", 
                                                    fg_color="#00ADB5", hover_color="#C77C78")
        data_analysis_btn.pack(padx=2, pady=5)
        
        exit_btn = customtkinter.CTkButton(master=root, image=cancel_image, command=exit_btn, text="Exit", width=150, height=50, compound="left",
                                                    fg_color="#D35B68", hover_color="#C77C78")
        exit_btn.pack(padx=2, pady=2)
            # Showing at the Frame of the screen
        menu_datatable_btn.place(x=25, y=200)
        data_analysis_btn.place(x=25, y=290)
        exit_btn.place(x=25, y=900)
        logo = Label(master=root, image=logo).place(x=35, y=20)
        
        ############################################################  Dataframe ############################################################
            #   Button Dataframe
        data_input_btn = customtkinter.CTkButton(master=root, text="Insert",command=read_file , width=150, height=50, compound="left",
                                                    fg_color="#00ADB5", hover_color="#C77C78")
        data_input_btn.place(x=250, y=140)
        
            # Show label at the screen
        Label(master=root, text="สรุปรายได้และค่าใช้จ่ายการท่องเที่ยวจากนักท่องเที่ยวชาวต่างชาติที่เดินทางเข้าประเทศไทยปี 2019 และ 2020 \nTOURISM RECEIPTS FROM INTERNATIONAL TOURIST ARRIVALS 2019 AND 2020", background="#393E46", foreground="white" , font=("Prompt", 13)).place(x=260, y=50)
        
            # Frame for TreeView
        data_table_frame = tk.Label(root, text="ตารางข้อมูล")
        data_table_frame.place(height=780, width=800, x=250, y=200)

            # Buttons
        data_confirm_btn = customtkinter.CTkButton(text="Confirm", command=lambda: load_data())
        data_confirm_btn.place(x=950, y=140, width=100, height=50)

            # The file/file path text
        label_file = tk.LabelFrame(text="ยังไม่ได้เลือกไฟล์")
        label_file.place(x=420, y=160, height=20, width=500)
            # Treeview Widget
        result_data_table = ttk.Treeview(data_table_frame)
        result_data_table.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

        treescrolly = tk.Scrollbar(data_table_frame, orient="vertical", command=result_data_table.yview) # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(data_table_frame, orient="horizontal", command=result_data_table.xview) # command means update the xaxis view of the widget
        result_data_table.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
        
        ############################################################  Data Analysis Page ############################################################
        def data_analysis_page():
            data_analysis_frame = tk.Frame(dataframe)
            lb = tk.Label(data_analysis_frame, text="Data Analysis")
            lb.pack()
            data_analysis_graph_btn = customtkinter.CTkButton(master=root, text="Graph Chart",command="" , width=150, height=50, compound="left",
                                                            fg_color="#00ADB5", hover_color="#C77C78")
            data_analysis_graph_btn.place(x=250, y=240)
#initialize the window
if __name__ == "__main__":
    #create CTk window
    root = customtkinter.CTk() #ใช้ส่วนเสริม customtkinter เพื่อความสวยงามโดยการ pip install customtkinter
    app = App(root)
    root.mainloop()
