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
    FIELD_IMG = "App/MarketAnalysis/field_img.png"

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
            263.0, 242.0,
            image=self.background_img
        )

        self.id_field_img = PhotoImage(file=self.FIELD_IMG)
        self.id_field_bg = self.canvas.create_image(
            133.0, 139.5,
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
            width=121.0,
            height=27
        )

        self.to_field_img = PhotoImage(file=self.FIELD_IMG)
        self.to_field_bg = self.canvas.create_image(
            315.0, 139.5,
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
            x=254.5, y=127,
            width=121.0,
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

    def place_update_chart(self):
        result = eth_generic_functions.get_coin_price_data(
            coin_id=self.id_field.text.lower().strip(),
            to=self.to_field.text.lower().strip(),
            days=365
        )

        self.graph_frame.destroy()
        self.graph_frame = Frame(self.frame)
        self.graph_frame.place(
            x=60, y=196.5
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
