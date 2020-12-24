#!/usr/bin/python3
'''camera_gui_2timelapse.py'''
import tkinter as TK
import cam.TimelapseGUI as GUI

root = TK.Tk()
root.title("Camera GUI")
cam = GUI.CameraGUI(root)
TK.mainloop()
#End
