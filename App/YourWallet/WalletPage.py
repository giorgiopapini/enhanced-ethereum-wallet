from tkinter import *

from App.ListWidget import ListWidget
from Page import Page


class WalletPage(Page):

    TOKEN_BG_IMG = "App/YourWallet/token_bg_img.png"

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.wallet_eth_balance = Label(
            self.frame,
            text=f"Total ETH value: {round(self.eth_account.get_balance('ether'), 4)} ETH",
            font=("Helvetica", 20)
        )

        self.wallet_eth_balance.place(
            x=40, y=40,
        )

        self.tokens = Label(
            self.frame,
            text=f"Tokens:",
            font=("Helvetica", 15)
        )

        self.tokens.place(
            x=90, y=120
        )

        self.tokens_list_frame = Frame(self.frame)
        self.tokens_list_frame.place(
            x=20, y=165,
            width=240,
            height=270,
        )

        self.list = ListWidget(
            parent=self.tokens_list_frame,
            space_between=5,
            elements=[
                PhotoImage(file=self.TOKEN_BG_IMG)
            ]
        )
