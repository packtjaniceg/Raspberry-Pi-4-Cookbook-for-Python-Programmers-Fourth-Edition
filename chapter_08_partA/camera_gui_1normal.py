#!/usr/bin/python3
'''camera_gui_1normal.py'''
import tkinter as TK
import cam.CameraGUI as GUI

root = TK.Tk()
root.title("Camera GUI")
cam = GUI.CameraGUI(root)
TK.mainloop()
#End
