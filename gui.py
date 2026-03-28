import customtkinter as ctk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Importing files
import preprocessing

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SYSC 2010 Final Project")
        self.geometry("1200x800")

#-------------------------------------SIDEBAR---------------------------------------------(for user inputs and ststs)----------------------
        self.sidebar = ctk.CTkFrame(self, width=300)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        #Getting CSV file name
        self.label_title = ctk.CTkLabel(self.sidebar, text="CSV File Name", font=ctk.CTkFont(weight="bold")).pack()
        self.entry_file = ctk.CTkEntry(self.sidebar, width=300)
        self.entry_file.pack(pady=5)
        
        self.btn_browse = ctk.CTkButton(self.sidebar, text="Browse File", command=self.browse_file)
        self.btn_browse.pack(pady=5)

        #Getting the x axis column name (time)
        ctk.CTkLabel(self.sidebar, text="X-axis Column (Time): ").pack()
        self.entry_x = ctk.CTkEntry(self.sidebar, width=300)
        self.entry_x.pack(pady=5)

        #Getting y axis column name (signal)
        ctk.CTkLabel(self.sidebar, text="Y-axis Column (Signal): ").pack()
        self.entry_y = ctk.CTkEntry(self.sidebar, width=300)
        self.entry_y.pack(pady=5)

        #Dropdown list (choosing data type)
        self.label_type = ctk.CTkLabel(self.sidebar, text="Select Data Type:")
        self.label_type.pack(pady=(15, 0))
        self.dropdown = ctk.CTkComboBox(self.sidebar, values=["ECG", "Temperature", "Respiration", "Motion"], width=200)
        self.dropdown.set("ECG")
        self.dropdown.pack(pady=5)

        #Button
        self.btn_load = ctk.CTkButton(self.sidebar, text="Load & Filter Data", 
            command=self.handle_selection,
            fg_color="transparent", 
            border_width=2,
            text_color=("gray10", "#DCE4EE"))
        self.btn_load.pack(pady=30)

            #-------------------------------------KEY FEATURES---------------------------------------------
        
        self.stats_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.stats_frame.pack(pady=10, padx=20, fill="x") 
        
        self.stats_title = ctk.CTkLabel(self.stats_frame, text="Key Features", font=ctk.CTkFont(weight="bold"))
        self.stats_title.pack(pady=5)
        self.dynamic_labels = []
        

    #------------------------------------Graph frame (for plotting the data)-----------------------------------------------
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    #------------------------------------Matplotlib-----------------------------------------------
       
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 8))
        self.figure.patch.set_facecolor('#2b2b2b') 
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        

    #Fiunding CSV
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
        
        #Calling the preprocessing function
        extracts = preprocessing.preprocess(filename, choice, x, y)
        
        if extracts is None:  # ← ADD THIS
            print("preprocess returned None")
            return
        #Clearing the previous labels
        self.clear_stats()
        
        for key, value in extracts.items():
                new_lbl = ctk.CTkLabel(
                    self.stats_frame, 
                    text=f"{key}: {value}", 
                    font=ctk.CTkFont(size=12)
                )
                new_lbl.pack(pady=10, padx=200, anchor="w")
                
                # Save it so we can clear it next time
                self.dynamic_labels.append(new_lbl)
            
    def clear_stats(self):
        for label in self.dynamic_labels:
            label.destroy()
        # Reset the list
        self.dynamic_labels = []