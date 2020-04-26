#!/usr/bin/python3
'''painting.py'''
import tkinter as TK

class Painter():
    '''Painter GUI Class'''
    def __init__(self):
        '''Define canvas and start mainloop'''
        #Set defaults
        self.btn1_pressed = False
        self.newline = True
        self.x_orig, self.y_orig = 0, 0
        root = TK.Tk()
        the_canvas = TK.Canvas(root)
        the_canvas.pack()
        the_canvas.bind("<Motion>", self.mouse_move)
        the_canvas.bind("<ButtonPress-1>", self.mouse1_press)
        the_canvas.bind("<ButtonRelease-1>", self.mouse1_release)
        root.mainloop()

    def mouse1_press(self, event):
        '''Handle mouse button press'''
        self.btn1_pressed = True

    def mouse1_release(self, event):
        '''Handle mouse button release'''
        self.btn1_pressed = False
        self.newline = True

    def mouse_move(self, event):
        '''Handle mouse movement'''
        if self.btn1_pressed:
            if not self.newline:
                event.widget.create_line(self.x_orig, self.y_orig,
                                         event.x, event.y,
                                         smooth=TK.TRUE)
            self.newline = False
            self.x_orig = event.x
            self.y_orig = event.y

if __name__ == "__main__":
    Painter()
#End
