#!/usr/bin/python3
''' tkencryptdecrypt '''
import tkinter as TK
import encryptdecrypt as ENC

def encrypt_button():
    encryptvalue.set(ENC.encrypt_text(encryptvalue.get(),
                                      keyvalue.get()))

def decrypt_button():
    encryptvalue.set(ENC.encrypt_text(encryptvalue.get(),
                                      -keyvalue.get()))

#Define Tkinter application
root = TK.Tk()
root.title("Encrypt/Decrypt GUI")
#Set control & test value
encryptvalue = TK.StringVar()
encryptvalue.set("My Message")
keyvalue = TK.IntVar()
keyvalue.set(20)
PROMPT = "Enter message to encrypt:"
KEY = "Key:"

label1 = TK.Label(root, text=PROMPT, width=len(PROMPT), bg='green')
text_enter = TK.Entry(root, textvariable=encryptvalue,
                      width=len(PROMPT))
encrypt_btn = TK.Button(root, text="Encrypt", command=encrypt_button)
decrypt_btn = TK.Button(root, text="Decrypt", command=decrypt_button)
label2 = TK.Label(root, text=KEY, width=len(KEY))
key_enter = TK.Entry(root, textvariable=keyvalue, width=8)
#Set layout
label1.grid(row=0, columnspan=2, sticky=TK.E+TK.W)
text_enter.grid(row=1, columnspan=2, sticky=TK.E+TK.W)
encrypt_btn.grid(row=2, column=0, sticky=TK.E)
decrypt_btn.grid(row=2, column=1, sticky=TK.W)
label2.grid(row=3, column=0, sticky=TK.E)
key_enter.grid(row=3, column=1, sticky=TK.W)

TK.mainloop()
#End
