import customtkinter
from tkinter import messagebox, filedialog, Tk
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import sys
import pandas as pd
import webbrowser
import cv2
import matplotlib.pyplot as plt
import numpy as np
import xlwings as xw
import openpyxl
from scipy.spatial import distance
body = []
def onclick(event):
    x, y = event.xdata, event.ydata
    if event.dblclick:
        plt.plot(x, y, 'go')
        body.append((x, y))
        plt.text(x, y, str(len(body)-1), color='red')  # Oznaèenie bodu èíslicou
        plt.draw()

def vypocet_vzdialenosti(bod1, bod2, skala):
    return np.sqrt((bod2[0] - bod1[0])**2 + (bod2[1] - bod1[1])**2) * skala
def vypocet_uhla(bod1, bod2, bod3):
    a = np.array(bod1)
    b = np.array(bod2)
    c = np.array(bod3)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)
def vypocet_plochy_polygonu(body_polygonu, skala):
    x = [bod[0] for bod in body_polygonu]
    y = [bod[1] for bod in body_polygonu]
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))) * skala**2
# Funkcia pre výpoèet bodu 45 bod na 0-7 radialny index k Diskodialnej odchylke 
def vypocet_bodu45(bod2, bod9, bod7):
    u = bod9 - bod2
    v = bod7 - bod2
    t = np.dot(u, v) / np.dot(u, u)
    bod45 = bod2 + t * u
    return bod45
# Funkcia pre výpoèet bodu 55 k DO ako bod najbližši k bodu 5 
def vypocet_bodu55(bod5, bod45, bod7):
    u = bod7 - bod45
    v = bod5 - bod45
    t = np.dot(u, v) / np.dot(u, u)
    bod55 = bod45 + t * u
    return bod55
# Funkcia pre výpoèet vzdialenosti DO
def vypocet_vzdialenosti_DO(bod5, bod55, skala):
    return np.linalg.norm(bod5 - bod55) * skala

# Funkcia pre výpoèet bodu 40 vypoèet aR bR
def vypocet_bodu40(bod2, bod5, bod9):
    u = bod9 - bod2
    v = bod5 - bod2
    t = np.dot(u, v) / np.dot(u, u)
    bod40 = bod2 + t * u
    return bod40

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x600")
        self.title("ApisVM")

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create the sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(9, weight=1)

        # Add the title to the sidebar
        self.title_label = customtkinter.CTkLabel(self.sidebar_frame, text="ApisVM", font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Add buttons to the sidebar
        buttons = ["Frontwing", "Backwing", "Excel", "XY points"]
        for i, button in enumerate(buttons):
            btn = customtkinter.CTkButton(self.sidebar_frame, text=button, command=lambda b=button: self.switch_to_class(b))
            btn.grid(row=i+1, column=0, padx=20, pady=10)

        # Add appearance mode options to the sidebar
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # Add scaling options to the sidebar
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "100%", "150%", "200%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

          # Add exit button to the sidebar
        self.exit_button = customtkinter.CTkButton(self.sidebar_frame, text="Exit", command=self.exit_application)
        self.exit_button.grid(row=9, column=0, padx=20, pady=(10, 20))
        # Create the main content frame
        self.content_frame = customtkinter.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Add a textbox with a title and text content
        self.textbox_title = customtkinter.CTkLabel(self.content_frame, text="Guide for ApisVM", font=("Arial", 16))
        self.textbox_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="n")

        textbox_content =  """
**Sidebar**
    1.Frontwing: For analyzing the front wing.
    2.Backwing: For analyzing the back wing.
    3.Excel: For merging Excel files and calculating probabilities.
    4. XY points: For displaying point coordinates.Comming soon

**Main Content**
    1.Calibration: Set calibration based on the selected image.
    2.Save: Set the path for saving results.
    3.Analysis: Start the wing analysis.
    4.Recalibrate: Reset the calibration.
    5.Reset Save: Reset the save path.

**Analysis Procedure**
1. **Calibration**
   1.Click the **Calibration** button.
   2.Select an image of the wing for calibration.
   3.Double-click to mark two points on the image to calculate the scale.
   4.After successful calibration, a message will appear indicating successful calibration.

2. **Setting the Save Path**
   1.Click the **Save** button.
   2.Select the directory where the analysis results will be saved.
   3.After successfully setting the path, a message will appear indicating successful save.

3. **Wing Analysis**
   1.Click the **Frontwing analysis** or **Backwing analysis** button depending on which wing you want to analyze.
   2.Select an image of the wing for analysis.
   3.Double-click to mark points on the image according to the DAWINO methodology.
   4.The script will calculate distances, angles, and other parameters and save the results to an Excel file.

4. **Merging Excel Files**
   1.Click the **Excel** button.
   2.Select the **Front excel merger** or **Back excel merger** option.
   3.Select the Excel files you want to merge.
   4.The script will create a new Excel file with average and median values.

5. **Calculating Probabilities**
   1.Click the **Excel** button.
   2.Select the **Posterior probability (Frontwing)** or **Posterior probability (Backwing)** option.
   3.Select the Excel file with the analysis results.
   4.The script will calculate and display posterior probabilities for various standards.
"""

        self.textbox = customtkinter.CTkTextbox(self.content_frame)
        self.textbox.insert("0.0", textbox_content)
        self.textbox.grid(row=1, column=0, padx=40, pady=(10, 20), sticky="nsew")

        # Add a bottom frame with centered text
        self.bottom_frame = customtkinter.CTkFrame(self)
        self.bottom_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        self.bottom_label = customtkinter.CTkLabel(self.bottom_frame,
                                                   text="Toto je program pre analýzu vèelieho krídla pod¾a metodiky DAWINO.",
                                                   anchor="center")
        self.bottom_label.pack(expand=True)

    def change_appearance_mode_event(self, new_mode):
        customtkinter.set_appearance_mode(new_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def exit_application(self):
        result = messagebox.askyesno("Exit Application", "Are you sure?")
        if result:
            self.quit()

    def switch_to_class(self, class_name):
        if class_name == "Frontwing":
            Frontwing(self)
        elif class_name == "Backwing":
            Backwing(self)
        elif class_name == "Excel":
            Excel(self)
        else:
            self.reset_calibration_and_save_path()
            self.show_textbox()
            self.clear_right_sidebar()

        

    def show_textbox(self):
        # Destroy the current content frame
        self.content_frame.destroy()
     

        # Create a new content frame with the original textbox
        self.content_frame = customtkinter.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.textbox_title = customtkinter.CTkLabel(self.content_frame, text="Guide for ApisVM", font=("Arial", 16))
        self.textbox_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="n")

        textbox_content = """
**Sidebar**
    1.Frontwing: For analyzing the front wing.
    2.Backwing: For analyzing the back wing.
    3.Excel: For merging Excel files and calculating probabilities.
    4. XY points: For displaying point coordinates.Comming soon

**Main Content**
    1.Calibration: Set calibration based on the selected image.
    2.Save: Set the path for saving results.
    3.Analysis: Start the wing analysis.
    4.Recalibrate: Reset the calibration.
    5.Reset Save: Reset the save path.

**Analysis Procedure**
1. **Calibration**
   1.Click the **Calibration** button.
   2.Select an image of the wing for calibration.
   3.Double-click to mark two points on the image to calculate the scale.
   4.After successful calibration, a message will appear indicating successful calibration.

2. **Setting the Save Path**
   1.Click the **Save** button.
   2.Select the directory where the analysis results will be saved.
   3.After successfully setting the path, a message will appear indicating successful save.

3. **Wing Analysis**
   1.Click the **Frontwing analysis** or **Backwing analysis** button depending on which wing you want to analyze.
   2.Select an image of the wing for analysis.
   3.Double-click to mark points on the image according to the DAWINO methodology.
   4.The script will calculate distances, angles, and other parameters and save the results to an Excel file.

4. **Merging Excel Files**
   1.Click the **Excel** button.
   2.Select the **Front excel merger** or **Back excel merger** option.
   3.Select the Excel files you want to merge.
   4.The script will create a new Excel file with average and median values.

5. **Calculating Probabilities**
   1.Click the **Excel** button.
   2.Select the **Posterior probability (Frontwing)** or **Posterior probability (Backwing)** option.
   3.Select the Excel file with the analysis results.
   4.The script will calculate and display posterior probabilities for various standards."""

        self.textbox = customtkinter.CTkTextbox(self.content_frame)
        self.textbox.insert("0.0", textbox_content)
        self.textbox.grid(row=1, column=0, padx=40, pady=(10, 20), sticky="nsew")

    def reset_calibration_and_save_path(self):
        self.calibration_factor = None
        global save_path
        save_path = None
        messagebox.showinfo("Reset", "Calibration and save path reset")

    def clear_right_sidebar(self):
        if hasattr(self, 'right_sidebar_frame'):
            for widget in self.right_sidebar_frame.winfo_children():
                if isinstance(widget, customtkinter.CTkTextbox):
                    widget.delete("1.0", "end")

