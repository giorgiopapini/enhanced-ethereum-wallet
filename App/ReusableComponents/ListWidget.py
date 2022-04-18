from tkinter import *

import utility_functions
from App.ReusableComponents.ListElement import ListElement


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
        if self.is_empty(self.elements) is False:
            for element in self.elements:
                utility_functions.check_var_type(
                    variable=element,
                    requested_type=ListElement,
                    error_msg="ListWidget elements array accepts only variables of type ListElement"
                )
                widget = self.define_object(element)  # Uses ListElement data for declaring the actual widget
                widget.pack(
                    pady=self.space_between
                )
                widget.bind_all("<Button>", self.clicked)

    def is_empty(self, arr):
        if len(arr) is 0:
            empty_list = Label(
                self.frame,
                text="Nothing to see here yet"
            )
            empty_list.pack()
            return True
        else:
            return False

    def define_object(self, element):
        obj = element.widget(master=self.frame)
        obj.config(**element.widget_attributes)
        print(vars(obj))
        return obj

    def clicked(self, event):
        print(event.widget)
