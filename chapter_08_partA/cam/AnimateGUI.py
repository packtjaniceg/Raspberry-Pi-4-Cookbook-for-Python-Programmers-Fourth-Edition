#!/usr/bin/python3
'''AnimateGUI.py'''
import time
import os
import tkinter as TK
from tkinter import messagebox
import cam.CameraGUI as camGUI

class SET(camGUI.SET):
    '''Extended Settings class'''
    TL_SIZE = (1920, 1080)
    ENC_PROG = "mencoder -nosound -ovc lavc -lavcopts"
    ENC_PROG += " vcodec=mpeg4:aspect=16/9:vbitrate=8000000"
    ENC_PROG += " -vf scale=%d:%d"%(TL_SIZE[0], TL_SIZE[1])
    ENC_PROG += " -o %s -mf type=jpeg:fps=24 mf://%s"

class CameraGUI(camGUI.CameraGUI):
    '''Extended Camera GUI Class'''
    @staticmethod
    def diff(a, b):
        ''' Return difference between lists '''
        b = set(b)
        return [aa for aa in a if aa not in b]

    def __init__(self, parent):
        '''Class contructor'''
        super(CameraGUI, self).__init__(parent)
        self.parent = parent
        TK.Frame.__init__(self, self.parent,
                          background="white")
        self.the_list = TK.Variable()
        self.image_listbox = TK.Listbox(self.parent,
                                        listvariable=self.the_list,
                                        selectmode=TK.EXTENDED)
        self.image_listbox.grid(row=0, column=4, columnspan=2,
                                sticky=TK.N+TK.S+TK.E+TK.W)
        yscroll = TK.Scrollbar(command=self.image_listbox.yview,
                               orient=TK.VERTICAL)
        yscroll.grid(row=0, column=6, sticky=TK.N+TK.S)
        self.image_listbox.configure(yscrollcommand=yscroll.set)
        self.trim_btn = TK.Button(self.parent, text="Trim",
                                  command=self.trim)
        self.trim_btn.grid(row=1, column=4)
        self.speed = TK.IntVar()
        self.speed.set(20)
        self.speed_scale = TK.Scale(self.parent,
                                    from_=1, to=30,
                                    orient=TK.HORIZONTAL,
                                    variable=self.speed,
                                    label="Speed (fps)")
        self.speed_scale.grid(row=2, column=4)
        self.gen_btn = TK.Button(self.parent, text="Generate",
                                 command=self.generate)
        self.gen_btn.grid(row=2, column=5)
        self.btn_ani_txt = TK.StringVar()
        self.btn_ani_txt.set("Animate")
        self.animate_btn = TK.Button(self.parent,
                                     textvariable=self.btn_ani_txt,
                                     command=self.animate)
        self.animate_btn.grid(row=1, column=5)
        self.animating = False
        self.update_list()

    def shutter(self):
        ''' Extended shutter function '''
        super(CameraGUI, self).shutter()
        self.update_list()

    def update_list(self):
        ''' Update list of images '''
        filelist = []
        for files in os.listdir("."):
            if files.endswith(".jpg"):
                filelist.append(files)
        filelist.sort()
        self.the_list.set(tuple(filelist))
        self.canvas.update()

    def generate(self):
        ''' Generate a new video '''
        self.msg("Generate video...")
        filename = CameraGUI.timestamp()+".avi"
        CameraGUI.run(SET.ENC_PROG%(filename, "*.jpg"))
        self.msg(filename)
        messagebox.showinfo("Encode Complete",
                            "Video: "+filename)

    def trim(self):
        ''' Remove selected items from list '''
        print("Trim List")
        selected = map(int, self.image_listbox.curselection())
        trim = CameraGUI.diff(range(self.image_listbox.size()),
                              selected)
        for item in trim:
            filename = self.the_list.get()[item]
            self.msg("Rename file %s"%filename)
            #We could delete os.remove() but os.rename() allows
            #us to change our minds (files are just renamed).
            os.rename(filename,
                      filename.replace(".jpg", ".jpg.bak"))
            self.image_listbox.selection_clear(
                0,
                last=self.image_listbox.size())
        self.update_list()

    def animate(self):
        ''' Start/Stop animation '''
        print("Animate Toggle")
        if self.animating:
            self.btn_ani_txt.set("Animate")
            self.animating = False
        else:
            self.btn_ani_txt.set("STOP")
            self.animating = True
            self.do_animate()

    def do_animate(self):
        ''' Load selected images and animate '''
        image_list = []
        selected = self.image_listbox.curselection()
        if len(selected) == 0:
            selected = range(self.image_listbox.size())
        print(selected)
        if len(selected) == 0:
            messagebox.showinfo(
                "Error",
                "There are no images to display!")
            self.animate()
        elif len(selected) == 1:
            filename = self.the_list.get()[int(selected[0])]
            self.update_disp(filename, SET.PV_SIZE)
            self.animate()
        else:
            for idx, item in enumerate(selected):
                self.msg("Generate Image: %d/%d"%(idx+1,
                                                  len(selected)))
                filename = self.the_list.get()[int(item)]
                an_image = CameraGUI.get_tk_image(filename,
                                                  SET.PV_SIZE)
                image_list.append(an_image)
            print("Apply Images")
            canvas_list = []
            for idx, an_image in enumerate(image_list):
                self.msg("Apply Image: %d/%d"%(idx+1,
                                               len(image_list)))
                canvas_list.append(
                    self.canvas.create_image(0, 0,
                                             anchor=TK.NW,
                                             image=image_list[idx],
                                             state=TK.HIDDEN))
            self.cycle_images(canvas_list)

    def cycle_images(self, canvas_list):
        ''' Cycle through images at required animation speed '''
        while self.animating:
            print("Cycle Images")
            for idx, an_image in enumerate(canvas_list):
                self.msg("Cycle Image: %d/%d"%(idx+1,
                                               len(canvas_list)))
                self.canvas.itemconfigure(canvas_list[idx],
                                          state=TK.NORMAL)
                if idx >= 1:
                    self.canvas.itemconfigure(canvas_list[idx-1],
                                              state=TK.HIDDEN)
                elif len(canvas_list) > 1:
                    self.canvas.itemconfigure(
                        canvas_list[len(canvas_list)-1],
                        state=TK.HIDDEN)
                self.canvas.update()
                time.sleep(1/self.speed.get())
#End
