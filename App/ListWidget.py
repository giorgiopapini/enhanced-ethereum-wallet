from tkinter import *


class ListWidget:

    def __init__(self, parent=None, elements=None, **kwargs):
        self.parent = parent
        self.elements = elements
        self.space_between = kwargs.get("space_between", 1)

        self.canvas = Canvas(self.parent)
        self.frame = Frame(self.canvas)

        self.display_elements()

        self.canvas.create_window(0, 0, anchor='nw', window=self.frame)
        self.canvas.update_idletasks()

        self.scrollbar = Scrollbar(
            self.parent,
            orient="vertical",
            command=self.canvas.yview
        )
        self.canvas.configure(
            scrollregion=self.canvas.bbox('all'),
            yscrollcommand=self.scrollbar.set
        )

        self.canvas.place(
            x=0, y=0
        )
        self.scrollbar.pack(fill='y', side='right')

    def display_elements(self):
        for element in self.elements:
            label = Label(
                self.frame,
                image=element,
            )
            label.pack(
                pady=self.space_between
            )
            label.bind("<Button>", self.clicked)

    def clicked(self, event):
        print(event.widget.cget("text"))
