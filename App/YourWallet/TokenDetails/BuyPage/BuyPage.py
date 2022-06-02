from tkinter import *


class BuyPage(Toplevel):

    def __init__(self, root, web3, **kwargs):
        super().__init__(**kwargs)

        self.root = root
        self.web3 = web3

        self.title("Buy ETH Page")
        self.geometry("380x380")
        self.resizable(False, False)

        self.label = Label(
            self,
            text="aaa"
        )
        self.label.place(
            x=30, y=30
        )
