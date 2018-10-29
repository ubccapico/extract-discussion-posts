#!/usr/bin/env python

import os
import time
import threading
import traceback
import pprint

from tkinter import *
from tkinter import messagebox


import init
import api_calls as api
import scrape_discussions as sd

def center(top_level):
    top_level.withdraw()
    top_level.update_idletasks()
    x = (top_level.winfo_screenwidth() - top_level.winfo_reqwidth()) / 2
    y = (top_level.winfo_screenheight() - top_level.winfo_reqheight()) / 2
    top_level.geometry("+%d+%d" % (x, y))
    top_level.deiconify()


def thread_message(self, messageParam, function):
    thread = threading.Thread(target=function)
    thread.start()
    cycle = ['/', '-', '\\']
    eli_count = 0
    while thread.is_alive():
        eli_count = (eli_count + 1) % 3
        self.frame.status['text'] = messageParam + ' ' + str(cycle[eli_count])
        self.master.update()
        time.sleep(0.1)
    thread.join()



class EnterCredentials:
    def __init__(self, master):
        # master refers to the window
        self.master = master

        # setting master title
        master.title('Scrape Discussions')

        # centering master
        center(master)
        #master.geometry("275x110")

        # put frame into master and configure grid
        self.frame = Frame(self.master)
        self.frame.pack(fill="both", expand=True)
        self.frame.grid_rowconfigure(4, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        # Course ID Label
        self.frame.course_id = Label(self.frame, text="Course ID: ")
        self.frame.course_id.grid(row=0, sticky=E)

        # Course ID Entry
        self.frame.course_id_entry = Entry(self.frame)
        self.frame.course_id_entry.grid(row=0, column=1, sticky='news')
        self.frame.course_id_entry.bind("<Key>", self.update_size)

        # Base URL Label
        self.frame.base_url = Label(self.frame, text="Base URL: ")
        self.frame.base_url.grid(row=1, sticky=E)

        # Base URL Entry
        self.frame.base_url_entry = Entry(self.frame)
        self.frame.base_url_entry.grid(row=1, column=1, sticky='news')
        self.frame.base_url_entry.bind("<Key>", self.update_size)

        self.frame.access_token = Label(self.frame, text="Access Token: ")
        self.frame.access_token.grid(row=2, sticky=E)

        self.frame.access_token_entry = Entry(self.frame)
        self.frame.access_token_entry.grid(row=2, column=1, sticky='news')
        self.frame.access_token_entry.bind("<Key>", self.update_size)

        self.master.bind('<Return>', self.new_window)
        self.master.bind('<Escape>', self.close_windows)

        # Ok Button
        self.frame.login_button_ok = Button(
            self.frame, text="Ok", command=self.new_window)
        self.frame.login_button_ok.grid(row=4, column=0, sticky='news')

        # Cancel Button
        self.frame.login_button_cancel = Button(
            self.frame, text="Cancel", command=self.close_windows)
        self.frame.login_button_cancel.grid(row=4, column=1, sticky='news')

        # Status Label
        self.frame.status = Label(
            self.frame,
            text='Choose an option...',
            bd=1,
            relief=SUNKEN,
            anchor=W)
        self.frame.status.grid(row=5, columnspan=2, sticky='news')

    def update_size(self, event):
        widget_width = 0
        widget_height = float(event.widget.index(END))
        for line in event.widget.get().split("\n"):
           if len(line) > widget_width:
              widget_width = len(line)+1
        event.widget.config(width=widget_width)

    def close_windows(self, event=None):
        self.master.destroy()

    def new_window(self, event=None):
        try:
            # record course_idas
            init.course_id = self.frame.course_id_entry.get()
            init.base_url = self.frame.base_url_entry.get()
            init.access_token = self.frame.access_token_entry.get()
            init.course_name = api.get_course()['name']

            self.scrape_discussions()



            # if everything comes back fine, destroy this EnterCredentials
            # window and create CourseCleanupOptions window
            # self.master.destroy()
            # self.master = Tk()
            # self.app = CourseCleanupOptions(self.master)
            # self.master.mainloop()
        except Exception as e:
            #traceback.print_exc()
            print('The Course ID, Access Token, or base URL is incorrect.\nIf any problem still persists, restart the program and try again.')
            self.frame.status['text'] = 'The Course ID, Access Token, or base URL is incorrect.'
            messagebox.showinfo(
                "Error",
                "The Course ID, Access Token, or base URL is incorrect.",
                icon="warning")

    def scrape_discussions(self):
        thread_message(
             self,
             "Scraping Discussions from " + init.course_name + "...",
             sd.scrape_discussions)
        self.frame.status['text'] = "Done Scraping Discussions from "+ init.course_name +"!"
        self.frame.update_idletasks()



root = Tk()
app = EnterCredentials(root)
root.mainloop()
