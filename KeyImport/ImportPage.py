from tkinter import *

import constants
from App.ReusableComponents.TextField import TextField
from EthereumAccount import EthereumAccount
from Page import Page
from SignUp.SignUpPage import SignUpPage


class ImportPage(Page):

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)
        self.canvas = Canvas(
            root,
            bg="#ffffff",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.prv_key_field_img = PhotoImage(file=f"KeyImport/img_textBox0.png")
        self.prv_key_field = self.canvas.create_image(
            400.0, 264.5,
            image=self.prv_key_field_img)

        self.prv_key_field = TextField(
            genesis_root=self.root,
            bd=0,
            bg="#ffffff",
            highlightthickness=0)

        self.prv_key_field.place(
            x=210.5, y=250,
            width=379.0,
            height=31)

        self.img0 = PhotoImage(file=f"KeyImport/img0.png")
        self.b0 = Button(
            image=self.img0,
            borderwidth=0,
            highlightthickness=0,
            command=self.import_account,
            relief="flat",
            cursor="hand2"
        )

        self.b0.place(
            x=292, y=310,
            width=185,
            height=59)

        self.background_img = PhotoImage(file=f"KeyImport/background.png")
        self.background = self.canvas.create_image(
            524.5, 203.0,
            image=self.background_img)

        self.img1 = PhotoImage(file=f"KeyImport/img1.png")
        self.b1 = Button(
            image=self.img1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.to_page(
                page=self.previous_page,
            ),
            cursor="hand2",
            relief="flat")

        self.b1.place(
            x=28, y=23,
            width=38,
            height=38)

    def import_account(self):
        try:
            account = self.web3.eth.account.from_key(self.prv_key_field.text)
            self.to_page(
                page=SignUpPage,
                previous_page=self.previous_page,
                eth_account=EthereumAccount(web3=self.web3, account=account),
            )
        except ValueError:
            self.prv_key_field.show_error(error=constants.ERRORS["ERROR_INCORRECT_PRIVATE_KEY"])

