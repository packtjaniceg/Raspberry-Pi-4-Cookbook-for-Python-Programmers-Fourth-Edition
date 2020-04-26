#!/usr/bin/python3
''' QrcodeGUI '''
import tkinter as TK
from tkinter import messagebox
import subprocess
import cam.CameraGUI as camGUI

class SET(camGUI.SET):
    '''Extended Settings class'''
    QR_SIZE = (640, 480)
    DETECT_QR = "zbarimg"
    READ_QR = "flite"
    PLAY_QR = "omxplayer"

class CameraGUI(camGUI.CameraGUI):
    '''Extended Camera GUI Class'''
    @staticmethod
    def run_p(cmd):
        ''' Run command using popen '''
        print("RunP:"+" ".join(cmd))
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE)
        result = ""
        for line in proc.stdout:
            result = str(line, "utf-8")
        return result

    def __init__(self, parent):
        '''Class contructor'''
        super(CameraGUI, self).__init__(parent)
        self.parent = parent
        TK.Frame.__init__(self, self.parent, background="white")
        self.qr_read = TK.IntVar()
        self.qr_play = TK.IntVar()
        self.result_qr = TK.StringVar()
        self.btn_qr_txt = TK.StringVar()
        self.btn_qr_txt.set("QR GO!")
        self.qr_btn = TK.Button(self.parent,
                                textvariable=self.btn_qr_txt,
                                command=self.qr_get)
        read_chk = TK.Checkbutton(self.parent, text="Read",
                                  variable=self.qr_read)
        play_chk = TK.Checkbutton(self.parent, text="Play",
                                  variable=self.qr_play)
        label_qr = TK.Label(self.parent,
                            textvariable=self.result_qr)
        read_chk.grid(row=3, column=0)
        play_chk.grid(row=3, column=1)
        self.qr_btn.grid(row=3, column=3)
        label_qr.grid(row=4, columnspan=4)
        self.scan = False

    def qr_get(self):
        ''' Start scan for a QR Code '''
        if self.scan:
            self.btn_qr_txt.set("QR GO!")
            self.btn_state("active")
            self.scan = False
        else:
            self.msg("Get QR Code")
            self.btn_qr_txt.set("STOP")
            self.btn_state("disabled")
            self.scan = True
            self.qr_scanner()

    def qr_scanner(self):
        ''' Perform scan for QRCode '''
        found = False
        while self.scan:
            self.result_qr.set("Taking image...")
            self.update()
            CameraGUI.cam_capture(SET.PREVIEW_FILE, SET.QR_SIZE)
            self.result_qr.set("Scanning for QRCode...")
            self.update()
            #check for QR code in image
            qrcode = CameraGUI.run_p([SET.DETECT_QR,
                                      SET.PREVIEW_FILE])
            if len(qrcode) > 0:
                qrcode = qrcode.strip("QR-Code:").strip('\n')
                self.msg("Got barcode: %s"%qrcode)
                self.result_qr.set(qrcode)
                self.scan = False
                found = True
            else:
                self.result_qr.set("No QRCode Found")
        if found:
            self.qr_action(qrcode)
            self.btn_state("active")
            self.btn_qr_txt.set("QR GO!")
        self.update()

    def qr_action(self, qrcode):
        ''' Read or Play QRCode '''
        if self.qr_read.get() == 1:
            self.msg("Read:"+qrcode)
            #CameraGUI.run_p("flite -t '"+qrcode+"'")
            CameraGUI.run_p([SET.READ_QR, "-t", "'"+qrcode+"'"])
        if self.qr_play.get() == 1:
            self.msg("Play:"+qrcode)
            #CameraGUI.run_p("omxplayer '"+qrcode+"'")
            CameraGUI.run_p([SET.PLAY_QR, "'"+qrcode+"'"])
        if self.qr_read.get() == 0 and self.qr_play.get() == 0:
            messagebox.showinfo("QR Code", self.result_qr.get())
#End
