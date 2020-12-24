#!/usr/bin/python3
''' TimelapseGUI.py '''
import time
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
    def cam_timelapse(filename, size=SET.TL_SIZE,
                      timedelay=10, num_images=10):
        ''' Run Timelapse capture '''
        with camGUI.picam.PiCamera() as camera:
            camera.resolution = size
            for count, name in \
                    enumerate(camera.capture_continuous(filename)):
                print("Timelapse: %s"%name)
                if count == num_images:
                    break
                time.sleep(timedelay)

    def __init__(self, parent):
        '''Class contructor'''
        super(CameraGUI, self).__init__(parent)
        self.parent = parent
        TK.Frame.__init__(self, self.parent, background="white")
        self.tstamp = ""
        self.num_image_tl = TK.StringVar()
        self.peroid_tl = TK.StringVar()
        self.total_time_tl = TK.StringVar()
        self.gen_video_tl = TK.IntVar()
        label_num_img_tk = TK.Label(self.parent, text="TL:#Images")
        label_peroid_tk = TK.Label(self.parent, text="TL:Delay")
        label_total_time_tk = TK.Label(self.parent,
                                       text="TL:TotalTime")
        self.num_img_spn = TK.Spinbox(
            self.parent,
            textvariable=self.num_image_tl,
            from_=1, to=99999,
            width=5, state="readonly",
            command=self.calc_tl_total_time)
        self.peroid_spn = TK.Spinbox(
            self.parent,
            textvariable=self.peroid_tl,
            from_=1, to=99999, width=5,
            command=self.calc_tl_total_time)
        self.total_time = TK.Label(
            self.parent,
            textvariable=self.total_time_tl)
        self.tl_btn = TK.Button(self.parent, text="TL GO!",
                                command=self.timelapse)
        gen_chk = TK.Checkbutton(self.parent, text="GenVideo",
                                 command=self.gen_video_chk,
                                 variable=self.gen_video_tl)
        label_num_img_tk.grid(row=3, column=0)
        self.num_img_spn.grid(row=4, column=0)
        label_peroid_tk.grid(row=3, column=1)
        self.peroid_spn.grid(row=4, column=1)
        label_total_time_tk.grid(row=3, column=2)
        self.total_time.grid(row=4, column=2)
        self.tl_btn.grid(row=3, column=3)
        gen_chk.grid(row=4, column=3)
        self.num_image_tl.set(10)
        self.peroid_tl.set(5)
        self.gen_video_tl.set(1)
        self.calc_tl_total_time()

    def btn_state(self, state):
        ''' Extended btn_state function '''
        self.tl_btn["state"] = state
        super(CameraGUI, self).btn_state(state)

    def calc_tl_total_time(self):
        ''' Calculate total timelapse time '''
        num_img = float(self.num_image_tl.get())-1
        peroid = float(self.peroid_tl.get())
        if num_img < 0:
            num_img = 1
        self.total_time_tl.set(num_img*peroid)

    def timelapse(self):
        ''' Perform timelapse '''
        self.msg("Running Timelapse")
        self.btn_state("disabled")
        self.update()
        self.tstamp = "TL" + CameraGUI.timestamp()
        CameraGUI.cam_timelapse(self.tstamp+'{counter:03d}.jpg',
                                SET.TL_SIZE,
                                float(self.peroid_tl.get()),
                                int(self.num_image_tl.get()))
        if self.gen_video_tl.get() == 1:
            self.gen_tl_video()
        self.btn_state("active")
        messagebox.showinfo("Timelapse Complete",
                            "Processing complete")
        self.update()

    def gen_video_chk(self):
        ''' Handle video checkbox '''
        if self.gen_video_tl.get() == 1:
            messagebox.showinfo("Generate Video Enabled",
                                "Video will be generated")
        else:
            messagebox.showinfo("Generate Video Disabled",
                                "Only images will be generated")

    def gen_tl_video(self):
        ''' Generate video '''
        self.msg("Generate video...")
        CameraGUI.run("pwd")
        CameraGUI.run(SET.ENC_PROG%(self.tstamp+".avi",
                                    self.tstamp+"*.jpg"))
        self.msg(self.tstamp+".avi")
#End
