import customtkinter as ctk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

#Importing files
import data_loader

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SYSC 2010 Final Project")
        self.geometry("1400x900")

#-------------------------------------SIDEBAR-------------------------------------------------------------------
        self.sidebar = ctk.CTkScrollableFrame(self, width=300)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        self.sidebar.pack_propagate(True)

        #Getting CSV file name
        self.label_title = ctk.CTkLabel(self.sidebar, text="CSV File Name", font=ctk.CTkFont(weight="bold"))
        self.label_title.pack(pady = (10, 3))
        self.entry_file = ctk.CTkEntry(self.sidebar, width=250)
        self.entry_file.pack(pady=3)
        
        self.btn_browse = ctk.CTkButton(self.sidebar, text="Browse File", command=self.browse_file)
        self.btn_browse.pack(pady=3)

        #Getting the x axis column name (time)
        ctk.CTkLabel(self.sidebar, text="X-axis Column (Time): ").pack(pady=(5, 0))
        self.entry_x = ctk.CTkEntry(self.sidebar, width=250)
        self.entry_x.pack(pady=3)

        #Getting y axis column name (signal)
        ctk.CTkLabel(self.sidebar, text="Y-axis Column (Signal): ").pack(pady=(10, 0))
        self.entry_y = ctk.CTkEntry(self.sidebar, width=250)
        self.entry_y.pack(pady=3)

        #Dropdown list (choosing data type)
        self.label_type = ctk.CTkLabel(self.sidebar, text="Select Data Type:")
        self.label_type.pack(pady=(15, 0))
        self.dropdown1 = ctk.CTkComboBox(self.sidebar, values=["ECG", "Temperature", "Respiration", "Motion"], width=200)
        self.dropdown1.set("ECG")
        self.dropdown1.pack(pady=5)
        
        #Dropdown list (choosing unit)
        self.label_type = ctk.CTkLabel(self.sidebar, text="Select Unit for Time:")
        self.label_type.pack(pady=(15, 0))
        self.dropdown2 = ctk.CTkComboBox(self.sidebar, values=["Seconds", "Milliseconds"], width=200)
        self.dropdown2.set("Seconds")
        self.dropdown2.pack(pady=5)

        #Button
        self.btn_load = ctk.CTkButton(self.sidebar, text="Load & Filter Data", 
            command=self.handle_selection,
            border_width=2)
        self.btn_load.pack(pady=30)
        
#------------switch for showing raw signal overlay on the time domain plot----------------------
        self.show_raw_switch = ctk.CTkSwitch(self.sidebar, text="Show Raw Signal Overlay")
        self.show_raw_switch.pack(pady=10) 
       
#----------------------- switch for showing fft----------------------
        self.show_fft_switch = ctk.CTkSwitch(self.sidebar, text="Show FFT")
        self.show_fft_switch.pack(pady=10) 
#-------------------------------------KEY FEATURES---------------------------------------------
        self.stats_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.stats_frame.pack(pady=5, fill="x") 
        
        self.stats_title = ctk.CTkLabel(self.stats_frame, text="Key Features", font=ctk.CTkFont(weight="bold"))
        self.stats_title.pack(pady=5)
        self.dynamic_labels = []
        

#------------------------------------Graph frame (for plotting the data)-----------------------------------------------
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

 #------------------------------------Matplotlib-----------------------------------------------
       
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 8))
        self.figure.patch.set_facecolor("#686767F8") 
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
              
        #toolbar for zooming and panning
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
        self.toolbar.update()
        self.toolbar.pack(side="top", fill="x")
        
        self.canvas.get_tk_widget().pack(side="bottom", fill="both", expand=True)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.after_cancel(self.handle_selection)
        self.quit() 
        try:
            self.destroy()
        except Exception:
            pass
        
    #Finding CSV
    def browse_file(self):
        #Choosing csv files only
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.entry_file.delete(0, "end")
            self.entry_file.insert(0, file_path)
            
    def handle_selection(self):
        choice = self.dropdown1.get()
        unit = self.dropdown2.get()

        #Reading csv filename and columns
        filename = self.entry_file.get().strip()
        x = self.entry_x.get().strip()
        y = self.entry_y.get().strip()
        
        #Clearing the plots 
        self.ax1.clear()
        self.ax2.clear()
        
        # get filtered data and extracted features
        pck = data_loader.data_load(filename, choice, x, y, unit)
        #pck= preprocessing.preprocess(filename, choice, x, y)
        if pck is None:
            return

        self.ax1.clear()
        # Plot Comparison
        if self.show_raw_switch.get() == 1:
            self.ax1.plot(pck["time"], pck["raw_signal"], color='gray', alpha=0.5, label='Raw')
        
        self.ax1.plot(pck["time"], pck["clean_signal"], color='blue', label='Filtered')
        self.ax1.set_title(f"Raw VS Filtered {choice} Signal")
        self.ax1.tick_params(colors='white')
    
        #  Axis Labels 
        self.ax1.set_xlabel("Time (s)", color='Black')
        self.ax1.set_ylabel("Amplitude (mV)", color='Black')
        self.ax1.legend() 

        if self.show_fft_switch.get() == 1:
            self.ax2.clear()
            self.ax2.plot(pck['fft_freqs'], pck['raw_fft_mag'], color='gray', alpha=0.3, label='Raw FFT')
            self.ax2.plot(pck['fft_freqs'], pck['fft_mag'], color='orange', label='Clean FFT')
            self.ax2.set_title("FFT Spectrum Comparison")
            self.ax2.tick_params(colors='white')
            self.ax2.set_xlabel("Frequency (Hz)", color ='Black')
            self.ax2.set_ylabel("Magnitude", color='Black')
            self.ax2.legend()
        else:
            self.ax2.clear()

        self.figure.tight_layout()
        self.canvas.draw_idle()
        self.update_idletasks()  
       
       # -----------------------Update the stats in the sidebar-----------------------
        self.clear_stats()
        
        for key, value in pck.items():
                if key in ["raw_signal", "clean_signal", "time", "fft_freqs", "fft_mag", "raw_fft_mag"]:
                    continue  # Skip

                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        sub_value = np.round(sub_value, 2)
                        new_lbl = ctk.CTkLabel(
                            self.stats_frame, 
                            text=f"{sub_key}: {sub_value}", 
                            font=ctk.CTkFont(size=12)
                        )
                        new_lbl.pack(pady=2, padx=20, anchor="w")
                        self.dynamic_labels.append(new_lbl)
            
            
    def clear_stats(self):
        for label in self.dynamic_labels:
            label.destroy()
        # Reset the list
        self.dynamic_labels = []