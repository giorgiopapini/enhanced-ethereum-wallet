import json
from tkinter import *

from App.ReusableComponents.ListWidget import ListWidget
from App.ReusableComponents.ListElement import ListElement
from App.YourWallet.ImportNFT.ImportNFTPage import ImportNFTPage
from App.YourWallet.ImportToken.ImportTokenPage import ImportTokenPage
from App.YourWallet.CollectionTile.CollectionTile import CollectionTile
from App.YourWallet.TokenTile.TokenTile import TokenTile
from Page import Page


class WalletPage(Page):

    BACKGROUND_IMG = "App/YourWallet/background.png"
    IMPORT_TOKEN_IMG = "App/YourWallet/import_token_img.png"
    IMPORT_NFT_IMG = "App/YourWallet/import_nft_img.png"

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.get_collections()

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
            text=f"{round(self.eth_account.get_balance('ether'), 4)}"[0:8],
            font=("Helvetica", 20, "bold"),  # ("OpenSansRoman-SemiBold", int(20.0))
            bg="white"
        )

        self.wallet_eth_balance.place(
            x=310, y=37,
        )

        self.tokens_list_frame = Frame(self.frame)
        self.tokens_list_frame.place(
            x=10, y=146,
            width=240,
            height=260,
        )

        self.token_list = ListWidget(
            parent=self.tokens_list_frame,
            space_between=5,
            elements=[ListElement(
                widget=TokenTile,
                genesis_root=self.root,
                web3=self.web3,
                next_page_frame=self.frame,
                previous_page=WalletPage,
                eth_account=self.eth_account,
                height=50
            )] + self.get_tokens()
        )

        self.nfts_list_frame = Frame(self.frame)
        self.nfts_list_frame.place(
            x=280, y=146,
            width=240,
            height=260,
        )

        self.nfts_list = ListWidget(
            parent=self.nfts_list_frame,
            space_between=5,
            elements=self.get_collections()
        )

        self.import_tokens_img = PhotoImage(file=self.IMPORT_TOKEN_IMG)
        self.import_tokens = Button(
            self.frame,
            image=self.import_tokens_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.to_page(
                page=ImportTokenPage,
                frame=self.frame,
                previous_page=WalletPage,
                eth_account=self.eth_account
            ),
            cursor="hand2"
        )
        self.import_tokens.place(
            x=79.8, y=430
        )

        self.import_nft_img = PhotoImage(file=self.IMPORT_NFT_IMG)
        self.import_nft = Button(
            self.frame,
            image=self.import_nft_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.to_page(
                page=ImportNFTPage,
                frame=self.frame,
                previous_page=WalletPage,
                eth_account=self.eth_account
            ),
            cursor="hand2"
        )
        self.import_nft.place(
            x=352, y=430
        )

    def get_tokens(self):
        path = f"{self.eth_account.account_path}/tokens.json"

        tokens = []
        with open(path, "r") as file:
            raw_tokens = json.load(file)
            for token in raw_tokens:
                tokens.append(
                    ListElement(
                        widget=TokenTile,
                        genesis_root=self.root,
                        web3=self.web3,
                        next_page_frame=self.frame,
                        previous_page=WalletPage,
                        eth_account=self.eth_account,
                        token=token,
                        height=50
                    )
                )
            return tokens

    def get_collections(self):
        path = f"{self.eth_account.account_path}/nfts.json"

        collections = []
        with open(path, "r") as file:
            raw_collections = json.load(file)
            for collection in raw_collections:
                collections.append(
                    ListElement(
                        widget=CollectionTile,
                        genesis_root=self.root,
                        web3=self.web3,
                        next_page_frame=self.frame,
                        previous_page=WalletPage,
                        eth_account=self.eth_account,
                        collection_name=collection,
                        collection=raw_collections[collection],
                        height=50,
                    )
                )
            return collections
