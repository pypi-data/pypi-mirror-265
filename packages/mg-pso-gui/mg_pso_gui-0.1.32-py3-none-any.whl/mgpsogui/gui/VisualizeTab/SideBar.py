from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkEntry
from customtkinter import CTkTextbox
from customtkinter import CTkImage
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

        self.containerFrame = CTkFrame(self)
        self.containerFrame.grid(row=0, column=0, padx=(
            0, 0), pady=(0, 0), sticky="nsew")
        self.containerFrame.grid_columnconfigure((0, 1), weight=1)
        
        selected_graph = self.home_page.graph_selector_value.get()
        
        print("Current Graph: " + selected_graph)
        
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
            pass