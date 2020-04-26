#!/usr/bin/python3
'''camera_gui_3animate.py'''
import tkinter as TK
import cam.AnimateGUI as GUI

#Define Tkinter App
root = TK.Tk()
root.title("Camera GUI")
cam = GUI.CameraGUI(root)
TK.mainloop()
#End