class Frontwing(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # Initialize calibration factor and save path
        master.calibration_factor = None
        global save_path
        save_path = None

        # Replace main content frame with Frontwing content
        master.content_frame.destroy()
        
        master.content_frame = customtkinter.CTkFrame(master)
        master.content_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        
        # Create frames for buttons
        frame1 = customtkinter.CTkFrame(master.content_frame)
        frame1.pack(fill="both", expand=True)

        frame2 = customtkinter.CTkFrame(master.content_frame)
        frame2.pack(fill="both", expand=True)

        frame3 = customtkinter.CTkFrame(master.content_frame)
        frame3.pack(fill="both", expand=True)

        frame4 = customtkinter.CTkFrame(master.content_frame)
        frame4.pack(fill="both", expand=True)

        # Add buttons to frames
        self.calibration_btn = customtkinter.CTkButton(frame1, text='Calibration', command=self.calibrate)
        self.calibration_btn.pack(side="left", padx=5, pady=5, expand=True)

        self.recalibrate_btn = customtkinter.CTkButton(frame1, text='Recalibrate', command=self.recalibrate)
        self.recalibrate_btn.pack(side="left", padx=5, pady=5, expand=True)
        self.recalibrate_btn.pack_forget()  # Hide the recalibrate button initially

        self.save_btn = customtkinter.CTkButton(frame2, text='Save', command=self.save_path)
        self.save_btn.pack(side="left", padx=5, pady=5, expand=True)

        self.reset_save_btn = customtkinter.CTkButton(frame2, text='Reset Save', command=self.reset_save)
        self.reset_save_btn.pack(side="left", padx=5, pady=5, expand=True)
        self.reset_save_btn.pack_forget()  # Hide the reset save button initially

        self.analysis_btn = customtkinter.CTkButton(frame3, text='Frontwing analysis', command=self.analyze)
        self.analysis_btn.pack(side="left", padx=5, pady=5, expand=True)

        self.back_btn = customtkinter.CTkButton(frame4, text='Back', command=lambda: self.back_to_main(master))
        self.back_btn.pack(side="left", padx=5, pady=5, expand=True)


        # Create the right sidebar frame
        self.right_sidebar_frame = customtkinter.CTkFrame(master, width=200, corner_radius=0)
        self.right_sidebar_frame.grid(row=0, column=2, rowspan=4, sticky="nsew")
        self.right_sidebar_frame.grid_rowconfigure(9, weight=1)

        # Add the title to the right sidebar
        self.right_title_label = customtkinter.CTkLabel(self.right_sidebar_frame, text="Save location", font=("Arial", 16, "bold"))
        self.right_title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Add a listbox to display folder contents
        self.folder_listbox = customtkinter.CTkTextbox(self.right_sidebar_frame, height=200)
        self.folder_listbox.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="nsew")

        # Add the title for analyzed pictures
        self.analyzed_title_label = customtkinter.CTkLabel(self.right_sidebar_frame, text="Analysed pictures", font=("Arial", 16, "bold"))
        self.analyzed_title_label.grid(row=2, column=0, padx=20, pady=(20, 10))

        # Add a listbox to display analyzed picture names
        self.analyzed_listbox = customtkinter.CTkTextbox(self.right_sidebar_frame, height=200)
        self.analyzed_listbox.grid(row=3, column=0, padx=20, pady=(10, 10), sticky="nsew")

    def calibrate(self):
        global skala
        Tk().withdraw()
        cesta_k_obrazku = filedialog.askopenfilename()
        if not cesta_k_obrazku:
            return
        body.clear()
        obrazok = cv2.imread(cesta_k_obrazku)
        obrazok = cv2.cvtColor(obrazok, cv2.COLOR_BGR2RGB)

        fig, ax = plt.subplots()
        ax.imshow(obrazok)

        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()

        if len(body) >= 2:
            # Výpoèet škály na základe vzdialenosti medzi prvými dvoma bodmi
            skala = 1 / vypocet_vzdialenosti(body[0], body[1], 1)
            self.master.calibration_factor = skala
            self.calibration_btn.configure(text='Successful Calibration', font=('Bradley Hand ITC', 12), command=lambda: None)
            self.recalibrate_btn.pack(side="left", padx=5, pady=5, expand=True)  # Show the recalibrate button
            print(f"Calibration factor set to {self.master.calibration_factor} px to mm")
        else:
            print("Not enough points for calibration.")

    def save_path(self):
        global save_path
        save_path = filedialog.askdirectory()
        if save_path:
            messagebox.showinfo("Save Path", f"Files will be saved to: {save_path}")
            self.save_btn.configure(text='Save Successful', font=('Bradley Hand ITC', 12), command=lambda: None)
            self.reset_save_btn.pack(side="left", padx=5, pady=5, expand=True)  # Show the reset save button
            self.update_folder_listbox()
        else:
            messagebox.showwarning("Save Path", "No directory selected. Files will not be saved.")

    def reset_save(self):
        global save_path
        save_path = None
        self.save_btn.configure(text='Save', font=('TkDefaultFont', 10), command=self.save_path)
        self.reset_save_btn.pack_forget()  # Hide the reset save button
        messagebox.showinfo("Reset Save", "Save path reset")
        self.folder_listbox.delete("1.0", "end")

    def analyze(self):
        missing_requirements = []

        if self.master.calibration_factor is None:
            missing_requirements.append("Calibration")

        if save_path is None:
            missing_requirements.append("Save Path")

        if missing_requirements:
            messagebox.showwarning("Missing Requirements", f"Please complete the following before analysis: {', '.join(missing_requirements)}")
            return

        global skala
        skala = self.master.calibration_factor

        # Open file dialog to select image for analysis
        Tk().withdraw()
        cesta_k_obrazku = filedialog.askopenfilename()
        if not cesta_k_obrazku:
            return
        body.clear()
        obrazok = cv2.imread(cesta_k_obrazku)
        obrazok = cv2.cvtColor(obrazok, cv2.COLOR_BGR2RGB)

        fig, ax = plt.subplots()
        ax.imshow(obrazok)

        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()

        # Calculate angles and distances
        data = []
        data_souradnice = []
        if len(body) >= 3:

             # Calculation of DO
            bod2 = np.array(body[2])
            bod5 = np.array(body[5])
            bod9 = np.array(body[9])
            bod7 = np.array(body[7])
            bod45 = vypocet_bodu45(bod2, bod9, bod7)
            bod55 = vypocet_bodu55(bod5, bod45, bod7)
            DO = vypocet_vzdialenosti_DO(bod5, bod55, skala)
            data.append(['Vzdialenos DO', f'{DO:.4f}'])
        if len(body) >= 3:
       
            # Výpoèet vzdialenosti
            vzdialenostA = vypocet_vzdialenosti(body[4], body[6], skala)
            data.append(['Dlzka A', f'{vzdialenostA:.4f}'])
            vzdialenostB = vypocet_vzdialenosti(body[3], body[4], skala)
            data.append(['Dlzka B', f'{vzdialenostB:.4f}'])
            vzdialenostC = vypocet_vzdialenosti(body[5], body[6], skala)
            data.append(['Dlzka C', f'{vzdialenostC:.4f}'])
            vzdialenostD = vypocet_vzdialenosti(body[13], body[17], skala)
            data.append(['Dlzka D', f'{vzdialenostD:.4f}'])
            vnutornadlzka = vypocet_vzdialenosti(body[3], body[16], skala)
            data.append(['Inner length', f'{vnutornadlzka:.4f}'])
            vnutornasirka = vypocet_vzdialenosti(body[9], body[15], skala)
            data.append(['vnutornasirka', f'{vnutornasirka:.4f}'])
            radialfield = vypocet_vzdialenosti(body[2], body[9], skala)
            data.append(['radialfield', f'{radialfield:.4f}'])
            predlaketnyC = vypocet_vzdialenosti(body[6], body[11], skala)

        if len(body) >= 4:
            uhol_A1 = vypocet_uhla(body[4], body[3], body[6])
            data.append(['Uhol A1', f'{uhol_A1:.4f}'])
            uhol_A4 = vypocet_uhla(body[6], body[3], body[7])
            data.append(['Uhol A4', f'{uhol_A4:.4f}'])
            uhol_B3 = vypocet_uhla(body[3], body[6], body[5])
            data.append(['Uhol B3', f'{uhol_B3:.4f}'])
            uhol_B4 = vypocet_uhla(body[3], body[6], body[7])
            data.append(['Uhol B4', f'{uhol_B4:.4f}'])
            uhol_D7 = vypocet_uhla(body[6], body[5], body[15])
            data.append(['Uhol D7', f'{uhol_D7:.4f}'])
            uhol_E9 = vypocet_uhla(body[8], body[7], body[12])
            data.append(['Uhol E9', f'{uhol_E9:.4f}'])
            uhol_G7 = vypocet_uhla(body[5], body[15], body[6])
            data.append(['Uhol G7', f'{uhol_G7:.4f}'])
            uhol_G18 = vypocet_uhla(body[14], body[15], body[16])
            data.append(['Uhol G18', f'{uhol_G18:.4f}'])
            uhol_H12 = vypocet_uhla(body[13], body[12], body[14])
            data.append(['Uhol H12', f'{uhol_H12:.4f}'])
            uhol_J10 = vypocet_uhla(body[8], body[11], body[12])
            data.append(['Uhol J10', f'{uhol_J10:.4f}'])
            uhol_J16 = vypocet_uhla(body[10], body[11], body[20])
            data.append(['Uhol J16', f'{uhol_J16:.4f}'])
            uhol_K19 = vypocet_uhla(body[14], body[13], body[16])
            data.append(['Uhol K19', f'{uhol_K19:.4f}'])
            uhol_L13 = vypocet_uhla(body[7], body[9], body[8])
            data.append(['Uhol L13', f'{uhol_L13:.4f}'])
            uhol_M17 = vypocet_uhla(body[9], body[10], body[20])
            data.append(['Uhol M17', f'{uhol_M17:.4f}'])
            uhol_N23 = vypocet_uhla(body[11], body[20], body[19])
            data.append(['Uhol N23', f'{uhol_N23:.4f}'])
            uhol_O26 = vypocet_uhla(body[17], body[16], body[18])
            data.append(['Uhol O26', f'{uhol_O26:.4f}'])
            uhol_Q21 = vypocet_uhla(body[13], body[18], body[19])
            data.append(['Uhol Q21', f'{uhol_Q21:.4f}'])

            body_polygonu = [body[i] for i in [3,7,9,20,19,18,17,16,15,14,5,4]]
            plocha = vypocet_plochy_polygonu(body_polygonu,skala)
            data.append(['Area 6', f'{plocha:.4f}'])
        
            Cubital_index = vzdialenostA / vzdialenostB
            data.append(['Cubital index:', f'{Cubital_index:.4f}'])
            Preubital_index = predlaketnyC / predlaketnyM
            data.append(['Preubital index:', f'{Preubital_index:.4f}'])
            Dumb_bell_index = cinkovyC / cinkovyM
            data.append(['Dumb-bell_index', f'{Dumb_bell_index:.4f}'])               
            Radial_index = aR / bR
            data.append(['Radial index', f'{Radial_index:.4f}'])
            # Výpoèet aR a bR
            bod2 = np.array(body[2])
            bod5 = np.array(body[5])
            bod9 = np.array(body[9])
            bod40 = vypocet_bodu40(bod2, bod5, bod9)
            aR = vypocet_vzdialenosti(bod2, bod40, skala)
            data.append(['Dåžka aR', f'{aR:.4f}'])
            bR = vypocet_vzdialenosti(bod9, bod40, skala)
            data.append(['Dåžka bR', f'{bR:.4f}'])
            data.append(['predlaketnyC', f'{predlaketnyC:.4f}'])
            predlaketnyM = vypocet_vzdialenosti(body[10], body[12], skala)
            data.append(['predlaketnyM', f'{predlaketnyM:.4f}'])
            cinkovyC = vypocet_vzdialenosti(body[3], body[6], skala)
            data.append(['cinkovyC', f'{cinkovyC:.4f}'])
            cinkovyM = vypocet_vzdialenosti(body[7], body[8], skala)
            data.append(['cinkovyM', f'{cinkovyM:.4f}'])


            for i, (x, y) in enumerate(body):
                print(f"Bod {i}: x = {x}, y = {y}")
            for i, (x, y) in enumerate(body):
                data_souradnice.append([f"Súradnice bodu {i} x", f"{x}", f"{y}", f"Súradnice bodu {i} y"])
            
            

        # Vytvorenie DataFrame a export do Excelu data_souradnice.append([f"Súradnice bodu {i} y", f"{y}"])
        df_data = pd.DataFrame(data, columns=['Parameter', 'Hodnota'])
        df_souradnice = pd.DataFrame(data_souradnice, columns=['Parameter', 'Hodnota x','Hodnota y' , 'Parameter'])

       # Check if file already exists and add a number to the end of the file name if it does
        i = 1
        while os.path.exists(os.path.join(save_path, f'Front{i}.xlsx')):
            i += 1

        df_data.to_excel(os.path.join(save_path, f'Front{i}.xlsx'), index=False)
   
   
        while os.path.exists(os.path.join(save_path, f'GeometrickaF{i}.xlsx')):
            i += 1

        df_souradnice.to_excel(os.path.join(save_path, f'GeometrickaF{i}.xlsx'), index=False)


        messagebox.showinfo("Analysis Complete", f"Analysis results saved as Back{i}.xlsx and GeometrickaB{i}.xlsx")
        print("Analysis started...")
      
       # Extract the file name from the path and add it to the listbox
        nazov_obrazku = os.path.basename(cesta_k_obrazku)
        self.analyzed_listbox.insert("end", nazov_obrazku)

    def recalibrate(self):
        self.reset()
        messagebox.showinfo("Calibration", "Calibration reset")

    def reset(self):
        global skala
        skala = None
        self.master.calibration_factor = None
        self.calibration_btn.configure(text='Calibration', font=('TkDefaultFont', 10), command=self.calibrate)
        self.recalibrate_btn.pack_forget()  # Hide the recalibrate button

    def update_folder_listbox(self):
        if save_path:
            self.folder_listbox.delete("1.0", "end")
            for file_name in os.listdir(save_path):
                self.folder_listbox.insert("end", file_name + "\n")

    def back_to_main(self, master):
        master.show_textbox()

    def open_help(self):
        help_path = os.path.join("Documentation", "Back.pdf")
        if os.path.exists(help_path):
            webbrowser.open(help_path)
        else:
            print("Help file not found.")
