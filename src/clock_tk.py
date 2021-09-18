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

# Waiting time in minutes
STANDARD = 15


class ClockTk(Frame):

    def __init__(self, master=None, start="00:00:00", interval=STANDARD):
        super().__init__(master)
        self.master = master
        self.master.title("TIMER - Press ESC to exit.")
        self.master.bind("<Escape>", lambda x : quit())
        self.path = "../images/clock.png"
        self.pack()
        
        hour, minute, second = start.split(':')
        self.interval = interval
        self.start = (int(hour) * 60) + int(minute)
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
        # Adjust angles
        a = (angle - 90) * pi / 180.0
        x = (self.size / 2) + cos(a) * radius
        y = (self.size / 2) + sin(a) * radius
        return (x, y)

    def render(self):
        # Update current time
        now = datetime.now()
        minute = now.minute
        minutes = (now.hour * 60) + minute
        hour = now.hour if now.hour <= 12 else now.hour - 12

        # Background - alert
        color = "#C4C4C4" if minutes < self.stop else "red"
        self.canvas.create_rectangle(0,0, self.size, self.size, fill=color)

        # Watch image
        self.canvas.create_image(0, 0, image=self.image, anchor='nw')

        # Pointers
        x, y = self.pointer(minute * 6, self.size / 3)
        self.canvas.create_line(self.size / 2, self.size / 2, x, y, width=5, fill='green')
        x, y = self.pointer((hour * 30) + (minute * 0.4), self.size / 4)
        self.canvas.create_line(self.size / 2, self.size / 2, x, y, width=5, fill='green')

        # Minute marker
        i = 0.0
        while minutes + i < self.stop:
            i += 0.1
            a = (minute + i) * 6
            x, y = self.pointer(a, self.size / 2 - 5)
            x1, y1 = self.pointer(a, self.size / 2 - 20)
            color = '#7AFF71'
            if minutes + i > self.start:
                color = "#0A6D04" 
                if minutes + i > self.alert:
                    color = "red"
            self.canvas.create_line(x, y, x1, y1, width=5, fill=color)
            
    def run(self):
        self.running = True  
        _thread.start_new_thread(self.update, tuple([]))
        print("Timer activated ...\n")
        print("Use Esc to exit the application ...\n")

    def close(self):
        print("There is something wrong.")
        exit()

    def update(self):
      while self.running:
        time.sleep(10)
        self.render()


def validate(args):
    now = datetime.now() 
    start = "EMPTY"
    interval = 0

    print("Check ...", args)
    for arg in args:
        if arg[0:4] == "now=":
            if start == "EMPTY":        
                try:
                    v = arg[4:].split(':')
                    if len(v) == 1:
                        v += ["00"]
                    h = "error" if int(v[0]) < 0 or int(v[0]) > 23 else v[0]
                    m = "error" if int(v[1]) < 0 or int(v[1]) > 59 else v[1]
                    print("Time status [ {0}:{1}:00 ]".format(h, m))
                    start = "{0}:{1}:00".format(int(h), int(m))
                except:
                    print("Time error ...")
        if arg[0:8] == "minutes=":
            if interval == 0:
                try:
                    v = arg[8:]
                    print("Interval status [ {0} ]".format(v))
                    v = "error" if int(v) <= 0 or int(v) > 60 else v
                    interval = int(v)
                except:
                    print("Wrong interval value ...")

    if start == "EMPTY":
        start = "{0}:{1}:{2}".format(now.hour, now.minute, now.second)
        print("Current time [ {0} ]".format(start))
    if interval == 0:
        interval = STANDARD
        print("Interval default [ {0} ]".format(interval))

    return [start, interval]


def main(args):
    # Check
    value_start, value_interval = validate(args)

    # Run
    root = Tk()
    app = ClockTk(master=root, start=value_start, interval=value_interval)
    app.run()
    app.mainloop()


def test():
    # Inputs
    tests = [
        [],
        ["test"],
        ["test", "minutes=-1", "test"],
        ["minutes=-1"],
        ["minutes=0"],
        ["minutes=61"],
        ["minutes=a5"],
        ["minutes= 5"],
        ["minutes=5"],
        ["now=hour:minute"],
        ["now=24:10", "minutes=5"],
        ["now=10:60", "minutes=5"],
        ["now=10:10", "minutes=5"],
        ["now=16", "minutes=5"],
        ["now=1", "minutes=5"]
    ]

    for i in tests:
        validate(i)
        print("="*80)


if __name__ == '__main__':
    # Test
    # test()

    # Run 
    main(sys.argv)
