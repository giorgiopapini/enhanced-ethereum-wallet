from tkinter import *
import json


class TokenTile(Frame):

    TOKEN_BG_IMG = "App/YourWallet/TokenTile/background.png"
    TOKEN_ICON_IMG = "App/YourWallet/TokenTile/token_bg_img.png"
    ARROW_IMG = "App/YourWallet/TokenTile/arrow_img.png"

    def __init__(self, genesis_root=None, token_name=None, **kwargs):
        super().__init__(**kwargs)

        self.genesis_root = genesis_root
        self.token_name = token_name

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

        self.arrow_img = PhotoImage(file=self.ARROW_IMG)
        self.arrow = Button(
            self,
            image=self.arrow_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.arrow.place(
            x=183, y=10,
            width=15,
            height=19
        )

    # Arrow button will render a new page containing every transaction made with that specific token (history)

