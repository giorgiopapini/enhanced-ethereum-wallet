from tkinter import *

import eth_generic_functions
from App.ReusableComponents.BasicChart import BasicChart
from App.ReusableComponents.TextField import TextField
from Page import Page

from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

from datetime import datetime


class AutomationPage(Page):

    BACKGROUND = "App/MarketAnalysis/background.png"
    DONE_BTN_IMG = "App/MarketAnalysis/done_btn_img.png"
    ID_FIELD_IMG = "App/MarketAnalysis/id_field_img.png"

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
            263.0, 242.0,
            image=self.background_img
        )

        self.id_field_img = PhotoImage(file=self.ID_FIELD_IMG)
        self.id_field = self.canvas.create_image(
            160.5, 139.5,
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
            width=176.0,
            height=27
        )

        self.done_btn_img = PhotoImage(file=self.DONE_BTN_IMG)
        self.done_btn = Button(
            master=self.frame,
            image=self.done_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.update_chart,
            relief="flat"
        )

        self.done_btn.place(
            x=275, y=120,
            width=39,
            height=39
        )

        self.result = eth_generic_functions.get_coin_price_data(
            coin_id=self.id_field.text,
            to="eur",
            days=1
        )

        self.graph_frame = Frame(self.frame)
        self.graph_frame.place(
            x=60, y=196.5
        )

        self.price_chart = BasicChart(
            master=self.graph_frame,
            data=self.result["prices"],
            kind="line",
            # if first value is greater than last value it means that the asset has lost value
            color="red" if self.result["prices"][0][1] > self.result["prices"][len(self.result["prices"]) - 1][1] else "green",
            title=f"{self.id_field.text} / eur",
        )
        self.price_chart.place_chart()

        # https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=eur&days=7
        # https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=eur&days=4&interval=daily
        # https://api.coingecko.com/api/v3/coins/list

    def update_chart(self):
        print("update")