#!/usr/bin/python3
'''photoorganizer.py'''
import os
import photohandler as PH
DEBUG=True

class FileList:
    def __init__(self,folder):
        '''Class constructor'''
        self.folder=folder
        self.listFiles()

    def listFiles(self):
        """Generates list of filenames"""
        self.fileList=list()
        self.fileDate=list()
        if os.path.isdir(self.folder):
            for filename in os.listdir(self.folder):
                if filename.lower().endswith(".jpg"):
                    aPhoto = PH.Photo(os.path.join(self.folder,filename))
                    if aPhoto.filevalid:
                        if (DEBUG):print("NameDate: %s %s"%
                                         (filename,aPhoto.getDate()))
                        self.fileList.append(filename)
                        self.fileDate.append(aPhoto.getDate())
                        sorted(self.fileDate,
                                    key=lambda date: date)
                        #self.photo_namedates.append((filename,
                        #                             aPhoto.getDate()))
                        #self.photo_namedates = sorted(self.photo_namedates,
                        #                        key=lambda date: date[DATE])


def getFolder():
    global ourFileList
    file_name.value = app.select_folder(title="Select photo folder",
                                        folder=r"C:\Users\onlin\Pictures\Camera Roll")
    ourFileList=FileList(file_name.value)
    print(ourFileList.fileList)
    #photolist_box=ourFileList.fileList
    for item in ourFileList.fileList:
      photolist_box.append(item)
    list_set = set(ourFileList.fileDate)
    print(list_set)
    print(list(list_set))
    datelist_box.clear()
    for item in list_set:
      datelist_box.append(item)


def showPicture(value):
    print(value)
    picture.image=os.path.join(file_name.value,value[0])
    print(ourFileList.fileDate[ourFileList.fileList.index(value[0])])
    file_date.value=ourFileList.fileDate[ourFileList.fileList.index(value[0])]
    #for index, item in enumerate(ourFileList.fileList):
    #    if item[0] == value:
    #        file_date.value = ourFileList.fileDate[index]

def updatePhotoList(value):
    print(value)
    alist = [ourFileList.fileList[i] for i, val in enumerate(ourFileList.fileDate) if val in value]
    print(alist)
    photolist_box.clear()
    for item in alist:
      photolist_box.append(item)

def addFolderText(clear=False):
    for i,item in enumerate(datelist_box.items):
        if file_date.value in item:
            print(f"{i} {item}")
            print(datelist_box.remove(item))
            #print(datelist_box.remove(0))
            if clear:
                filedate=ourFileList.fileDate[i]
                datelist_box.insert(i,filedate)
            else:
                datelist_box.insert(i,item+newName.value)
            break

def generateFolders():
    print(f"Create new folder in {file_name.value}")
    for value in datelist_box.items:
        alist = [ourFileList.fileList[i] for i, val in enumerate(ourFileList.fileDate) if val in value]
        print(f"New folder: {value}")
        for item in alist:
            print(f"Photo: {item}")
            print(f"Move {file_name.value}/{item} to {file_name.value}/{value}/{item}")

def main():
    """called only when run directly, allowing module testing"""
    #pathname=r"C:\Users\T\Pictures\Camera Roll"

if __name__=="__main__":
    from guizero import App, PushButton, Text, ListBox, Picture, TextBox
    app=App(layout="grid")
    PushButton(app, command=getFolder, text="Get folder", grid=[0,0])
    file_name = Text(app, grid=[1,0,3,1])
    datelist_box = ListBox(app, grid=[0,1],items=[],command=updatePhotoList)
    photolist_box = ListBox(app, grid=[1,1],items=[],command=showPicture, multiselect=True)
    picture = Picture(app, grid=[3,1,2,3], width=200, height=200)
    file_date = Text(app, grid=[0,2,1,3])
    newName = TextBox(app, grid=[2,4])
    PushButton(app, command=addFolderText, text="Rename", grid=[4,4])
    PushButton(app, command=addFolderText, args=[True], text="Reset", grid=[4,5])
    PushButton(app, command=generateFolders, text="Generate", grid=[0,5])
 
    app.display()
#End
