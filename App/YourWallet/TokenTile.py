from tkinter import *
import json


class TokenTile(Frame):

    TOKEN_BG_IMG = "App/YourWallet/token_bg_img.png"

    def __init__(self, genesis_root=None, token_name=None, **kwargs):
        super().__init__(**kwargs)

        self.background_img = PhotoImage(file=self.TOKEN_BG_IMG)
        self.background = Label(
            self,
            image=self.background_img,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.background.pack()