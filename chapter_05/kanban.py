#!/usr/bin/python3
'''kanban.py'''
import os.path
import json
from guizero import App, MenuBar, Text, TextBox, ListBox, PushButton, Box, Window

STAGE = ["TODO", "INPROGRESS", "DONE"]
NONE_SELECTED = {"stage":'', "title":'', "description":''}
WIDTH = 650

class NewTask():
    '''NewTask GUI'''
    def __init__(self, app, callback):
        '''Class contructor'''
        self.callback = callback
        self.window_new = Window(app, title="Add Task")
        Text(self.window_new, "Add new task title")
        self.title = TextBox(self.window_new, command=self.check_empty,
                             width="fill")
        Text(self.window_new, "Add new task description")
        self.desc_box = Box(self.window_new, align="top",
                            width="fill", height="fill", border=True)
        self.btn_box = Box(self.window_new, align="bottom",
                           width="fill", border=True)
        self.description = TextBox(self.desc_box, command=self.check_empty,
                                   width="fill", height="fill",
                                   multiline=True, scrollbar=True)
        PushButton(self.btn_box, command=self.window_new.destroy,
                   align="left", width="fill", text="Cancel")
        self.add_btn = PushButton(self.btn_box, enabled=False,
                                  align="left", width="fill",
                                  command=self.add_task, text="Add")
        self.window_new.tk.resizable(True, False)
        self.window_new.show()

    def check_empty(self):
        '''disable add button if title and description are empty'''
        if self.title.value != "" and self.description.value != "\n":
            self.add_btn.enable()
        else:
            self.add_btn.disable()

    def add_task(self):
        '''callback with new title and description'''
        self.callback(self.title.value, self.description.value)
        self.window_new.destroy()

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
        self.regress_btn = PushButton(self.stage_box, text="Back", align="left", width="fill",
                                      command=self.regress_task)
        self.stage = Text(self.stage_box, align="left", width="fill")
        self.progress_btn = PushButton(self.stage_box, text="Next", align="left", width="fill",
                                       command=self.progress_task)
        self.title = Text(self.app, width="fill", align="top")
        self.description = TextBox(self.app, width="fill", align="bottom", height="fill",
                                   multiline=True, scrollbar=True, command=self.update_task)
        self.add_btn = PushButton(self.control_box, text="New", align="left",
                                  width="fill", command=self.add_task)
        self.remove_btn = PushButton(self.control_box, text="Delete", align="left",
                                     width="fill", command=self.remove_task)
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

    def add_task(self):
        '''Open NewTask GUI'''
        NewTask(self.app, self.addtask_callback)

    def addtask_callback(self, title, description):
        '''add new task to data'''
        self.data[STAGE[0]].append({"title":title,
                                    "description":description})
        self.selected = {"stage":STAGE[0],
                         "title":title,
                         "description":description}
        self.load_selected()
        self.load_tasks()

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

    def progress_task(self):
        '''move task to next stage'''
        new_stage = self.change_stage(self.selected["stage"])
        self.move_task(self.selected["stage"], new_stage)

    def regress_task(self):
        '''move task to previous stage'''
        new_stage = self.change_stage(self.selected["stage"], direc=-1)
        self.move_task(self.selected["stage"], new_stage)

    def change_stage(self, stage, direc=1):
        '''determine next stage'''
        if direc > 0:
            new_stage = min(STAGE.index(stage)+direc, len(STAGE)-1)
        else:
            new_stage = max(STAGE.index(stage)+direc, 0)
        return STAGE[new_stage]

    def move_task(self, old_stage, new_stage):
        '''move task to new stage'''
        for i, task in enumerate(self.data[old_stage]):
            if self.selected["title"] in task["title"]:
                move_task = self.data[old_stage].pop(i)
                self.data[new_stage].append(move_task)
                self.selected["stage"] = new_stage
                self.load_selected()
        self.load_tasks()

    def remove_task(self):
        '''delete task from data'''
        stage = self.selected["stage"]
        for i, task in enumerate(self.data[stage]):
            if self.selected["title"] in task["title"]:
                self.data[stage].pop(i)
                self.selected = NONE_SELECTED
                self.load_selected()
        self.load_tasks()

    def update_task(self):
        '''update task description'''
        stage = self.selected["stage"]
        if stage != '':
            for i, task in enumerate(self.data[stage]):
                if self.selected["title"] in task["title"]:
                    self.data[stage][i]["description"] = self.description.value

myKanbanApp = GuiApp()
#End
