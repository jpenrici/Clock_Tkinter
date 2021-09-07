# -*- Mode: Python3; coding: utf-8; indent-tabs-mpythoode: nil; tab-width: 4 -*-
#
# Simple clock with timer.
# The stopwatch can be seen on the edge of the pointer in green and red colors.
# When the deadline ends, the entire border turns red.
#
# Reference:
#   https://docs.python.org/3/library/tkinter.html

from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from math import cos, sin, pi
import time, _thread
import sys

# waiting time in minutes
STANDARD = 15


class ClockTk(Frame):

    def __init__(self, master=None, interval=STANDARD):
        super().__init__(master)
        self.master = master
        self.master.title("TIMER- Press ESC to exit.")
        self.master.bind("<Escape>", lambda x : quit())
        self.path = "../images/clock.png"
        self.pack()
        
        now = datetime.now()
        self.interval = interval
        self.start = (now.hour * 60) + now.minute
        self.stop = self.start + self.interval
        self.alert = self.start + self.interval * 0.8

        self.running = False
        self.make()
        self.render()

    def make(self):
        try:
            img = Image.open(self.path)
            img_width, img_height = img.size

            if img_width != img_height:
                self.close()

            self.size = img_width
            self.canvas = Canvas(self.master, width=self.size, height=self.size)
            self.canvas.pack()
            self.image = ImageTk.PhotoImage(img)
        except:
            self.close()

    def pointer(self, angle, radius):
        a = (angle - 90) * pi / 180.0
        x = (self.size / 2) + cos(a) * radius
        y = (self.size / 2) + sin(a) * radius
        return (x, y)

    def render(self):
        now = datetime.now()
        minute = now.minute
        minutes = (now.hour * 60) + minute
        hour = now.hour if now.hour <= 12 else now.hour - 12

        # background - alert
        color = "white" if minutes < self.stop else "red"
        self.canvas.create_rectangle(0,0, self.size, self.size, fill=color)

        # watch image
        self.canvas.create_image(0, 0, image=self.image, anchor='nw')

        # pointers
        x, y = self.pointer(minute * 6, self.size / 3)
        self.canvas.create_line(self.size / 2, self.size / 2, x, y, width=5, fill='green')
        x, y = self.pointer(hour * 30, self.size / 4)
        self.canvas.create_line(self.size / 2, self.size / 2, x, y, width=5, fill='green')

        # minute marker
        i = 0.0
        while minutes + i < self.stop:
            i += 0.1
            a = (minute + i) * 6
            x, y = self.pointer(a, self.size / 2 - 5)
            x1, y1 = self.pointer(a, self.size / 2 - 20)
            color = "green" if minutes + i < self.alert else "red"
            self.canvas.create_line(x, y, x1, y1, width=5, fill=color)
            
    def run(self):
        self.running = True  
        _thread.start_new_thread(self.update, tuple([]))
        print("timer activated ...")

    def close(self):
        print("There is something wrong.")
        exit()

    def update(self):
      while self.running:
        time.sleep(10)
        self.render()


def main(args):
    msg = "interval = {0} [ {1} ]"
    value = STANDARD
    status = "Using default value."

    for arg in args:
        if arg[0:8] == "minutes=":
            try:
                value = int(arg[8:])
                status = "OK!"
                if value <= 0 or value > 60:
                    status = str(value) + ", value out of range! Using default."
                    value = STANDARD
                break
            except:
                status = arg[8:] + ", invalid value! Using default value."
    print(msg.format(value, status))
    print("Use ESC to exit.")

    # run
    root = Tk()
    app = ClockTk(master=root, interval=value)
    app.run()
    app.mainloop()


def test():
    ## uncomment one test at a time

    ## use default
    # main([])
    # main(["test"])
    # main(["test", "minutes=-1", "test"])
    # main(["minutes=-1", "test"])
    # main(["minutes=0"])
    # main(["minutes=61"])
    # main(["minutes=a5"])
    
    ## use value
    # main(["minutes= 5"])
    main(["minutes=5"])


if __name__ == '__main__':
    # Test
    # test()

    # run 
    main(sys.argv)
