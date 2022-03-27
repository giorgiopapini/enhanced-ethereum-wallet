from tkinter import *
from Page import Page


class FundsPage(Page):

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.funds = Label(
            self.frame,
            text="Sample Funds"
        )

        self.funds.place(
            x=100, y=109
        )