class Backwing(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # Initialize calibration factor and save path
        master.calibration_factor = None
        global save_path
        save_path = None

        # Replace main content frame with Frontwing content
        master.content_frame.destroy()
        
        master.content_frame = customtkinter.CTkFrame(master)
        master.content_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        
        # Create frames for buttons
        frame1 = customtkinter.CTkFrame(master.content_frame)
        frame1.pack(fill="both", expand=True)

        frame2 = customtkinter.CTkFrame(master.content_frame)
        frame2.pack(fill="both", expand=True)

        frame3 = customtkinter.CTkFrame(master.content_frame)
        frame3.pack(fill="both", expand=True)

        frame4 = customtkinter.CTkFrame(master.content_frame)
        frame4.pack(fill="both", expand=True)

        # Add buttons to frames
        self.calibration_btn = customtkinter.CTkButton(frame1, text='Calibration', command=self.calibrate)
        self.calibration_btn.pack(side="left", padx=5, pady=5, expand=True)

        self.recalibrate_btn = customtkinter.CTkButton(frame1, text='Recalibrate', command=self.recalibrate)
        self.recalibrate_btn.pack(side="left", padx=5, pady=5, expand=True)
        self.recalibrate_btn.pack_forget()  # Hide the recalibrate button initially

        self.save_btn = customtkinter.CTkButton(frame2, text='Save', command=self.save_path)
        self.save_btn.pack(side="left", padx=5, pady=5, expand=True)

        self.reset_save_btn = customtkinter.CTkButton(frame2, text='Reset Save', command=self.reset_save)
        self.reset_save_btn.pack(side="left", padx=5, pady=5, expand=True)
        self.reset_save_btn.pack_forget()  # Hide the reset save button initially

        self.analysis_btn = customtkinter.CTkButton(frame3, text='Backwing analysis', command=self.analyze)
        self.analysis_btn.pack(side="left", padx=5, pady=5, expand=True)

        self.back_btn = customtkinter.CTkButton(frame4, text='Back', command=lambda: self.back_to_main(master))
        self.back_btn.pack(side="left", padx=5, pady=5, expand=True)

        # Create the right sidebar frame
        self.right_sidebar_frame = customtkinter.CTkFrame(master, width=200, corner_radius=0)
        self.right_sidebar_frame.grid(row=0, column=2, rowspan=4, sticky="nsew")
        self.right_sidebar_frame.grid_rowconfigure(9, weight=1)

        # Add the title to the right sidebar
        self.right_title_label = customtkinter.CTkLabel(self.right_sidebar_frame, text="Save location", font=("Arial", 16, "bold"))
        self.right_title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Add a listbox to display folder contents
        self.folder_listbox = customtkinter.CTkTextbox(self.right_sidebar_frame, height=200)
        self.folder_listbox.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="nsew")

        # Add the title for analyzed pictures
        self.analyzed_title_label = customtkinter.CTkLabel(self.right_sidebar_frame, text="Analysed pictures", font=("Arial", 16, "bold"))
        self.analyzed_title_label.grid(row=2, column=0, padx=20, pady=(20, 10))

        # Add a listbox to display analyzed picture names
        self.analyzed_listbox = customtkinter.CTkTextbox(self.right_sidebar_frame, height=200)
        self.analyzed_listbox.grid(row=3, column=0, padx=20, pady=(10, 10), sticky="nsew")

    def calibrate(self):
        global skala
        Tk().withdraw()
        cesta_k_obrazku = filedialog.askopenfilename()
        if not cesta_k_obrazku:
            return
        body.clear()
        obrazok = cv2.imread(cesta_k_obrazku)
        obrazok = cv2.cvtColor(obrazok, cv2.COLOR_BGR2RGB)

        fig, ax = plt.subplots()
        ax.imshow(obrazok)

        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()

        if len(body) >= 2:
            # Výpoèet škály na základe vzdialenosti medzi prvými dvoma bodmi
            skala = 1 / vypocet_vzdialenosti(body[0], body[1], 1)
            self.master.calibration_factor = skala
            self.calibration_btn.configure(text='Successful Calibration', font=('Bradley Hand ITC', 12), command=lambda: None)
            self.recalibrate_btn.pack(side="left", padx=5, pady=5, expand=True)  # Show the recalibrate button
            print(f"Calibration factor set to {self.master.calibration_factor} px to mm")
        else:
            print("Not enough points for calibration.")

    def save_path(self):
        global save_path
        save_path = filedialog.askdirectory()
        if save_path:
            messagebox.showinfo("Save Path", f"Files will be saved to: {save_path}")
            self.save_btn.configure(text='Save Successful', font=('Bradley Hand ITC', 12), command=lambda: None)
            self.reset_save_btn.pack(side="left", padx=5, pady=5, expand=True)  # Show the reset save button
            self.update_folder_listbox()
        else:
            messagebox.showwarning("Save Path", "No directory selected. Files will not be saved.")

    def reset_save(self):
        global save_path
        save_path = None
        self.save_btn.configure(text='Save', font=('TkDefaultFont', 10), command=self.save_path)
        self.reset_save_btn.pack_forget()  # Hide the reset save button
        messagebox.showinfo("Reset Save", "Save path reset")
        self.folder_listbox.delete("1.0", "end")

    def analyze(self):
        missing_requirements = []

        if self.master.calibration_factor is None:
            missing_requirements.append("Calibration")

        if save_path is None:
            missing_requirements.append("Save Path")

        if missing_requirements:
            messagebox.showwarning("Missing Requirements", f"Please complete the following before analysis: {', '.join(missing_requirements)}")
            return
        global skala
        skala = self.master.calibration_factor

        # Open file dialog to select image for analysis
        Tk().withdraw()
        cesta_k_obrazku = filedialog.askopenfilename()
        if not cesta_k_obrazku:
            return
        body.clear()
        obrazok = cv2.imread(cesta_k_obrazku)
        obrazok = cv2.cvtColor(obrazok, cv2.COLOR_BGR2RGB)

        fig, ax = plt.subplots()
        ax.imshow(obrazok)

        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()

        # Calculate angles and distances
        data = []
        data_souradnice = []
        if len(body) >= 3:
            # Calculate distances

            vzdialenostA = vypocet_vzdialenosti(body[0], body[1], skala)
            data.append(['Dlzka A', f'{vzdialenostA:.4f}'])
            vzdialenostB = vypocet_vzdialenosti(body[1], body[2], skala)
            data.append(['Dlzka B', f'{vzdialenostB:.4f}'])
            vzdialenostC = vypocet_vzdialenosti(body[2], body[3], skala)
            data.append(['Dlzka C', f'{vzdialenostC:.4f}'])
            vzdialenostD = vypocet_vzdialenosti(body[3], body[4], skala)
            data.append(['Dlzka D', f'{vzdialenostD:.4f}'])
            vzdialenostE = vypocet_vzdialenosti(body[2], body[4], skala)
            data.append(['Dlzka E', f'{vzdialenostE:.4f}'])
            vnutornadlzka = vypocet_vzdialenosti(body[1], body[3], skala)
            data.append(['Inner length', f'{vnutornadlzka:.4f}'])
            vnutornasirka = vypocet_vzdialenosti(body[0], body[4], skala)
            data.append(['Inner width', f'{vnutornasirka:.4f}'])

        if len(body) >= 4:
            uhol_A1 = vypocet_uhla(body[2], body[1], body[2])
            data.append(['Uhol X1', f'{uhol_A1:.4f}'])
            uhol_A2 = vypocet_uhla(body[4], body[3], body[4])
            data.append(['Uhol X2', f'{uhol_A2:.4f}'])

            for i, (x, y) in enumerate(body):
                print(f"Bod {i}: x = {x}, y = {y}")
            for i, (x, y) in enumerate(body):
                data_souradnice.append([f"Súradnice bodu {i} x", f"{x}", f"Súradnice bodu {i} y", f"{y}"])

        df_data = pd.DataFrame(data, columns=['Parameter', 'Hodnota'])
        df_souradnice = pd.DataFrame(data_souradnice, columns=['Parameter', 'Hodnota x','Hodnota y' , 'Parameter'])

        # Check if file already exists and add a number to the end of the file name if it does
        i = 1
        while os.path.exists(os.path.join(save_path, f'Back{i}.xlsx')):
            i += 1

        df_data.to_excel(os.path.join(save_path, f'Back{i}.xlsx'), index=False)

        while os.path.exists(os.path.join(save_path, f'GeometrickaB{i}.xlsx')):
            i += 1

        df_souradnice.to_excel(os.path.join(save_path, f'GeometrickaB{i}.xlsx'), index=False)

        messagebox.showinfo("Analysis Complete", f"Analysis results saved as Back{i}.xlsx and GeometrickaB{i}.xlsx")
        print("Analysis started...")
       # Extract the file name from the path and add it to the listbox
        nazov_obrazku = os.path.basename(cesta_k_obrazku)
        self.analyzed_listbox.insert("end", nazov_obrazku)

    def recalibrate(self):
        self.reset()
        messagebox.showinfo("Calibration", "Calibration reset")

    def reset(self):
        global skala
        skala = None
        self.master.calibration_factor = None
        self.calibration_btn.configure(text='Calibration', font=('TkDefaultFont', 10), command=self.calibrate)
        self.recalibrate_btn.pack_forget()  # Hide the recalibrate button

    def update_folder_listbox(self):
        if save_path:
            self.folder_listbox.delete("1.0", "end")
            for file_name in os.listdir(save_path):
                self.folder_listbox.insert("end", file_name + "\n")

    def back_to_main(self, master):
        master.show_textbox()


    def open_help(self):
        help_path = os.path.join("Documentation", "Back.pdf")
        if os.path.exists(help_path):
            webbrowser.open(help_path)
        else:
            print("Help file not found.")
