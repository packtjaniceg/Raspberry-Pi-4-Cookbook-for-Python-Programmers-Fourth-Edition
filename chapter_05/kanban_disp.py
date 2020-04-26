#!/usr/bin/python3
'''kanban_json.py'''
import os.path
import json
from guizero import App, MenuBar, Text, TextBox, ListBox, PushButton, Box

STAGE = ["TODO", "INPROGRESS", "DONE"]
NONE_SELECTED = {"stage":'', "title":'', "description":''}
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

        self.heading_box = Box(self.app, align="top", width="fill", border=True)
        self.task_box = Box(self.app, align="top", width="fill", border=True, layout="grid")
        self.stage_box = Box(self.app, align="top", width="fill", border=True)
        self.control_box = Box(self.app, align="bottom", height="fill", width="fill", border=True)
        self.stage_list = []
        for stage in STAGE:
            self.stage_list.append(Text(self.heading_box, text=stage, align="left", width="fill"))
        self.todo_list = ListBox(self.task_box, height=200, width=WIDTH/3,
                                 command=self.list_selected_todo, scrollbar=True, grid=[0, 0])
        self.inprogress_list = ListBox(self.task_box, height=200, width=WIDTH/3,
                                       command=self.list_selected_inprogress,
                                       scrollbar=True, grid=[1, 0])
        self.done_list = ListBox(self.task_box, height=200, width=WIDTH/3,
                                 command=self.list_selected_done, scrollbar=True, grid=[2, 0])
        self.lists = [self.todo_list, self.inprogress_list, self.done_list]
        self.regress_btn = PushButton(self.stage_box, text="Back", align="left", width="fill")
        self.stage = Text(self.stage_box, align="left", width="fill")
        self.progress_btn = PushButton(self.stage_box, text="Next", align="left", width="fill")
        self.title = Text(self.app, width="fill", align="top")
        self.description = TextBox(self.app, width="fill", align="bottom", height="fill",
                                   multiline=True, scrollbar=True)
        self.add_btn = PushButton(self.control_box, text="New", align="left", width="fill")
        self.remove_btn = PushButton(self.control_box, text="Delete", align="left", width="fill")
        #Set defaults
        self.file_name = None
        self.data = {STAGE[0]:[], STAGE[1]:[], STAGE[2]:[]}
        self.selected = NONE_SELECTED
        self.app.tk.bind("<Configure>", self.resize_callback)
        self.app.display()

    def resize_callback(self):
        '''Resize list boxes'''
        for i in self.lists:
            i.width = self.app.width/3

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
                self.load_tasks()

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

    def load_tasks(self):
        '''Load the tasks into each of the ListBoxes'''
        for i, stage in enumerate(STAGE):
            self.lists[i].clear()
            for task in self.data[stage]:
                self.lists[i].append(task["title"])

    def list_selected_todo(self, title):
        '''called from todo_list'''
        self.list_selected(STAGE[0], title)

    def list_selected_inprogress(self, title):
        '''called from inprogress_list'''
        self.list_selected(STAGE[1], title)

    def list_selected_done(self, title):
        '''called from done_list'''
        self.list_selected(STAGE[2], title)

    def list_selected(self, stage, title):
        '''find details of selected task'''
        for task in self.data[stage]:
            if title in task["title"]:
                self.selected = {"stage":stage,
                                 "title":title,
                                 "description":task["description"]}
                self.load_selected()

    def load_selected(self):
        '''load selected task on GUI'''
        self.stage.value = self.selected.get("stage", "")
        self.title.value = self.selected.get("title", "")
        self.description.value = self.selected.get("description", "")

myKanbanApp = GuiApp()
#End
