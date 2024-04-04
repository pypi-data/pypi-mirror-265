from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkEntry
from customtkinter import CTkTextbox
from customtkinter import CTkImage
from customtkinter import CTkOptionMenu
from PIL import Image
import os

class SideBar(CTkScrollableFrame):
    def __init__(self, *args,
                 option_manager: None,
                 home_page: None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.option_manager = option_manager
        self.home_page = home_page
        
        self.render()

    def clear(self):
        self.containerFrame.destroy()

    def refresh(self):
        self.clear()
        self.render()

    def render(self):

        self.containerFrame = CTkFrame(self, fg_color="transparent", bg_color="transparent")
        self.containerFrame.grid(row=0, column=0, padx=(
            0, 0), pady=(0, 0), width=300, sticky="nsew")
        self.containerFrame.grid_columnconfigure(0, weight=1)
        
        selected_graph = self.home_page.graph_selector_value.get()
        
        if (selected_graph == "Best Cost Stacked"):
            self.graph_label = CTkLabel(self.containerFrame, text="Best Cost Stacked")
            self.graph_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
            pass
        elif (selected_graph == "Best Cost by Round"):
            self.graph_label = CTkLabel(self.containerFrame, text="Best Cost by Round")
            self.graph_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
            pass
        elif (selected_graph == "Iteration Table"):
            self.graph_label = CTkLabel(self.containerFrame, text="Iteration Table")
            self.graph_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
            pass
        elif (selected_graph == "Calibrated Parameters"):
            self.graph_label = CTkLabel(self.containerFrame, text="Calibrated Parameters")
            self.graph_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        elif (selected_graph == "Custom CSV"):
            
            info = self.option_manager.get_project_data()
            folder = os.path.join(info['path'], info['name'])
            if not os.path.exists(folder):
                os.makedirs(folder)
                
            # Get all CSV files in the folder and add their paths to a list
            path_list = []
            name_list = []
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith(".csv"):
                        path_list.append(os.path.join(root, file))
                        name_list.append(file.replace(".csv", ""))
            
            if (len(name_list) == 0):
                name_list.append("No files found...")
            else:
                if (self.home_page.selected_csv.get() not in name_list):
                    self.home_page.selected_csv.set(name_list[0])
            
            print("PATH LIST")
            print(path_list)
            print("NAME LIST")
            print(name_list)
            
            self.home_page.csv_file_selector = CTkOptionMenu(self.containerFrame, values=name_list, variable=self.home_page.selected_csv, command=self.home_page.update_graph)
            self.home_page.csv_file_selector.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")