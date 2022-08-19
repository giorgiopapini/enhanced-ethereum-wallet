from tkinter import *

import utility_functions
from App.ReusableComponents.ListElement import ListElement


class ListWidget:

    def __init__(self, parent=None, elements=None, **kwargs):
        self.parent = parent
        self.elements = elements
        self.space_between = kwargs.get("space_between", 1)

        self.canvas = Canvas(
            self.parent,
            bg="white",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.frame = Frame(self.canvas, bg="white")

        self.display_elements()

        self.canvas.create_window(0, 0, anchor='nw', window=self.frame)
        self.canvas.update_idletasks()

        self.scrollbar = Scrollbar(
            self.parent,
            orient="vertical",
            command=self.canvas.yview,
            cursor="hand2"
        )
        self.canvas.configure(
            scrollregion=self.canvas.bbox('all'),
            yscrollcommand=self.scrollbar.set,
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

    def is_empty(self, arr):
        if arr is None or len(arr) is 0:
            empty_list = Label(
                self.frame,
                text="Nothing to see here yet",
                bg="white"
            )
            empty_list.pack()
            return True
        else:
            return False

    def define_object(self, element):
        obj = element.widget(
            master=self.frame,
            width=self.frame.cget("width"),
            **element.widget_attributes
        )
        return obj

    def destroy(self):
        self.canvas.delete("all")
        self.scrollbar.destroy()
        self.frame.destroy()

    def refresh_list(self, parent_frame=None, elements=None):
        self.destroy()
        self.__init__(parent=parent_frame, elements=elements)
