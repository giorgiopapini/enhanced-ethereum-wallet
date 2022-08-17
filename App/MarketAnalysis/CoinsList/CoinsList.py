import json
from tkinter import *

from App.MarketAnalysis.CoinsList.CoinTile.CoinTile import CoinTile
from App.ReusableComponents.ListElement import ListElement
from App.ReusableComponents.ListWidget import ListWidget
from App.ReusableComponents.TextField import TextField


class CoinsList(Toplevel):

    BACKGROUND = "App/MarketAnalysis/CoinsList/background.png"
    TEXTBOX_IMG = "App/MarketAnalysis/CoinsList/textbox_img.png"
    DONE_BTN_IMG = "App/MarketAnalysis/CoinsList/done_btn_img.png"
    LOAD_MORE_BTN_IMG = "App/MarketAnalysis/CoinsList/load_more_btn.png"

    COINS_PATH_JSON = "App/MarketAnalysis/CoinsList/coins.json"
    COIN_RANGE = 20

    def __init__(self, root, web3, **kwargs):
        super().__init__(**kwargs)
        self.root = root
        self.web3 = web3

        self.coins = []
        self.raw_coins = []
        self.current_index = 0

        self.title("Coins List")
        self.geometry("301x380")
        self.resizable(False, False)

        self.get_coins()
        self.render_coins()

        self.canvas = Canvas(
            self,
            bg="#ffffff",
            height=380,
            width=301,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=self.BACKGROUND)
        self.background = self.canvas.create_image(
            127.0, 64.5,
            image=self.background_img
        )

        self.search_box_img = PhotoImage(file=self.TEXTBOX_IMG)
        self.search_box_bg = self.canvas.create_image(
            124.5, 117.0,
            image=self.search_box_img
        )

        self.search_box = TextField(
            master=self,
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            clean_on_click=True,
            callback_on_click=self.reinitialize_list
        )

        self.search_box.place(
            x=41.0, y=106,
            width=167.0,
            height=22
        )

        self.done_btn_img = PhotoImage(file=self.DONE_BTN_IMG)
        self.done_btn = Button(
            self,
            image=self.done_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.scrape_coins,
            relief="flat",
            cursor="hand2"
        )

        self.done_btn.place(
            x=238, y=101,
            width=32,
            height=32
        )

        self.coins_list_frame = Frame(self)
        self.coins_list_frame.place(
            x=28, y=147,
            width=245,
            height=193,
        )

        self.coins_list = ListWidget(
            parent=self.coins_list_frame,
            space_between=3,
            elements=self.coins
        )

        self.load_more_frame = Frame(self, bg="white")
        self.load_more_frame.place(
            x=0, y=350,
            width=301,
            height=30,
        )

        self.load_more_btn_img = PhotoImage(file=self.LOAD_MORE_BTN_IMG)
        self.load_more_btn = Button(
            self.load_more_frame,
            image=self.load_more_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.load_more_coins,
            relief="flat",
            cursor="hand2"
        )

        self.load_more_btn.pack()

    def get_coins(self):
        with open(self.COINS_PATH_JSON, "r", encoding="utf8") as file:
            self.raw_coins = json.load(file)

    def render_coins(self):
        if self.current_index < len(self.raw_coins):
            for i in range(self.current_index, self.current_index + self.COIN_RANGE):
                self.coins.append(
                    ListElement(
                        widget=CoinTile,
                        genesis_root=self.root,
                        coin=self.raw_coins[i],
                        height=50
                    )
                )
            self.current_index += self.COIN_RANGE

    def scrape_coins(self):
        self.coins.clear()
        query = self.search_box.get()
        if query is not "":
            for coin in self.raw_coins:
                if query in coin["symbol"]:
                    self.coins.append(
                        ListElement(
                            widget=CoinTile,
                            genesis_root=self.root,
                            coin=coin,
                            height=50
                        )
                    )

        self.coins_list.refresh_list(
            parent_frame=self.coins_list_frame,
            elements=self.coins
        )

        self.coins_list_frame.place(
            x=28, y=156,
            width=245,
            height=193,
        )

        self.load_more_btn.pack_forget()

    def load_more_coins(self):
        self.render_coins()
        self.coins_list.refresh_list(
            parent_frame=self.coins_list_frame,
            elements=self.coins
        )

    def reinitialize_list(self):
        if self.search_box.get() == "":
            self.current_index = 0
            self.coins.clear()

            self.render_coins()
            self.coins_list.destroy()
            self.coins_list.__init__(parent=self.coins_list_frame, elements=self.coins)

            self.coins_list_frame.place(
                x=28, y=147,
                width=245,
                height=193,
            )
            self.load_more_btn.pack()
