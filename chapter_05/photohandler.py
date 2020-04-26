#!/usr/bin/python3
'''photohandler.py'''
import os
import datetime
from PIL import Image
from PIL import ExifTags

#set module values
PREVIEWSIZE = 240, 240
DEFAULT_IMAGE_PREVIEW = "./preview.ppm"
FILEDATE_TO_USE = "Exif DateTime"

class Photo:
    def __init__(self, filename):
        '''Class constructor'''
        self.filename = filename
        self.filevalid = False
        self.exifvalid = False
        img = self.init_image()
        if self.filevalid:
            self.init_exif(img)
            self.init_dates()

    def init_image(self):
        '''opens the image and confirms if valid, returns Image'''
        try:
            img = Image.open(self.filename)
            self.filevalid = True
        except IOError:
            print(f"Target image not found/valid {self.filename}")
            img = None
            self.filevalid = False
        return img

    def init_exif(self, image):
        '''gets any Exif data from the photo'''
        try:
            self.exif_info = {
                ExifTags.TAGS[x]:y
                for x, y in image._getexif().items()
                if x in ExifTags.TAGS
            }
            self.exifvalid = True
        except AttributeError:
            print("Image has no Exif Tags")
            self.exifvalid = False


    def init_dates(self):
        '''determines the date the photo was taken'''
        #Gather all the times available into YYYY-MM-DD format
        self.filedates = {}
        if self.exifvalid:
            #Get the date info from Exif info
            exif_ids = ["DateTime", "DateTimeOriginal",
                        "DateTimeDigitized"]
            for the_id in exif_ids:
                try:
                    dateraw = self.exif_info[the_id]
                    self.filedates["Exif "+the_id] = \
                                dateraw[:10].replace(":", "-")
                except KeyError:
                    print(f"ID: {the_id} not found")
        modtimeraw = os.path.getmtime(self.filename)
        self.filedates["File ModTime"] = "%s" %\
            datetime.datetime.fromtimestamp(modtimeraw).date()
        createtimeraw = os.path.getctime(self.filename)
        self.filedates["File CreateTime"] = "%s" %\
            datetime.datetime.fromtimestamp(createtimeraw).date()

    def get_date(self, use_date=FILEDATE_TO_USE):
        '''returns the date the image was taken'''
        try:
            date = self.filedates[use_date]
        except KeyError:
            print("Exif Date not found")
            date = self.filedates["File ModTime"]
        return date

    def preview_photo(self, pvname=DEFAULT_IMAGE_PREVIEW):
        '''creates a thumbnail image suitable for tk to display'''
        imageview = self.init_image()
        imageview = imageview.convert('RGB')
        imageview.thumbnail(PREVIEWSIZE, Image.ANTIALIAS)
        imageview.save(pvname, format='ppm')
        return pvname
#End
