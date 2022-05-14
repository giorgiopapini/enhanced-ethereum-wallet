from tkinter import *
import utility_functions


class TextField(Entry):

    def __init__(self, genesis_root=None, placeholder_text="", **kwargs):
        super().__init__(**kwargs)

        self.genesis_root = genesis_root
        self.text = placeholder_text

        self.bind("<Key>", self.get_text)
        self.bind("<<Paste>>", self.paste)

    def get_text(self, event, pasted_text=None):
        if pasted_text is None:
            self.text = utility_functions.format_query(event=event)
        else:
            self.text = utility_functions.format_query(event=event, pasted=True)
            self.delete(0, len(pasted_text))

    def paste(self, event):
        pasted_text = self.genesis_root.clipboard_get()
        utility_functions.clear_field(self)
        self.insert(0, pasted_text)
        self.get_text(event=event, pasted_text=pasted_text)
