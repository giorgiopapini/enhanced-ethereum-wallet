from tkinter import *

import utility_functions
from Page import Page


class ImportNFTPage(Page):

    BACKGROUND_IMG = "App/YourWallet/ImportNFT/background.png"
    INPUT_FIELD_IMG = "App/Contacts/AddContact/img_textBox.png"
    DISABLED_TEXT_BOX_IMAGE = "App/YourWallet/ImportToken/disabled_textbox_img.png"
    IMPORT_BUTTON_IMG = "App/YourWallet/ImportNFT/import_button.png"

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

        self.address_field = Entry(
            self.frame,
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

        self.nft_id_field = Entry(
            self.frame,
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

        self.nft_url_field = Entry(
            self.frame,
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

        self.address_field.bind("<Key>", self.get_field_text)
        self.nft_id_field.bind("<Key>", self.get_field_text)

    def get_field_text(self, event):
        pass

    def import_nft(self):
        pass
