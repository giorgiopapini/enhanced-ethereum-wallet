from tkinter import *

import constants
import utility_functions


class TextField(Entry):

    text = ""

    def __init__(self, genesis_root=None, callback=None, placeholder_text="", **kwargs):
        super().__init__(**kwargs)

        self.genesis_root = genesis_root
        self.state = kwargs.get("state")
        self.override_text(text=placeholder_text)
        self.callback = callback

        self.bind("<Key>", self.get_text)
        self.bind("<<Paste>>", self.paste)
        self.bind("<Button>", self.clear_error)

    def get_text(self, event, pasted_text=None):
        self.clear_error(event=event)
        if pasted_text is None:
            self.text = utility_functions.format_query(event=event)
        else:
            self.text = utility_functions.format_query(event=event, pasted=True)
            self.delete(0, len(pasted_text))

        if self.callback is not None:
            self.callback()

    def paste(self, event):
        pasted_text = self.genesis_root.clipboard_get()
        self.clear_field()
        self.insert(0, pasted_text)
        self.get_text(event=event, pasted_text=pasted_text)

    def clear_error(self, event):
        for error in constants.ERRORS:
            if event.widget.get() == constants.ERRORS[error]:
                self.clear_field()

    def clear_field(self):
        self.config(state="normal")
        self.delete(0, END)
        self.text = ""
        self.config(fg="black")
        self.config(state=self.state)

    def override_text(self, text=""):
        self.clear_field()
        self.config(state="normal")
        self.insert(END, text)
        self.text = text
        self.config(state=self.state)

    def show_error(self, error=None):
        self.text = ""
        self.config(state="normal")
        self.delete(0, END)
        self.config(fg="red")
        self.insert(END, error)
        self.config(state=self.state)
