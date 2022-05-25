from tkinter import *

import utility_functions
from App.YourWallet.NFTDetails.NFTDetailsPage import NFTDetailsPage
from Page import Page


class NFTTile(Frame):

    TOKEN_BG_IMG = "App/YourWallet/TokenTile/background.png"
    ARROW_IMG = "App/YourWallet/TokenTile/arrow_img.png"

    def __init__(self, genesis_root=None, web3=None, next_page_frame=None, previous_page=None, eth_account=None, collection_name=None, collection=None, **kwargs):
        super().__init__(**kwargs)

        self.genesis_root = genesis_root
        self.web3 = web3
        self.next_page_frame = next_page_frame
        self.previous_page = previous_page
        self.eth_account = eth_account

        self.collection_name = collection_name
        self.collection = collection

        self.background_img = PhotoImage(file=self.TOKEN_BG_IMG)
        self.background = Label(
            self,
            image=self.background_img,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.background.pack()

        self.collection_name_label = Label(
            self,
            text=f"{utility_functions.format_string(string=self.collection_name, cut_to=20)}",
            font=("Arial", 11),
            bg="white"
        )
        self.collection_name_label.place(
            x=20, y=8.5
        )

        self.arrow_img = PhotoImage(file=self.ARROW_IMG)
        self.arrow = Button(
            self,
            image=self.arrow_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.to_nfts_details,
            relief="flat"
        )

        self.arrow.place(
            x=183, y=10,
            width=15,
            height=19
        )

    def to_nfts_details(self):
        Page.render_page(
            root=self.genesis_root,
            web3=self.web3,
            page=NFTDetailsPage,
            previous_page=self.previous_page,
            frame=self.next_page_frame,
            eth_account=self.eth_account,
            collection_name=self.collection_name,
            nfts=self.collection
        )
