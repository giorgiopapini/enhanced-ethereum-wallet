from tkinter import *

import eth_generic_functions
from App.MenuButton import MenuButton
from App.ReusableComponents.BasicChart import BasicChart
from App.ReusableComponents.TextField import TextField
from Page import Page

from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

from datetime import datetime


class MarketAnalysisPage(Page):

    BACKGROUND = "App/MarketAnalysis/background.png"
    MENU_BG_IMG = "App/MarketAnalysis/menu_bg_img.png"
    DONE_BTN_IMG = "App/MarketAnalysis/done_btn_img.png"
    FIELD_IMG = "App/MarketAnalysis/field_img.png"

    PRICE_BTN_IMG = "App/BtnAssets/price_btn.png"
    PRICE_BTN_FOCUS_IMG = "App/BtnAssets/price_btn_focus.png"
    VOLUME_BTN_IMG = "App/BtnAssets/volume_btn.png"
    VOLUME_BTN_FOCUS_IMG = "App/BtnAssets/volume_btn_focus.png"
    MARKET_CAP_BTN_IMG = "App/BtnAssets/market_cap_btn.png"
    MARKET_CAP_BTN_FOCUS_IMG = "App/BtnAssets/market_cap_btn_focus.png"

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.graph_frame = Frame(self.frame)
        self.price_chart = None

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
            263.0, 246.5,
            image=self.background_img
        )

        self.id_field_img = PhotoImage(file=self.FIELD_IMG)
        self.id_field_bg = self.canvas.create_image(
            107.0, 139.5,
            image=self.id_field_img
        )

        self.id_field = TextField(
            master=self.frame,
            genesis_root=self.root,
            placeholder_text="bitcoin",
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.id_field.place(
            x=72.5, y=127,
            width=67.0,
            height=27
        )

        self.to_field_img = PhotoImage(file=self.FIELD_IMG)
        self.to_field_bg = self.canvas.create_image(
            228.0, 139.5,
            image=self.to_field_img
        )

        self.to_field = TextField(
            master=self.frame,
            genesis_root=self.root,
            placeholder_text="usd",
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.to_field.place(
            x=194.5, y=127,
            width=67.0,
            height=27
        )

        self.days_field_img = PhotoImage(file=self.FIELD_IMG)
        self.days_field_bg = self.canvas.create_image(
            349.0, 139.5,
            image=self.days_field_img
        )

        self.days_field = TextField(
            master=self.frame,
            genesis_root=self.root,
            placeholder_text=30,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.days_field.place(
            x=315.5, y=127,
            width=67.0,
            height=27
        )

        self.done_btn_img = PhotoImage(file=self.DONE_BTN_IMG)
        self.done_btn = Button(
            master=self.frame,
            image=self.done_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.place_update_chart,
            relief="flat"
        )

        self.done_btn.place(
            x=422, y=120,
            width=39,
            height=39
        )

        self.place_update_chart()

        # https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=eur&days=7
        # https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=eur&days=4&interval=daily
        # https://api.coingecko.com/api/v3/coins/list

        self.menu_bg_img = PhotoImage(file=self.MENU_BG_IMG)
        self.menu_bg = Label(
            self.frame,
            image=self.menu_bg_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.menu_bg.place(
            x=272, y=200,
            width=173,
            height=32
        )

        self.price_btn_img = PhotoImage(file=self.PRICE_BTN_IMG)
        self.price_btn_focus_img = PhotoImage(file=self.PRICE_BTN_FOCUS_IMG)
        self.price_btn = MenuButton(
            master=self.frame,
            image=self.price_btn_img,
            focused_image=self.price_btn_focus_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.price_btn.place(
            x=278, y=202,  # x = +3, y = -2
            width=44,
            height=28
        )

        self.mk_cap_btn_img = PhotoImage(file=self.MARKET_CAP_BTN_IMG)
        self.mk_cap_btn_focus_img = PhotoImage(file=self.MARKET_CAP_BTN_FOCUS_IMG)
        self.mk_cap_btn = MenuButton(
            master=self.frame,
            image=self.mk_cap_btn_img,
            focused_image=self.mk_cap_btn_focus_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.mk_cap_btn.place(
            x=329.3, y=202,
            width=61,
            height=28
        )

        self.volume_btn_img = PhotoImage(file=self.VOLUME_BTN_IMG)
        self.volume_btn_focus_img = PhotoImage(file=self.VOLUME_BTN_FOCUS_IMG)
        self.volume_btn = MenuButton(
            master=self.frame,
            image=self.volume_btn_img,
            focused_image=self.volume_btn_focus_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.volume_btn.place(
            x=396, y=202,
            width=44,
            height=28
        )

        self.buttons = [self.price_btn, self.mk_cap_btn, self.volume_btn]

        self.price_btn.bind("<Button>", self.btn_clicked)
        self.mk_cap_btn.bind("<Button>", self.btn_clicked)
        self.volume_btn.bind("<Button>", self.btn_clicked)

    def place_update_chart(self):
        result = eth_generic_functions.get_coin_price_data(
            coin_id=self.id_field.get().lower().strip(),
            to=self.to_field.get().lower().strip(),
            days=int(self.days_field.get())
        )

        print(result)

        self.graph_frame.destroy()
        self.graph_frame = Frame(self.frame)
        self.graph_frame.place(
            x=60, y=204
        )

        self.price_chart = BasicChart(
            master=self.graph_frame,
            data=result["prices"],
            kind="line",
            # if first value is greater than last value it means that the asset has lost value
            color="red" if result["prices"][0][1] > result["prices"][len(result["prices"]) - 1][
                1] else "green",
            title=f"{self.id_field.text.lower().strip()} / {self.to_field.text.lower().strip()}",
        )
        self.price_chart.place_chart()

    def update_menu(self, clicked_btn):
        clicked_btn.config(
            image=clicked_btn.focused_image
        )
        for btn in self.buttons:
            if btn is not clicked_btn:
                btn.config(
                    image=btn.default_image
                )

    def clean_frame(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

    def btn_clicked(self, event=None, def_btn=None):
        btn = None
        if def_btn is None:
            btn = event.widget
        elif event is None:
            btn = def_btn

        self.update_menu(btn)
        self.clean_frame()