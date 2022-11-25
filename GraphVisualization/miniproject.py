####################################################    PLEASE READ AN ATTENTION HERE!    ####################################################################
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
####################################################    PLEASE READ AN ATTENTION HERE!    ###################################################################

class App:
    def __init__(self, root):
        def back_to_chart_analysis():
                for widget in root.winfo_children():
                    widget.destroy()
                main()
        def main():
            #setting title
            root.title("Data Analysis KMITL")
            icon = PhotoImage(file = 'GraphVisualization/src/images/icon.png')
            root.iconphoto(False, icon)
            root.option_add("*Font", "Prompt 12")
            
            #setting window size
            window_width=1100
            window_height=1000
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x_cordinate = int((screen_width/2) - (window_width/2))
            y_cordinate = int((screen_height/2) - (window_height/2))
            root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
                    # Useless THEME but Beautiful
                    #style = ttk.Style(root)
                    #root.tk.call('source', 'GraphVisualization/src/theme/azure dark.tcl')
                    #style.theme_use('azure')
            root.resizable(width=False, height=False)
            
            ############################################################  Dataframe ############################################################
            def data_table_page():
                global data_table_page
                global data_input_btn
                global data_table_frame
                global data_confirm_btn
                global label_file
                global result_data_table
                global treescrollx, treescrolly
                data_frame_bg = "#393E46"
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
                label_file = tk.LabelFrame(text="ยังไม่ได้เลือกไฟล์", background=data_frame_bg, fg="white")
                label_file.place(x=420, y=160, height=20, width=500)
                    # Treeview Widget
                result_data_table = ttk.Treeview(data_table_frame)
                result_data_table.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

                treescrolly = tk.Scrollbar(data_table_frame, orient="vertical", command=result_data_table.yview) # command means update the yaxis view of the widget
                treescrollx = tk.Scrollbar(data_table_frame, orient="horizontal", command=result_data_table.xview) # command means update the xaxis view of the widget
                result_data_table.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
                treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
                treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
            
            def exit_btn():
                #askyesno is a function that return true if user click yes
                if messagebox.askyesno("ออกโปรแกรม?","คุณต้องการออกจากโปรแกรมจริงหรือ?"):
                    root.destroy()
                
            def read_file():
                """This Function will open the file explorer and assign the chosen file path to label_file"""
                result_data = filedialog.askopenfilename(initialdir="/",
                                                    title="Select A File",
                                                    filetype=(("csv files", "*.csv"),("xlsx files", "*.xlsx"),("All Files", "*.*")))
                label_file["text"] = result_data
                return None
            
            def load_data():
                global file_path
                """If the file selected is valid this will load the file into the Treeview"""
                file_path = label_file["text"]
                try:
                    excel_filename = r"{}".format(file_path)
                    if excel_filename[-4:] == ".csv":
                        df = pd.read_csv(excel_filename)
                    else:
                        df = pd.read_excel(excel_filename)

                except ValueError:
                    tk.messagebox.showerror("Information", "The file you have chosen is invalid.")
                    return None
                except FileNotFoundError:
                    tk.messagebox.showerror("Information", f"No such file please select a valid file.")
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
                
            ############################################################  Graph Chart Page ############################################################
            def graph_chart():
                global back_btn
                global graph_chart1
                global figure1
                global select_data_btn
                global dataset_1
                #place the combobox
                try:
                    select_dataset1 = tk.StringVar()
                    dataset_1 = ttk.Combobox(root, textvariable=select_dataset1, state='readonly')
                    dataset_1.set('No. of Arrivals')
                    dataset_1['values'] = ('No. of Arrivals', 'Length of Stay','Per Capita Spending Baht', 'Per Capita Spending USD','Tourism Receipts Mil. Baht', 'Tourism Receipts Mil. USD')
                    dataset_1.place(x=470, y=950, width=230, height=30)
                    
                    def selected_dataset():
                        try:
                            global result_dataset
                            result_dataset = select_dataset1.get()
                            
                            print(file_path)
                            graph_chart = pd.read_csv(file_path)
                            #make a graph chart
                            data_frame = pd.DataFrame(graph_chart)
                            figure1 = plt.Figure(figsize=(8, 7), dpi=100)
                            ax1 = figure1.add_subplot(111)
                            graph_chart1 = FigureCanvasTkAgg(figure1, root)
                            graph_chart1.get_tk_widget().place(x=250, y=200)

                            data_frame = data_frame[['Country', f'{result_dataset} By GROUP TOUR', f'{result_dataset} By NON GROUP TOUR']].groupby('Country').sum().astype(float)
                            data_frame.plot(kind='line', legend=True, ax=ax1, fontsize=8)
                            ax1.set_title('Country has arrive to Thailand By Group Tour and NON Group Tour')
                        except ValueError:
                            tk.messagebox.showerror("Information", "The file you have chosen is invalid")
                            return None
                        except FileNotFoundError:
                            tk.messagebox.showerror("Information", f"You din't click CONFIRM! for analysis please click confirm")
                            return None
                        except NameError:
                            tk.messagebox.showerror("Information", f"Plese choose file for analysis and then click confirm")
                            return None
                    #button for graph chart
                    select_data_btn = customtkinter.CTkButton(master=root, text="Comfirm Data", command=selected_dataset, width=150, height=50, compound="left",
                                                                fg_color="#00ADB5", hover_color="#C77C78")
                    select_data_btn.place(x=740, y=940)

                    back_btn = customtkinter.CTkButton(master=root, text="Back",command=back_to_chart_analysis , width=150, height=50, compound="left",
                                                                fg_color="#00ADB5", hover_color="#C77C78")
                    back_btn.place(x=250, y=940)
                    
                except ValueError:
                    tk.messagebox.showerror("Information", "The file you have chosen is invalid")
                    return None
                except FileNotFoundError:
                    tk.messagebox.showerror("Information", f"You din't click CONFIRM! for analysis please click confirm")
                    return None
                except NameError:
                    tk.messagebox.showerror("Information", f"Plese choose file for analysis and then click confirm")
                    return None
            
            def bar_chart():
                try:
                    select_dataset1 = tk.StringVar()
                    dataset_1 = ttk.Combobox(root, textvariable=select_dataset1, state='readonly')
                    dataset_1.set('No. of Arrivals')
                    dataset_1['values'] = ('No. of Arrivals', 'Length of Stay','Per Capita Spending Baht', 'Per Capita Spending USD','Tourism Receipts Mil. Baht', 'Tourism Receipts Mil. USD')
                    dataset_1.place(x=470, y=950, width=230, height=30)
                    
                    def selected_dataset():
                        try:
                            global result_dataset
                            result_dataset = select_dataset1.get()
                            
                            print(file_path)
                            graph_chart = pd.read_csv(file_path)
                            #make a graph chart
                            data_frame = pd.DataFrame(graph_chart)
                            figure1 = plt.Figure(figsize=(8, 7), dpi=100)
                            ax1 = figure1.add_subplot(111)
                            graph_chart1 = FigureCanvasTkAgg(figure1, root)
                            graph_chart1.get_tk_widget().place(x=250, y=200)

                            data_frame = data_frame[['Country', f'{result_dataset} By GROUP TOUR', f'{result_dataset} By NON GROUP TOUR']].groupby('Country').sum().astype(float)
                            data_frame.plot(kind='bar', legend=True, ax=ax1, fontsize=8)
                            ax1.set_title('Country has arrive to Thailand By Group Tour and NON Group Tour')
                        except ValueError:
                            tk.messagebox.showerror("Information", "The file you have chosen is invalid")
                            return None
                        except FileNotFoundError:
                            tk.messagebox.showerror("Information", f"You din't click CONFIRM! for analysis please click confirm")
                            return None
                        except NameError:
                            tk.messagebox.showerror("Information", f"Plese choose file for analysis and then click confirm")
                            return None
                    #button for graph chart
                    select_data_btn = customtkinter.CTkButton(master=root, text="Comfirm Data", command=selected_dataset, width=150, height=50, compound="left",
                                                                fg_color="#00ADB5", hover_color="#C77C78")
                    select_data_btn.place(x=740, y=940)

                    back_btn = customtkinter.CTkButton(master=root, text="Back",command=back_to_chart_analysis , width=150, height=50, compound="left",
                                                                fg_color="#00ADB5", hover_color="#C77C78")
                    back_btn.place(x=250, y=940)
                    
                except ValueError:
                    tk.messagebox.showerror("Information", "The file you have chosen is invalid")
                    return None
                except FileNotFoundError:
                    tk.messagebox.showerror("Information", f"You din't click CONFIRM! for analysis please click confirm")
                    return None
                except NameError:
                    tk.messagebox.showerror("Information", f"Plese choose file for analysis and then click confirm")
                    return None

            def scatter_chart():
                
                global back_btn
                global scatter1
                try:
                    print(file_path)
                    scatter_chart = pd.read_csv(file_path)
                    result_data = pd.DataFrame(scatter_chart)
                    #success: make scatter chart
                    figure1 = plt.Figure(figsize=(8, 7), dpi=100)
                    ax1 = figure1.add_subplot(111)
                    ax1.set_ylabel('Lenght of Stay', fontsize=9)
                    ax1.set_xlabel('Country', fontsize=9)
                    ax1.scatter(result_data['Length of Stay'], result_data['Country'], color='g', s=50, alpha=0.5, edgecolors='black', linewidths=1, )
                    scatter1 = FigureCanvasTkAgg(figure1, root)
                    scatter1.get_tk_widget().place(x=250, y=200)
                    ax1.legend(['Country'])
                    ax1.set_title('Country has arrive to Thailand VS. Lenght of Stay')
                except ValueError:
                    tk.messagebox.showerror("Information", "The file you have chosen is invalid")
                    return None
                except FileNotFoundError:
                    tk.messagebox.showerror("Information", f"You din't click CONFIRM! for analysis please click confirm")
                    return None
                except NameError:
                    tk.messagebox.showerror("Information", f"Plese choose file for analysis and then click confirm")
                    return None
                    
                #button for graph chart
                back_btn = customtkinter.CTkButton(master=root, text="Back",command=back_to_chart_analysis , width=150, height=50, compound="left",
                                                            fg_color="#00ADB5", hover_color="#C77C78")
                back_btn.place(x=250, y=940)
            
            def geo_map_chart():
                try:
                    print(file_path)
                    graph_chart = pd.read_csv(file_path)
                    #make a graph chart
                    data = pd.DataFrame(graph_chart)
                    print(data.shape)

                    data['Country'] = data['Country'].dropna().apply(lambda x :  x.replace(' ,',',').replace(', ',',').split(','))
                    lst_col = 'Country'
                    data2 = pd.DataFrame({
                        col :  np.repeat(data[col].values, data[lst_col].str.len())
                        for col in data.columns.drop(lst_col)}
                        ).assign(**{lst_col:np.concatenate(data[lst_col].values)})[data.columns.tolist()]

                    year_country2 = data2.groupby('No. of Arrivals')['Country'].value_counts().reset_index(name='counts')

                    fig = px.choropleth(year_country2, locations="Country", color="counts", 
                                        locationmode='country names',
                                        animation_frame='No. of Arrivals',
                                        range_color=[0, 1],
                                        color_continuous_scale=px.colors.sequential.OrRd
                                    )

                    fig.update_layout(title='Comparison by country')
                    fig.show()
                    
                    
                except ValueError:
                    tk.messagebox.showerror("Information", "The file you have chosen is invalid")
                    return None
                except FileNotFoundError:
                    tk.messagebox.showerror("Information", f"You din't click CONFIRM! for analysis please click confirm")
                    return None
                except NameError:
                    tk.messagebox.showerror("Information", f"Plese choose file for analysis and then click confirm")
                    return None
                    
                """ #button for graph chart
                back_btn = customtkinter.CTkButton(master=root, text="Back",command=back_to_chart_analysis , width=150, height=50, compound="left",
                                                            fg_color="#00ADB5", hover_color="#C77C78")
                back_btn.place(x=250, y=940)    """
            ############################################################  ENDING of Graph Chart Page ############################################################
            
            ############################################################  Data Analysis Page ############################################################
            def data_analysis_page():
                global data_analysis_frame
                global graph_chart_btn
                global bar_chart_btn
                global scatter_chart_btn
                global geo_chart_btn
                
                # destroy the previous page
                data_table_frame.destroy()
                
                
                data_analysis_frame = tk.Frame(dataframe, background=data_frame_bg)
                data_analysis_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
                #lb = tk.Label(data_analysis_frame)
                #lb.pack()
                
                #chartimages
                graph_chart_img = ImageTk.PhotoImage(Image.open("GraphVisualization/src/images/graph_chart.png").resize((100,100), Image.ANTIALIAS))
                bar_chart_img = ImageTk.PhotoImage(Image.open("GraphVisualization/src/images/bar_chart.png").resize((100,100), Image.ANTIALIAS))
                scatter_chart_img = ImageTk.PhotoImage(Image.open("GraphVisualization/src/images/scatter_chart.png").resize((100,100), Image.ANTIALIAS))
                geo_chart_img = ImageTk.PhotoImage(Image.open("GraphVisualization/src/images/geomap_chart.png").resize((100,100), Image.ANTIALIAS))
                
                #buttons
                graph_chart_btn = customtkinter.CTkButton(master=root, image=graph_chart_img, text="Graph Chart",command=lambda: graph_chart() , width=250, height=80, compound="left",
                                                                fg_color="#00ADB5", hover_color="#C77C78")
                
                bar_chart_btn = customtkinter.CTkButton(master=root, image=bar_chart_img, text="Bar Chart",command=lambda: bar_chart() , width=250, height=80, compound="left",
                                                                fg_color="#00ADB5", hover_color="#C77C78")
                scatter_chart_btn = customtkinter.CTkButton(master=root, image=scatter_chart_img, text="Scatter Chart",command=lambda:scatter_chart() , width=250, height=80, compound="left",
                                                                fg_color="#00ADB5", hover_color="#C77C78")
                geo_chart_btn = customtkinter.CTkButton(master=root, image=geo_chart_img, text="Geo Map Chart",command=lambda: geo_map_chart() , width=250, height=80, compound="left",
                                                                fg_color="#00ADB5", hover_color="#C77C78")
                
                graph_chart_btn.place(x=350, y=340)
                bar_chart_btn.place(x=680, y=340)
                scatter_chart_btn.place(x=350, y=500)
                geo_chart_btn.place(x=680, y=500)
                
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
            menu_datatable_btn = customtkinter.CTkButton(master=root, image=data_table_image, command=data_table_page, text="Data Table", width=150, height=50, compound="left", 
                                                        fg_color="#00ADB5", hover_color="#C77C78")
            menu_datatable_btn.pack(padx=2, pady=5)
            
            data_analysis_btn = customtkinter.CTkButton(master=root, image=pie_chart_image, command=data_analysis_page, text="Data Analysis", width=150, height=50, compound="left", 
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

            data_table_page() # default page run at first start program
        main()
#initialize the window
if __name__ == "__main__":
    #create CTk window
    root = customtkinter.CTk() #ใช้ส่วนเสริม customtkinter เพื่อความสวยงามโดยการ pip install customtkinter
    app = App(root)
    root.mainloop()
    