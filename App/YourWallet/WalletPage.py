import json
from tkinter import *

import smart_contract_functions
from App.ReusableComponents.ListWidget import ListWidget
from App.ReusableComponents.ListElement import ListElement
from App.YourWallet.ImportToken.ImportTokenPage import ImportTokenPage
from App.YourWallet.TokenTile.TokenTile import TokenTile
from Page import Page


class WalletPage(Page):

    BACKGROUND_IMG = "App/YourWallet/background.png"
    TOKENS_PATH = "App/YourWallet/tokens.json"
    NFTS_PATH = "App/YourWallet/nfts.json"

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.canvas = Canvas(
            self.frame,
            bg="white",
            height=466,
            width=522,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=self.BACKGROUND_IMG)
        self.background = self.canvas.create_image(
            231.5, 227.0,
            image=self.background_img
        )

        self.wallet_eth_balance = Label(
            self.frame,
            text=f"{round(self.eth_account.get_balance('ether'), 4)}",
            font=("Helvetica", 20, "bold"),
            bg="white"
        )

        self.wallet_eth_balance.place(
            x=310, y=37,
        )

        self.tokens_list_frame = Frame(self.frame)
        self.tokens_list_frame.place(
            x=10, y=150,
            width=240,
            height=255,
        )

        self.token_list = ListWidget(
            parent=self.tokens_list_frame,
            space_between=5,
            elements=[ListElement(
                widget=TokenTile,
                genesis_root=self.root,
                token_symbol="ETH",
                token_amount=round(self.eth_account.get_balance('ether'), 4),
                height=50
            )] + self.get_tokens()
        )

        self.nfts_list_frame = Frame(self.frame)
        self.nfts_list_frame.place(
            x=280, y=150,
            width=240,
            height=255,
        )

        self.nfts_list = ListWidget(
            parent=self.nfts_list_frame,
            space_between=5,
            elements=[]
        )

        self.import_tokens = Button(
            self.frame,
            text="Import tokens",
            font=("Helvetica", 10),
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.to_page(
                page=ImportTokenPage,
                frame=self.frame,
                previous_page=WalletPage,
                eth_account=self.eth_account
            )
        )

        self.import_tokens.place(
            x=80, y=420
        )

    def get_tokens(self):
        tokens = []
        with open(self.TOKENS_PATH, "r") as file:
            raw_tokens = json.load(file)
            for token in raw_tokens:
                tokens.append(
                    ListElement(
                        widget=TokenTile,
                        genesis_root=self.root,
                        token_symbol=token["symbol"],
                        token_amount=smart_contract_functions.get_token_amount(  # This causes laggy loading, because for every token it asks the blockchain for the updated balance
                            # Solution may be saving the current balance inside the JSON file and than update it when required
                            # Solution may be loading tokens balances inside separate threads
                            web3=self.web3,
                            token_address=token["address"],
                            user_address=self.eth_account.account.address
                        ),
                        height=50
                    )
                )
            return tokens
