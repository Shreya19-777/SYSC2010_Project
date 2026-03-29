import customtkinter as ctk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#Importing files
import preprocessing
import data_loader

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SYSC 2010 Final Project")
        self.geometry("1200x800")

#-------------------------------------SIDEBAR---------------------------------------------(for user inputs and ststs)----------------------
        self.sidebar = ctk.CTkFrame(self, width=300)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        self.sidebar.pack_propagate(False)

        #Getting CSV file name
        self.label_title = ctk.CTkLabel(self.sidebar, text="CSV File Name", font=ctk.CTkFont(weight="bold"))
        self.label_title.pack(pady = (10, 5))
        self.entry_file = ctk.CTkEntry(self.sidebar, width=250)
        self.entry_file.pack(pady=5)
        
        self.btn_browse = ctk.CTkButton(self.sidebar, text="Browse File", command=self.browse_file)
        self.btn_browse.pack(pady=5)

        #Getting the x axis column name (time)
        ctk.CTkLabel(self.sidebar, text="X-axis Column (Time): ").pack(pady=(10, 0))
        self.entry_x = ctk.CTkEntry(self.sidebar, width=250)
        self.entry_x.pack(pady=5)

        #Getting y axis column name (signal)
        ctk.CTkLabel(self.sidebar, text="Y-axis Column (Signal): ").pack(pady=(10, 0))
        self.entry_y = ctk.CTkEntry(self.sidebar, width=250)
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
            text_color=("gray10", "#080808"))
        self.btn_load.pack(pady=30)

        self.show_raw_switch = ctk.CTkSwitch(self.sidebar, text="Show Raw Signal Overlay")
        self.show_raw_switch.pack(pady=10) 

            #-------------------------------------KEY FEATURES---------------------------------------------
        
        self.stats_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.stats_frame.pack(pady=10, fill="x") 
        
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
        self.withdraw() # Hide the window immediately
        self.quit()     # Stop the main loop
        self.destroy()  # Clean up resources
  
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
        
        # Get raw data 
        #raw_data = data_loader.data_load(filename, choice, x, y)
        

        # get filtered data and extracted features
        extracts = preprocessing.preprocess(filename, choice, x, y)
        raw_data = extracts[0]  # Unpack raw data
        if raw_data is None:
            print("data_load returned None")
            return
        raw_signal, raw_time = raw_data

        cleaned_signal = extracts[1]  # Unpack cleaned signal
        if cleaned_signal is None:
            print("preprocess returned None")
            return
        clean_signal, cleaned_time = cleaned_signal

            # Update the time domain Plot (ax1)
        self.ax1.clear()
        # Plot Comparison
        if self.show_raw_switch.get() == 1:
            self.ax1.plot(raw_time, raw_signal, color='gray', alpha=0.5, label='Raw')
        
        self.ax1.plot(cleaned_time, clean_signal, color='blue', label='Filtered')
        self.ax1.set_title(f"Raw VS Filtered {choice} Signal")
        self.ax1.tick_params(axis='x', colors='white')
        self.ax1.tick_params(axis='y', colors='white')

        #  Axis Labels 
        self.ax1.set_xlabel("Time (s)", color='Black')
        self.ax1.set_ylabel("Amplitude (mV)", color='Black')

        self.figure.tight_layout()
        self.ax1.legend() 

        self.figure.tight_layout()
        self.canvas.draw_idle()  #
        self.update_idletasks()  
        self.clear_stats()
        
        for key, value in extracts.items():
                new_lbl = ctk.CTkLabel(
                    self.stats_frame, 
                    text=f"{key}: {value}", 
                    font=ctk.CTkFont(size=12)
                )
                new_lbl.pack(pady=10, padx=20, anchor="w")
                # Store the label reference so we can clear them later
                self.dynamic_labels.append(new_lbl)
            
    def clear_stats(self):
        for label in self.dynamic_labels:
            label.destroy()
        # Reset the list
        self.dynamic_labels = []