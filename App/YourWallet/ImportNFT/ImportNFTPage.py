import json
from tkinter import *

import constants
import eth_generic_functions
import utility_functions
from App.ReusableComponents.TextField import TextField
from Page import Page


class ImportNFTPage(Page):

    BACKGROUND_IMG = "App/YourWallet/ImportNFT/background.png"
    INPUT_FIELD_IMG = "App/Contacts/AddContact/img_textBox.png"
    DISABLED_TEXT_BOX_IMAGE = "App/YourWallet/ImportToken/disabled_textbox_img.png"
    IMPORT_BUTTON_IMG = "App/YourWallet/ImportNFT/import_button.png"
    COPY_BUTTON_IMG = "App/Contacts/ContactTile/copy_img.png"
    BACK_ARROW_IMG = "KeyImport/img1.png"
    NFT_JSON_PATH = "App/YourWallet/nfts.json"

    nft_metadata = {}

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

        self.background_img = PhotoImage(file=self.BACKGROUND_IMG)
        self.background = self.canvas.create_image(
            144.5, 165.5,
            image=self.background_img
        )

        self.import_button_img = PhotoImage(file=self.IMPORT_BUTTON_IMG)
        self.import_button = Button(
            self.frame,
            image=self.import_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.import_nft,
            relief="flat"
        )

        self.import_button.place(
            x=290, y=382,
            width=169,
            height=59
        )

        self.address_field_img = PhotoImage(file=self.INPUT_FIELD_IMG)
        self.address_field_bg = self.canvas.create_image(
            217.0, 154.5,
            image=self.address_field_img
        )

        self.address_field = TextField(
            master=self.frame,
            genesis_root=self.root,
            callback=self.get_nft_data,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.address_field.place(
            x=73.5, y=142,
            width=287.0,
            height=27
        )

        self.nft_id_field_img = PhotoImage(file=self.INPUT_FIELD_IMG)
        self.nft_id_field_bg = self.canvas.create_image(
            217.0, 237.5,
            image=self.nft_id_field_img
        )

        self.nft_id_field = TextField(
            master=self.frame,
            genesis_root=self.root,
            callback=self.get_nft_data,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.nft_id_field.place(
            x=73.5, y=225,
            width=287.0,
            height=27
        )

        self.nft_url_field_img = PhotoImage(file=self.DISABLED_TEXT_BOX_IMAGE)
        self.nft_url_field_bg = self.canvas.create_image(
            217.0, 320.5,
            image=self.nft_url_field_img
        )

        self.nft_url_field = TextField(
            master=self.frame,
            genesis_root=self.root,
            bd=0,
            bg="#f0f0f0",
            highlightthickness=0,
            state="disabled"
        )

        self.nft_url_field.place(
            x=73.5, y=308,
            width=287.0,
            height=27
        )

        self.copy_button_img = PhotoImage(file=self.COPY_BUTTON_IMG)
        self.copy_button = Button(
            self.frame,
            image=self.copy_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.copy_to_clipboard,
            relief="flat"
        )

        self.copy_button.place(
            x=396, y=306,
            width=30,
            height=30
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
            relief="flat"
        )
        self.back_button.place(
            x=60, y=383
        )

    def get_nft_data(self):
        try:
            self.nft_metadata = eth_generic_functions.get_nft_metadata(
                web3=self.web3,
                contract_address=self.address_field.text,
                token_id=int(self.nft_id_field.text)
            )
            self.nft_url_field.clear_field()
            self.nft_url_field.override_text(text=self.nft_metadata["image"])
        except:
            self.nft_url_field.show_error(error=constants.ERRORS["ERROR_ERC721_NOT_FOUND"])

    def import_nft(self):
        with open(self.NFT_JSON_PATH, "r+") as file:
            collections = json.load(file)
            try:
                collection_name = eth_generic_functions.get_contract_name(
                    contract_address=self.nft_metadata["address"],
                    web3=self.web3
                )
                if collection_name not in collections:
                    collections[collection_name] = []

                nfts = collections[collection_name]
                nft_alredy_saved = utility_functions.is_nft_saved(
                    nfts=nfts,
                    token_address=self.address_field.text,
                    token_id=self.nft_id_field.text,
                )
                is_owner = eth_generic_functions.get_nft_owner(
                    nft_address=self.nft_metadata["address"],
                    nft_id=self.nft_metadata["token_id"],
                    user_address=self.eth_account.account.address,
                    web3=self.web3
                )
                fields_valid = utility_functions.check_fields_validity(
                    fields=[self.nft_url_field],
                    error=constants.ERRORS["ERROR_ERC721_NOT_FOUND"],
                )

                if fields_valid is True and nft_alredy_saved is False:  # and is_owner is True
                    nfts.append(
                        {
                            "name": self.nft_metadata["name"],
                            "address": self.address_field.text,
                            "token_id": self.nft_id_field.text,
                            "image": self.nft_metadata["image"]
                        }
                    )
                    nfts.sort(key=lambda x: x["name"].lower())

                    collections[collection_name] = nfts

                    file.seek(0)
                    json.dump(collections, file)
                    file.truncate()

                    self.to_page(
                        page=self.previous_page,
                        previous_page=None,
                        frame=self.frame,
                        eth_account=self.eth_account
                    )
                else:
                    self.address_field.show_error(
                        error=constants.ERRORS["ERROR_ERC721_NOT_VALID"] if is_owner else constants.ERRORS["ERROR_ERC721_DIFFERENT_OWNER"]
                    )
                    self.nft_id_field.show_error(
                        error=constants.ERRORS["ERROR_ERC721_NOT_VALID"] if is_owner else constants.ERRORS["ERROR_ERC721_DIFFERENT_OWNER"]
                    )
            except KeyError:
                self.address_field.show_error(error=constants.ERRORS["ERROR_ERC721_NOT_VALID"])
                self.nft_id_field.show_error(error=constants.ERRORS["ERROR_ERC721_NOT_VALID"])

        self.nft_url_field.clear_field()

    def copy_to_clipboard(self):
        if self.root is not None:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.nft_url_field.text)
            self.root.update()
