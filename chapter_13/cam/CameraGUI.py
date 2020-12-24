#!/usr/bin/python3
'''CameraGUI.py'''
import subprocess
import time
import datetime
import sys
import tkinter as TK
from PIL import Image
import picamera as picam

class SET():
    '''Settings class'''
    PV_SIZE = (320, 240)
    NORM_SIZE = (2592, 1944)
    NO_RESIZE = (0, 0)
    PREVIEW_FILE = "PREVIEW.jpg"
    TEMP_FILE = "PREVIEW.ppm"

class CameraGUI(TK.Frame):
    '''Camera GUI Class'''
    @staticmethod
    def run(cmd):
        '''Run command'''
        print("Run:" + cmd)
        subprocess.call(cmd.split())

    @staticmethod
    def cam_capture(filename, size=SET.NORM_SIZE):
        '''Capture a new image'''
        with picam.PiCamera() as camera:
            camera.resolution = size
            print("Image: %s"%filename)
            camera.capture(filename)

    @staticmethod
    def get_tk_image(filename, previewsize=SET.NO_RESIZE):
        '''Load image for TK'''
        encoding = str.split(filename, ".")[1].lower()
        print("Image Encoding: %s"%encoding)
        try:
            if encoding == "gif" and previewsize == SET.NO_RESIZE:
                the_tk_image = TK.PhotoImage(file=filename)
            else:
                imageview = Image.open(filename)
                if previewsize != SET.NO_RESIZE:
                    imageview.thumbnail(previewsize, Image.ANTIALIAS)
                imageview.save(SET.TEMP_FILE, format="ppm")
                the_tk_image = TK.PhotoImage(file=SET.TEMP_FILE)
        except IOError:
            print("Unable to get: %s"%filename)
        return the_tk_image

    @staticmethod
    def timestamp():
        '''Generate timestamp'''
        ts = time.time()
        tstring = datetime.datetime.fromtimestamp(ts)
        return tstring.strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def exit():
        '''Exit application'''
        sys.exit()

    def __init__(self, parent):
        '''Class contructor'''
        self.parent = parent
        TK.Frame.__init__(self, self.parent)
        self.parent.title("Camera GUI")
        self.preview_update = TK.IntVar()
        self.filename = TK.StringVar()
        self.canvas = TK.Canvas(self.parent,
                                width=SET.PV_SIZE[0],
                                height=SET.PV_SIZE[1])
        self.canvas.grid(row=0, columnspan=4)
        self.shutter_btn = TK.Button(self.parent, text="Shutter",
                                     command=self.shutter)
        self.shutter_btn.grid(row=1, column=0)
        exit_btn = TK.Button(self.parent, text="Exit",
                             command=CameraGUI.exit)
        exit_btn.grid(row=1, column=3)
        preview_chk = TK.Checkbutton(self.parent, text="Preview",
                                     variable=self.preview_update)
        preview_chk.grid(row=1, column=1)
        label_filename = TK.Label(self.parent,
                                  textvariable=self.filename)
        label_filename.grid(row=2, column=0, columnspan=3)
        self.preview()

    def msg(self, text):
        '''Update message'''
        self.filename.set(text)
        self.update()

    def btn_state(self, state):
        '''Set button state'''
        self.shutter_btn["state"] = state

    def shutter(self):
        '''Take a new picture'''
        self.btn_state("disabled")
        self.msg("Taking photo...")
        self.update()
        if self.preview_update.get() == 1:
            self.preview()
        else:
            self.normal()
        self.btn_state("active")

    def normal(self):
        '''Take picture and save file'''
        name = CameraGUI.timestamp()+".jpg"
        CameraGUI.cam_capture(name, SET.NORM_SIZE)
        self.update_disp(name, previewsize=SET.PV_SIZE)
        self.msg(name)

    def preview(self):
        '''Take picture and display only'''
        CameraGUI.cam_capture(SET.PREVIEW_FILE, SET.PV_SIZE)
        self.update_disp(SET.PREVIEW_FILE)
        self.msg(SET.PREVIEW_FILE)

    def update_disp(self, filename, previewsize=SET.NO_RESIZE):
        '''Update preview image'''
        self.msg("Loading Preview...")
        self.my_image = CameraGUI.get_tk_image(filename,
                                               previewsize)
        self.the_image = self.canvas.create_image(0, 0,
                                                  anchor=TK.NW,
                                                  image=self.my_image)
        self.update()
#End