class Excel(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


        # Replace main content frame with Frontwing content
        master.content_frame.destroy()
        
        master.content_frame = customtkinter.CTkFrame(master)
        master.content_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        
        # Create frames for buttons
        frame1 = customtkinter.CTkFrame(master.content_frame)
        frame1.pack(fill="both", expand=True)

        frame2 = customtkinter.CTkFrame(master.content_frame)
        frame2.pack(fill="both", expand=True)

        frame3 = customtkinter.CTkFrame(master.content_frame)
        frame3.pack(fill="both", expand=True)

        frame4 = customtkinter.CTkFrame(master.content_frame)
        frame4.pack(fill="both", expand=True)

        # Add buttons to frames
        self.ExcelF_btn = customtkinter.CTkButton(frame1, text='Front excel merger', command=self.Frontexcel)
        self.ExcelF_btn.pack(side="left", padx=5, pady=5, expand=True)

        self.ExcelB_btn = customtkinter.CTkButton(frame1, text='Back excel merger', command=self.Backexcel)
        self.ExcelB_btn.pack(side="left", padx=5, pady=5, expand=True)

        self.PropF_btn = customtkinter.CTkButton(frame2, text='Posterior probability (Frontwing)',command=self.PPFront)
        self.PropF_btn.pack(side="left", padx=5, pady=5, expand=True)

        self.PropB_btn = customtkinter.CTkButton(frame2, text='Posterior probability (Backwing)', command=self.PPBack)
        self.PropB_btn.pack(side="left", padx=5, pady=5, expand=True)


        self.back_btn = customtkinter.CTkButton(frame4, text='Back', command=lambda: self.back_to_main(master))
        self.back_btn.pack(side="left", padx=5, pady=5, expand=True)

    def Frontexcel(self):
            root = Tk()
            root.withdraw()  # Hide the main window
            file_paths = filedialog.askopenfilenames(title="Vyber Excel subory", filetypes=[("Excel subory", "*.xlsx")])

            # List of parameters for the 'Parameter' column
            parameters = [
                "Leingh A", "Leingh B", "Leingh C", "Leingh D", "Inner length ", "Inner width", "Radialfield",
                "Angle A1", "Angle A4", "Angle B3", "Angle B4", "Angle D7", "Angle E9", "Angle G7", "Angle G18", "Angle H12",
               "Angle J10", "Angle J16", "Angle K19", "Angle L13", "Angle M17", "Angle N23", "Angle O26", "Angle Q21", "Area 6", "Cubital index", "Preubital index", "Dumb-bell_index"
               "Radial index", "Leingh aR", "Leingh bR", "Precubital numerator", "Precubital denominator", "Cubital numerator","Cubital denominator"
            ]

            # Initialize an empty DataFrame for the result table
            result_df = pd.DataFrame()

            # Add 'Parameter' column to the result DataFrame
            result_df['Parameter'] = parameters

            # Counter for Hodnota columns
            hodnota_counter = 1

            # For each selected Excel file
            for file in file_paths:
                # Read the Excel file into a DataFrame
                df = pd.read_excel(file)
    
                # Check if 'Hodnota' column exists or any column starting with 'Hodnota'
                hodnota_columns = [col for col in df.columns if col.startswith('Hodnota')]
    
                for col in hodnota_columns:
                    # Convert 'Hodnota' column to string, replace commas with dots, and convert to float
                    df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
        
                    # Select only the 'Hodnota' column
                    values = df[col]
        
                    # Add the column to the result DataFrame with a new name
                    result_df[f'Hodnota {hodnota_counter}'] = values
                    hodnota_counter += 1

            # Calculate the average for each row 
            result_df['Average'] = result_df.iloc[:, 1:].mean(axis=1)

            # Calculate the median for each row 
            result_df['Median'] = result_df.iloc[:, 1:-1].median(axis=1)

            # Function to generate a unique file name if 'vysledna tabu¾ka' already exists
            def generate_unique_filename(base_name, extension):
                counter = 1
                new_name = f"{base_name}.{extension}"
                while os.path.exists(new_name):
                    new_name = f"{base_name} {counter}.{extension}"
                    counter += 1
                return new_name

            # Generate a unique file name for the result file
            result_file_name = generate_unique_filename("vysledna tabu¾ka", "xlsx")

            # Save the result DataFrame to a new Excel file with a unique name
            result_df.to_excel(result_file_name, index=False)

            print(f"The merged table with average and median calculations has been saved to '{result_file_name}'.")

    def Backexcel(self):
        # Open dialog to select files
        root = Tk()
        root.withdraw()  # Hide the main window
        file_paths = filedialog.askopenfilenames(title="Vyber Excel subory", filetypes=[("Excel subory", "*.xlsx")])

        # List of parameters for the 'Parameter' column
        parameters = [
            "Leingh A", "Leingh B", "Leingh C", "Leingh D", "Leingh E", "Inner length ", "Inner width",
            "Angle X1", "Angle X2"
        ]

        # Initialize an empty DataFrame for the result table
        result_df = pd.DataFrame()

        # Add 'Parameter' column to the result DataFrame
        result_df['Parameter'] = parameters

        # Counter for Hodnota columns
        hodnota_counter = 1

        # For each selected Excel file
        for file in file_paths:
            # Read the Excel file into a DataFrame
            df = pd.read_excel(file)
    
            # Check if 'Hodnota' column exists or any column starting with 'Hodnota'
            hodnota_columns = [col for col in df.columns if col.startswith('Hodnota')]
    
            for col in hodnota_columns:
                # Convert 'Hodnota' column to string, replace commas with dots, and convert to float
                df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
        
                # Select only the 'Hodnota' column
                values = df[col]
        
                # Add the column to the result DataFrame with a new name
                result_df[f'Hodnota {hodnota_counter}'] = values
                hodnota_counter += 1

        # Calculate the average for each row 
        result_df['Average'] = result_df.iloc[:, 1:].mean(axis=1)

        # Calculate the median for each row 
        result_df['Median'] = result_df.iloc[:, 1:-1].median(axis=1)

        # Function to generate a unique file name if 'vysledna tabu¾ka' already exists
        def generate_unique_filename(base_name, extension):
            counter = 1
            new_name = f"{base_name}.{extension}"
            while os.path.exists(new_name):
                new_name = f"{base_name} {counter}.{extension}"
                counter += 1
            return new_name

        # Generate a unique file name for the result file
        result_file_name = generate_unique_filename("vysledna tabu¾ka", "xlsx")

        # Save the result DataFrame to a new Excel file with a unique name
        result_df.to_excel(result_file_name, index=False)

        print(f"The merged table with average and median calculations has been saved to '{result_file_name}'.")
    def PPFront(self):
        root = Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(title="Vyber Excel súbor", filetypes=[("Excel súbory", "*.xlsx")])

        # Read the selected Excel file into a DataFrame
        df = pd.read_excel(file_path)

        # Check if 'Hodnota' column exists or any column containing 'Hodnota'
        hodnota_columns = [col for col in df.columns if 'Hodnota' in col]

        # Initialize an empty DataFrame for the result table
        result_df = pd.DataFrame()

        # Counter for Hodnota columns
        hodnota_counter = 1

        for col in hodnota_columns:
            # Convert 'Hodnota' column to string, replace commas with dots, and convert to float
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
    
            # Select only the 'Hodnota' column
            values = df[col]
    
            # Add the column to the result DataFrame with a new name
            result_df[f'Hodnota {hodnota_counter}'] = values
            hodnota_counter += 1

        # Calculate the average for each row and add it as a new column
        result_df['Aritmetický priemer'] = result_df.iloc[:, 0:].mean(axis=1)

        # Ensure that Average values use decimal points instead of commas
        result_df['Aritmetický priemer'] = result_df['Aritmetický priemer'].astype(str).str.replace(',', '.').astype(float)

        # Define the standard values (mean vectors) for six standards
        standard_values_list = [
            np.array([0.116805, 0.548275, 0.22746, 0.90528, 2.06897, 4.686575, 2.10432, 3.50466, 22.141325, 31.399765, 79.878295, 111.209145, 100.96872, 22.53493, 22.489505, 96.50631, 17.27989, 53.85102, 93.43829, 76.12653, 11.186255, 42.425165, 98.95303, 36.16565, 36.741125, 5.74794, 2.44164, 2.75657, 0.9891, 1.27707]),
            np.array([0.121695, 0.565125, 0.235245, 0.887885, 2.0184, 4.607785, 2.062155, 3.4271, 20.40599, 30.640405, 77.409375, 109.5146, 99.396765, 23.093875, 23.165735, 91.49537, 19.81198, 52.137775, 97.86597, 80.50859, 12.10859, 44.451265, 101.00166, 36.32277, 35.66527, 5.50519, 2.446955, 2.7721, 0.999295, 1.323295]),
            np.array([0.12003, 0.615995, 0.223125, 0.907685, 2.039805, 4.6678, 2.074945, 3.4826, 22.837265, 29.25817, 75.757675, 111.29614, 98.223095, 23.782165, 23.55976, 93.640605, 19.912605, 55.15726, 96.398785, 78.431405, 12.46036, 40.912655, 98.498315, 36.141435, 35.36121, 5.631515, 2.80416, 2.668715, 1.04046, 1.318125]),
            np.array([0.16025, 0.59513, 0.200455, 0.89068, 2.042745, 4.584875, 2.04607, 3.398045,24.82496, 29.41571, 74.46441, 112.972825, 96.706695, 24.54987, 23.594055, 95.394085, 19.52643, 54.33357, 97.406485, 78.20913, 11.613085, 42.59282, 99.809745, 36.374985, 35.17757, 5.480315, 3.04638, 2.66261, 1.04191, 1.25366]),
            np.array([0.10668, 0.589465, 0.19675, 0.878915, 1.98793, 4.476185, 1.98581, 3.44876, 22.5495, 30.68187, 73.29852, 105.933095, 96.589955, 21.559555, 23.83059, 93.709765, 19.170675, 52.06361, 100.56371, 78.826175, 11.452585, 41.583635, 102.631755, 39.498025, 36.892665, 5.234845, 3.034295, 2.781035, 0.972395, 1.29448]),
            np.array([0.106905, 0.55951, 0.2381, 0.906555, 1.990505, 4.48667, 2.07348, 3.38038, 21.217785, 30.3252, 75.885185, 110.250405, 99.36358, 23.5714, 24.2152, 92.50064, 19.089385, 53.30625, 93.622445, 79.33063, 13.22365, 41.71043, 95.91285, 35.94177, 35.715755, 5.37821, 2.38587, 2.651, 1.04161, 1.375695])
        ]

        # Extract the average values from the result_df (only first 30 values)
        average_values = result_df['Aritmetický priemer'].values[:30]

        # Calculate the covariance matrix of the standard values (assuming identity matrix for simplicity)
        cov_matrix = np.identity(len(standard_values_list[0]))
        inv_cov_matrix = np.linalg.inv(cov_matrix)

        # Calculate Mahalanobis distances for all six standards
        mahalanobis_distances = []
        for i, standard_values in enumerate(standard_values_list):
            mahalanobis_distance = distance.mahalanobis(average_values, standard_values, inv_cov_matrix)
            mahalanobis_distances.append(mahalanobis_distance)
            print(f"Mahalanobis distance for standard {i+1}: {mahalanobis_distance}")

        # Calculate exponentials of Mahalanobis distances
        exp_values = [np.exp(-0.5 * d**2) for d in mahalanobis_distances]

        # Calculate the sum of exponentials
        sum_exp_values = sum(exp_values)

        # Calculate Posterior probabilities
        posterior_probabilities = [exp_val / sum_exp_values for exp_val in exp_values]

        # Print Posterior probabilities with specific labels
        labels = ["Value of AMC SOK", "Value of HRA", "Value of AMC MLY", "Value of AMC MAM", "Value of AMC KIS", "Value of AMC STJ"]
        values = []
        for i in range(6):
            values.append(f"{labels[i]}: {posterior_probabilities[i]*100:.2f}%")

        # Show the values in a message box
        messagebox.showinfo("Values", "\n".join(values))
    def PPBack(self):
        root = Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(title="Vyber Excel súbor", filetypes=[("Excel súbory", "*.xlsx")])

        # Read the selected Excel file into a DataFrame
        df = pd.read_excel(file_path)

        # Check if 'Hodnota' column exists or any column containing 'Hodnota'
        hodnota_columns = [col for col in df.columns if 'Hodnota' in col]

        # Initialize an empty DataFrame for the result table
        result_df = pd.DataFrame()

        # Counter for Hodnota columns
        hodnota_counter = 1

        for col in hodnota_columns:
            # Convert 'Hodnota' column to string, replace commas with dots, and convert to float
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

            # Select only the 'Hodnota' column
            values = df[col]

            # Add the column to the result DataFrame with a new name
            result_df[f'Hodnota {hodnota_counter}'] = values
            hodnota_counter += 1

        # Calculate the average for each row and add it as a new column
        result_df['Aritmetický priemer'] = result_df.iloc[:, 0:].mean(axis=1)

        # Ensure that Average values use decimal points instead of commas
        result_df['Aritmetický priemer'] = result_df['Aritmetický priemer'].astype(str).str.replace(',', '.').astype(float)

        # Define the standard values (mean vectors) for six standards(2023)
        standard_values_list = [
            np.array([1.6398, 1.3172, 1.4681, 0.3587, 1.3867, 2.7831, 1.5264, 25.5513, 69.9947]),
            np.array([1.5954, 1.2732, 1.4162, 0.3433, 1.3559, 2.6865, 1.4729, 25.4025, 72.8911]),
            np.array([1.6397, 1.3024, 1.4528, 0.3319, 1.4093, 2.7508, 1.5216, 26.3676, 76.0481]),
            np.array([1.5846, 1.2643, 1.4408, 0.3452, 1.3499, 2.7031, 1.4884, 26.0195, 68.0523]),
            np.array([1.5719, 1.2291, 1.4156, 0.3375, 1.3469, 2.6413, 1.4379, 25.6192, 71.4872]),
            np.array([1.5687, 1.2375, 1.3583, 0.3442, 1.3047, 2.5924, 1.4585, 27.2262, 73.9209])
        ]

        # Extract the average values from the result_df (only first 9 values)
        average_values = result_df['Aritmetický priemer'].values[:9]

        # Calculate the covariance matrix of the standard values (assuming identity matrix for simplicity)
        cov_matrix = np.identity(len(standard_values_list[0]))
        inv_cov_matrix = np.linalg.inv(cov_matrix)

        # Calculate Mahalanobis distances for all six standards
        mahalanobis_distances = []
        for i, standard_values in enumerate(standard_values_list):
            mahalanobis_distance = distance.mahalanobis(average_values, standard_values, inv_cov_matrix)
            mahalanobis_distances.append(mahalanobis_distance)
            print(f"Mahalanobis distance for standard {i+1}: {mahalanobis_distance}")

        # Calculate exponentials of Mahalanobis distances
        exp_values = [np.exp(-0.5 * d**2) for d in mahalanobis_distances]

        # Calculate the sum of exponentials
        sum_exp_values = sum(exp_values)

        # Calculate Posterior probabilities
        posterior_probabilities = [exp_val / sum_exp_values for exp_val in exp_values]

        # Print Posterior probabilities with specific labels
        labels = ["Value of AMC SOK", "Value of HRA", "Value of AMC MLY", "Value of AMC MAM", "Value of AMC KIS", "Value of AMC STJ"]
        values = []
        for i in range(6):
            values.append(f"{labels[i]}: {posterior_probabilities[i]*100:.2f}%")

        # Show the values in a message box
        messagebox.showinfo("Values", "\n".join(values))

    def back_to_main(self, master):
        master.show_textbox()
        master.clear_right_sidebar()

    def open_help(self):
        help_path = os.path.join("Documentation", "ApisVM Script User Manual.pdf")
        if os.path.exists(help_path):
            webbrowser.open(help_path)
        else:
            print("Help file not found.")

if __name__ == "__main__":
    app = App()
    app.mainloop()