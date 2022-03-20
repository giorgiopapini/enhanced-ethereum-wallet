from tkinter import *
import utility_functions
import constants


class Page(Frame):

    def __init__(self, root=None, web3=None, **kwargs):
        Frame.__init__(self, root)
        self.root = root
        self.web3 = web3
        self.previous_page = kwargs.get("previous_page", None)

    # Capire come usare **kwargs, sia per rendere piú generico e riutilizzabile il codice sia per renderlo piú esplicito
    # e comprensibile

    def to_page(self, page=None, previous_page=None, **kwargs):
        page(self.root, self.web3, previous_page=previous_page, **kwargs)
        print(previous_page)

