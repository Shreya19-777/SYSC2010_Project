import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import customtkinter as ctk
from scipy import signal
from tkinter import filedialog

#Importing files
import preprocessing

#*************************************************GUI**********************************************
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SYSC 2010 Final Project")
        self.geometry("800x550")
        
        #Getting CSV file name
        self.label_title = ctk.CTkLabel(self, text="CSV File Name", font=ctk.CTkFont(weight="bold")).pack()
        self.entry_file = ctk.CTkEntry(self, width=300)
        self.entry_file.pack(pady=5)
        
        self.btn_browse = ctk.CTkButton(self, text="Browse File", command=self.browse_file)
        self.btn_browse.pack(pady=5)

        #Getting the x axis column name (time)
        ctk.CTkLabel(self, text="X-axis Column (Time): ").pack()
        self.entry_x = ctk.CTkEntry(self, width=300)
        self.entry_x.pack(pady=5)

        #Getting y axis column name (signal)
        ctk.CTkLabel(self, text="Y-axis Column (Signal): ").pack()
        self.entry_y = ctk.CTkEntry(self, width=300)
        self.entry_y.pack(pady=5)

        #Dropdown list (choosing data type)
        self.label_type = ctk.CTkLabel(self, text="Select Data Type:")
        self.label_type.pack(pady=(15, 0))
        self.dropdown = ctk.CTkComboBox(self, values=["ECG", "Temperature", "Respiration", "Motion"], width=200)
        self.dropdown.set("ECG")
        self.dropdown.pack(pady=5)

        #Button
        self.btn_load = ctk.CTkButton(self, text="Load & Filter Data", 
            command=self.handle_selection,
            fg_color="transparent", 
            border_width=2,
            text_color=("gray10", "#DCE4EE"))
        self.btn_load.pack(pady=30)
        
        #-------------------------------------KEY FEATURES---------------------------------------------
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(pady=10, padx=20, fill="x") # Added .pack()
        
        self.stats_title = ctk.CTkLabel(self.stats_frame, text="Key Features", font=ctk.CTkFont(weight="bold"))
        self.stats_title.pack(pady=5)
        
    
    #BROWSING FOR CSV FILE
    def browse_file(self):
        #Choosing csv files only
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.entry_file.delete(0, "end")
            self.entry_file.insert(0, file_path)
            
    def handle_selection(self):
        
        choice = self.dropdown.get()

        #Reading csv filename and columns
        filename = self.entry_file.get().strip()
        x = self.entry_x.get().strip()
        y = self.entry_y.get().strip()
        
        extracts = preprocessing.preprocess(filename, choice, x, y)
        print(extracts)
        
        for key,value in extracts.items() :
            self.stat_labels[key].configure(text=f"{key.title()}: {value:.4f}")
        
#**************************************CHOOSING CORRECT FILTER FOR SPECIFIED DATA TYPE****************************************

if __name__ == "__main__":
    app = GUI()
    app.mainloop()
    
