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

        self.tokens_label = Label(
            self.frame,
            text="Tokens:",
            font=("Helvetica", 15)
        )

        self.tokens_label.place(
            x=80, y=105
        )

        self.nfts_label = Label(
            self.frame,
            text="NFTs:",
            font=("Helvetica", 15)
        )

        self.nfts_label.place(
            x=353, y=105
        )

        self.tokens_list_frame = Frame(self.frame)
        self.tokens_list_frame.place(
            x=10, y=150,
            width=240,
            height=255,
        )

        self.token_list = ListWidget(
            parent=self.tokens_list_frame,
            space_between=5,
            elements=[
                #PhotoImage(file=self.TOKEN_BG_IMG)
            ]
        )

        self.nfts_list_frame = Frame(self.frame)
        self.nfts_list_frame.place(
            x=270, y=150,
            width=240,
            height=255,
        )

        self.nfts_list = ListWidget(
            parent=self.nfts_list_frame,
            space_between=5,
            elements=[
                PhotoImage(file=self.TOKEN_BG_IMG)
            ]
        )

        self.import_tokens = Button(
            self.frame,
            text="Import tokens",
            font=("Helvetica", 10),
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.import_tokens.place(
            x=80, y=420
        )

