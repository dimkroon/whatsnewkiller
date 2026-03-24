# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  SPDX-License-Identifier: GPL-3.0-or-later
# ------------------------------------------------------------------------------

import os
import sys
import queue
import threading
import logging
from io import StringIO

from tkinter import *
from tkinter.ttk import *

import killer


APP_TITLE = "WhatsNewKiller"


_gui_msg_queue = queue.Queue()


def autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed."""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)


class Runner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        log_stream = StringIO()
        log_handler = logging.StreamHandler(log_stream)
        log_handler.setLevel(logging.INFO)
        log_handler.setFormatter(logging.Formatter('%(message)s'))
        logging.getLogger().addHandler(log_handler)
        killer.run()
        logging.getLogger().removeHandler(log_handler)
        _gui_msg_queue.put(log_stream.getvalue())


def get_log_path():
    logger = logging.getLogger()
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            path = handler.baseFilename
            return handler.baseFilename
    return None


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class App(Tk):
    def __init__(self, version):
        super().__init__()
        self.title(APP_TITLE)
        self.app_version = version
        self.iconbitmap(default=resource_path('wnk.ico'))

        self.quitting = False
        self.create_gui()

        self.after(50, self._handle_msg_q)

    # noinspection PyAttributeOutsideInit
    def create_gui(self):
        frm = Frame(self)
        frm.pack(fill='both', expand=True)
        Button(frm, text="Run Killer", command=self.on_btn_start_pressed).pack(side='top', anchor='w', padx=10, pady=(20, 10))

        txt_frm = Frame(frm)
        txt_frm.pack(padx=10, pady=(10, 20), fill='both', expand=True)
        self.text_box = Text(txt_frm, wrap='none', spacing1=5)
        self.text_box.grid(column=0, row=0, sticky='nsew')
        yscroll = Scrollbar(txt_frm, orient='vertical', command=self.text_box.yview)
        xscroll = Scrollbar(txt_frm, orient='horizontal', command=self.text_box.xview)
        self.text_box.configure(yscrollcommand=lambda fst, lst: autoscroll(yscroll, fst, lst),
                                xscrollcommand=lambda fst, lst: autoscroll(xscroll, fst, lst))
        yscroll.grid(row=0, column=1, sticky=NS)
        xscroll.grid(row=1, column=0, sticky=EW)
        txt_frm.grid_rowconfigure(0, weight=1)
        txt_frm.grid_columnconfigure(0, weight=1)

        Label(frm, text="Log file:").pack(padx=10, pady=(10, 0), anchor='w')
        entry = Entry(frm)
        entry.pack(padx=10, pady=(5, 10), anchor='w', fill='x')
        entry.insert(0, get_log_path())
        entry.config(state='readonly')

        Label(frm, text='version ' + self.app_version).pack(padx=10, pady=(5, 5), anchor='e')

        self.protocol("WM_DELETE_WINDOW", self._on_quit)    # window close button

    def update_text_box(self, new_text):
        self.text_box.insert('end', new_text + '\n')
        self.text_box.see('end')

    def _handle_msg_q(self):
        if self.quitting:
            return
        try:
            msg = _gui_msg_queue.get_nowait()
            if msg:
                self.update_text_box(msg)
        except queue.Empty:
            pass
        self.after(10, self._handle_msg_q)

    def _on_quit(self, evt=None):
        self.quitting = True
        self.quit()

    def on_btn_start_pressed(self):
        Runner().start()
