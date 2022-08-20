import json
from tkinter import *

import constants
import utility_functions
from App.ReusableComponents.ListElement import ListElement
from App.ReusableComponents.ListWidget import ListWidget
from App.ReusableComponents.TextField import TextField
from App.YourWallet.NFTDetails.NFTTile.NFTTile import NFTTile
from Page import Page


class NFTDetailsPage(Page):

    BACKGROUND_IMG = "App/YourWallet/NFTDetails/background.png"
    SEND_BUTTON_IMG = "App/YourWallet/NFTDetails/send_button_img.png"
    ADDRESS_FIELD_IMG = "App/YourWallet/NFTDetails/address_field_img.png"
    BACK_ARROW_IMG = "KeyImport/img1.png"

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.collection_name = kwargs.get("collection_name", "")
        self.nfts = kwargs.get("nfts", [])

        self.selected_nft = self.nfts[0]

        self.canvas = Canvas(
            self.frame,
            bg="#ffffff",
            height=466,
            width=522,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=self.BACKGROUND_IMG)
        self.background = self.canvas.create_image(
            263.5, 244.0,
            image=self.background_img
        )

        self.collection_name_label = Label(
            self.frame,
            text=f"{utility_functions.format_string(string=self.collection_name, cut_to=26)}",
            font=("OpenSansRoman-Bold", int(25)),
            bg="white"
        )
        self.collection_name_label.place(
            x=45, y=32
        )

        self.nfts_list_frame = Frame(self.frame, bg="white")
        self.nfts_list_frame.place(
            x=74, y=120,
            width=420,
            height=197
        )

        self.nfts_list = ListWidget(
            parent=self.nfts_list_frame,
            space_between=5,
            elements=self.create_nfts_list()
        )

        self.selected_nft_label = Label(
            self.frame,
            text=utility_functions.format_string(string=self.selected_nft["name"], cut_to=47),
            font=("OpenSansRoman-SemiBold", int(14.0)),
            bg="white"
        )
        self.selected_nft_label.place(
            x=45, y=345,
        )

        self.address_field_img = PhotoImage(file=self.ADDRESS_FIELD_IMG)
        self.address_field_bg = self.canvas.create_image(
            238.0, 395,
            image=self.address_field_img
        )

        self.address_field = TextField(
            master=self.frame,
            genesis_root=self.root,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.address_field.place(
            x=104.5, y=381.7,
            width=267.0,
            height=27
        )

        self.send_button_img = PhotoImage(file=self.SEND_BUTTON_IMG)
        self.send_button = Button(
            self.frame,
            image=self.send_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.send_nft,
            relief="flat",
            cursor="hand2"
        )

        self.send_button.place(
            x=408, y=380,
            width=90,
            height=39
        )

        self.back_button_img = PhotoImage(file=self.BACK_ARROW_IMG)
        self.back_button = Button(
            self.frame,
            image=self.back_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.to_page(
                page=self.previous_page,
                frame=self.frame,
                eth_account=self.eth_account
            ),
            relief="flat",
            cursor="hand2"
        )
        self.back_button.place(
            x=47, y=415
        )

    def create_nfts_list(self):
        nfts_list = []
        for nft in self.nfts:
            nfts_list.append(
                ListElement(
                    widget=NFTTile,
                    genesis_root=self.root,
                    web3=self.web3,
                    eth_account=self.eth_account,
                    nft=nft,
                    callback=self.set_active_nft,
                    height=50
                )
            )
        return nfts_list

    def set_active_nft(self, nft_clicked=None):
        self.selected_nft = nft_clicked
        self.selected_nft_label.config(text=self.selected_nft["name"])

    def send_nft(self):
        try:
            self.eth_account.send_ERC721(
                contract_address=self.selected_nft["address"],
                sender=self.eth_account.account.address,
                receiver=self.address_field.text,
                token_id=self.selected_nft["token_id"]
            )
            self.remove_nft_from_json()
            self.to_page(
                page=self.previous_page,
                frame=self.frame,
                eth_account=self.eth_account
            )
        except:
            self.address_field.show_error(error=constants.ERRORS["ERROR_SENDING_ERC721"])

    def remove_nft_from_json(self):
        path = f"{self.eth_account.account_path}/nfts.json"
        with open(path, "r+") as file:
            json_collections = json.load(file)
            json_nfts = json_collections[self.collection_name]
            for i in range(len(json_nfts)):
                if json_nfts[i] == self.selected_nft:
                    if len(json_nfts) == 1:
                        del json_collections[self.collection_name]
                        break
                    else:
                        del json_collections[self.collection_name][i]
                        break

            file.seek(0)
            json.dump(json_collections, file)
            file.truncate()
