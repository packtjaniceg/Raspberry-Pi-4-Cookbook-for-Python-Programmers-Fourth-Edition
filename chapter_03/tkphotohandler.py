#!/usr/bin/python3
'''tkphotohandler.py'''
import tkinter as TK
from tkinter import filedialog
import photohandler as PH

#Define expected inputs
ARG_IMAGEFILE = 1
ARG_LENGTH = 2

class PhotoGui():
    def __init__(self, filename=None):
        '''Create a test GUI'''
        self.filename = filename
        #Define the app window
        self.app = TK.Tk()
        self.app.title("Photo View Demo")

        #Define TK objects
        menubar = TK.Menu(self.app)
        filemenu = TK.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Exit", command=self.app.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        self.app.config(menu=menubar)
        # create an empty canvas object the same size as the image
        self.canvas = TK.Canvas(self.app, width=PH.PREVIEWSIZE[0],
                                height=PH.PREVIEWSIZE[1])
        self.canvas.grid(row=0, rowspan=2)
        # Add list box to display the photo data
        #(including xyscroll bars)
        self.photo_info = TK.Variable()
        lbphoto_info = TK.Listbox(self.app, listvariable=self.photo_info,
                                  height=18, width=45,
                                  font=("monospace", 10))
        yscroll = TK.Scrollbar(command=lbphoto_info.yview,
                               orient=TK.VERTICAL)
        xscroll = TK.Scrollbar(command=lbphoto_info.xview,
                               orient=TK.HORIZONTAL)
        lbphoto_info.configure(xscrollcommand=xscroll.set,
                               yscrollcommand=yscroll.set)
        lbphoto_info.grid(row=0, column=1, sticky=TK.N+TK.S)
        yscroll.grid(row=0, column=2, sticky=TK.N+TK.S)
        xscroll.grid(row=1, column=1, sticky=TK.N+TK.E+TK.W)

        if self.filename:
            self.disp_preview()
        self.app.mainloop()

    def open_file(self):
        '''Request select a photo'''
        self.filename = filedialog.askopenfilename(
            initialdir="/", title="Select photo",
            filetypes=(("jpeg files", ["*.jpg", "*.JPG"]),
                       ("all files", "*.*")))
        if self.filename:
            self.disp_preview()

    def disp_preview(self):
        '''Display preview and details'''
        #Create an instance of the Photo class
        self.a_photo = PH.Photo(self.filename)
        # Generate the preview image
        preview_filename = self.a_photo.preview_photo()
        self.photo_img = TK.PhotoImage(file=preview_filename)
        # anchor image to NW corner
        self.canvas.create_image(0, 0, anchor=TK.NW, image=self.photo_img)
        # Populate info_list with dates and exif data
        info_list = []
        for key, value in self.a_photo.filedates.items():
            info_list.append(key.ljust(25) + value)
        if self.a_photo.exifvalid:
            for key, value in self.a_photo.exif_info.items():
                info_list.append(key.ljust(25) + str(value))
        # Set listvariable with the info_list
        self.photo_info.set(tuple(info_list))

def main():
    '''called only when run directly, allowing module testing'''
    import sys
    #Check the arguments
    if len(sys.argv) == ARG_LENGTH:
        print(f"Command: {sys.argv}")
        #Create an instance of the Photo class
        view_photo = PH.Photo(sys.argv[ARG_IMAGEFILE])
        #Test the module by running a GUI
        if view_photo.filevalid:
            PhotoGui(sys.argv[ARG_IMAGEFILE])
    else:
        print("Usage: tkphotohandler.py imagefile")
        PhotoGui()

if __name__ == '__main__':
    main()
#End
