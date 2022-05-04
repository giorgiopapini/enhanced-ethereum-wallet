from tkinter import *

from App.YourWallet.TokenDetails.TokenDetailsPage import TokenDetailsPage
from Page import Page


class TokenTile(Frame):

    TOKEN_BG_IMG = "App/YourWallet/TokenTile/background.png"
    TOKEN_ICON_IMG = "App/YourWallet/TokenTile/token_bg_img.png"
    ARROW_IMG = "App/YourWallet/TokenTile/arrow_img.png"

    # Is it possible to create a 'Tile' class that manages root, web3, next_page_frame, previous_page and eth_account?

    def __init__(self, root=None, web3=None, next_page_frame=None, previous_page=None, eth_account=None, token_symbol=None, token_amount=None, **kwargs):
        super().__init__(**kwargs)

        self.root = root
        self.web3 = web3
        self.token_symbol = token_symbol
        self.token_amount = token_amount
        self.next_page_frame = next_page_frame
        self.previous_page = previous_page
        self.eth_account = eth_account

        self.background_img = PhotoImage(file=self.TOKEN_BG_IMG)
        self.background = Label(
            self,
            image=self.background_img,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.background.pack()

        self.token_icon_img = PhotoImage(file=self.TOKEN_ICON_IMG)
        self.token_icon = Label(
            self,
            image=self.token_icon_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.token_icon.place(
            x=14, y=2,
            width=35,
            height=35
        )

        self.amount = Label(
            self,
            text=f"{self.token_symbol}: {round(self.token_amount, 4)}",
            font=("Helvetica", 11),
            bg="white"
        )
        self.amount.place(
            x=55, y=8.5
        )

        self.arrow_img = PhotoImage(file=self.ARROW_IMG)
        self.arrow = Button(
            self,
            image=self.arrow_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.to_token_details,
            relief="flat"
        )

        self.arrow.place(
            x=183, y=10,
            width=15,
            height=19
        )

    def to_token_details(self):
        Page.render_page(
            root=self.root,
            web3=self.web3,
            page=TokenDetailsPage,
            previous_page=self.previous_page,
            frame=self.next_page_frame,
            eth_account=self.eth_account
        )

