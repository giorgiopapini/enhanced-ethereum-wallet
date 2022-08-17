from tkinter import *

import utility_functions


class CoinTile(Frame):

    COIN_BG_IMG = "App/MarketAnalysis/CoinsList/CoinTile/background.png"
    COPY_BTN_IMG = "App/MarketAnalysis/CoinsList/CoinTile/copy_btn_img.png"

    def __init__(self, genesis_root=None, web3=None, coin=None, **kwargs):
        super().__init__(**kwargs)

        self.genesis_root = genesis_root
        self.web3 = web3
        self.coin = coin

        self.background_img = PhotoImage(file=self.COIN_BG_IMG)
        self.background = Label(
            self,
            image=self.background_img,
            bd=0,
            highlightthickness=0,
            relief="flat"
        )
        self.background.pack()

        self.coin_name_label = Label(
            self,
            text=(utility_functions.format_string(coin["id"], 29)),
            font=("Arial", 9),
            bg="white"
        )
        self.coin_name_label.place(
            x=14, y=5
        )

        self.copy_btn_img = PhotoImage(file=self.COPY_BTN_IMG)
        self.copy_btn = Button(
            self,
            image=self.copy_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.copy_btn_clicked,
            relief="flat",
            cursor="hand2"
        )

        self.copy_btn.place(
            x=188, y=6.5,
            width=18,
            height=17
        )

    def copy_btn_clicked(self):
        if self.genesis_root is not None:
            self.genesis_root.clipboard_clear()
            self.genesis_root.clipboard_append(self.coin["id"])
            self.genesis_root.update()


