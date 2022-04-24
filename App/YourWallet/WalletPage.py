from tkinter import *

from App.ReusableComponents.ListWidget import ListWidget
from App.ReusableComponents.ListElement import ListElement
from App.YourWallet.TokenTile.TokenTile import TokenTile
from Page import Page


class WalletPage(Page):

    BACKGROUND_IMG = "App/YourWallet/background.png"

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.canvas = Canvas(
            self.frame,
            bg="white",
            height=466,
            width=522,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=self.BACKGROUND_IMG)
        self.background = self.canvas.create_image(
            231.5, 227.0,
            image=self.background_img
        )

        self.wallet_eth_balance = Label(
            self.frame,
            text=f"{round(self.eth_account.get_balance('ether'), 4)}",
            font=("Helvetica", 20, "bold"),
            bg="white"
        )

        self.wallet_eth_balance.place(
            x=310, y=37,
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
                ListElement(
                    widget=TokenTile,
                    genesis_root=self.root,
                    token_name="example2",
                    bg="red",
                    height=50
                )
            ]
        )

        self.nfts_list_frame = Frame(self.frame)
        self.nfts_list_frame.place(
            x=280, y=150,
            width=240,
            height=255,
        )

        self.nfts_list = ListWidget(
            parent=self.nfts_list_frame,
            space_between=5,
            elements=[
                ListElement(
                    widget=TokenTile,
                    genesis_root=self.root,
                    token_name="example1",
                    bg="red",
                    height=50
                )
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

