#!/usr/bin/python3
'''kanban_json.py'''
import os.path
import json
from guizero import App, MenuBar, Text
from pprint import pprint

STAGE = ["TODO", "INPROGRESS", "DONE"]
WIDTH = 650

class GuiApp():
    '''Main GUI'''
    def __init__(self):
        '''Class contructor'''
        self.app = App(title="Kanban", width=WIDTH)
        MenuBar(self.app,
                toplevel=["File"],
                options=[
                    [["Open", self.file_open],
                     ["Save", self.file_save],
                     ["Exit", self.app.destroy]]
                ])
        self.project_name = Text(self.app, text="Open a new project or add new tasks...")
        #Set defaults
        self.file_name = None
        self.data = {STAGE[0]:[], STAGE[1]:[], STAGE[2]:[]}
        self.app.display()

    def file_open(self):
        '''Open JSON file and load into data'''
        self.file_name = self.app.select_file(
                                title="Select your task file",
                                folder=".",
                                filetypes=[["JSON documents", "*.json"],
                                           ["All files", "*.*"]])
        if self.file_name != '':
            self.project_name.value = os.path.basename(self.file_name).split(".")[0]
            with open(self.file_name) as json_file:
                self.data = json.load(json_file)
                pprint(self.data)

    def file_save(self):
        '''Save the data in JSON format'''
        self.file_name = self.app.select_file(
                                title="Save a copy of your tasks",
                                folder=".",
                                filetypes=[["JSON documents", "*.json"],
                                           ["All files", "*.*"]],
                                save=True)
        if self.file_name != '':
            with open(self.file_name, 'w') as outfile:
                json.dump(self.data, outfile, sort_keys=True, indent=4)
                self.project_name.value = os.path.basename(self.file_name).split(".")[0]

myKanbanApp = GuiApp()
#End
