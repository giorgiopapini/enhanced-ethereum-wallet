from tkinter import *
from Page import Page


class WalletPage(Page):

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.wallet = Label(
            self.frame,
            text="Sample Wallet"
        )

        self.wallet.place(
            x=150, y=150,
        )
