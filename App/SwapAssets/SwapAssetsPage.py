from tkinter import *

import utility_functions
from Page import Page


class FundsPage(Page):

    BACKGROUND = "App/SwapAssets/background.png"
    SWAP_BTN_IMG = "App/SwapAssets/swap_btn_img.png"

    swap_eth_with_token_toplevel = None
    swap_token_with_token_toplevel = None

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.canvas = Canvas(
            self.frame,
            bg="#ffffff",
            height=466,
            width=522,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=self.BACKGROUND)
        self.background = self.canvas.create_image(
            257.0, 233.5,
            image=self.background_img
        )

        self.swap_eth_to_token_btn_img = PhotoImage(file=self.SWAP_BTN_IMG)
        self.swap_eth_to_token_btn = Button(
            master=self.frame,
            image=self.swap_eth_to_token_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.show_toplevel(self.swap_eth_with_token_toplevel),
            relief="flat",
            cursor="hand2"
        )

        self.swap_eth_to_token_btn.place(
            x=99, y=345,
            width=90,
            height=39
        )

        self.swap_token_to_token_btn_img = PhotoImage(file=self.SWAP_BTN_IMG)
        self.swap_token_to_token_btn = Button(
            master=self.frame,
            image=self.swap_token_to_token_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.show_toplevel(self.swap_token_with_token_toplevel),
            relief="flat",
            cursor="hand2"
        )

        self.swap_token_to_token_btn.place(
            x=332, y=345,
            width=90,
            height=39
        )

    def show_toplevel(self, toplevel):
        pass
