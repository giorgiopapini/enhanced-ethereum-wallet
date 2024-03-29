from tkinter import *

import constants
import utility_functions
from App.ReusableComponents.TextField import TextField
from App.YourWallet.WalletPage import WalletPage
from EthereumAccount import EthereumAccount

from KeyImport.ImportPage import ImportPage
from App.AppPageManager import AppPageManager
from Login.AccountList.AccountList import AccountList
from Page import Page


class LoginPage(Page):

    account_list_toplevel = None

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.password = ""

        self.canvas = Canvas(
            root,
            bg="#ffffff",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=f"Login/background.png")
        self.background = self.canvas.create_image(
            524.5, 203.0,
            image=self.background_img)

        self.img0 = PhotoImage(file=f"Login/img0.png")
        self.b0 = Button(
            image=self.img0,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat",
            cursor="hand2"
        )

        self.b0.place(
            x=307, y=279,
            width=185,
            height=59)

        self.entry0_img = PhotoImage(file=f"Login/img_textBox0.png")
        self.entry0_bg = self.canvas.create_image(
            398.5, 228.5,
            image=self.entry0_img)

        self.entry0 = TextField(
            bd=0,
            bg="#ffffff",
            highlightthickness=0)

        self.entry0.place(
            x=272.5, y=214,
            width=252.0,
            height=31)

        self.img1 = PhotoImage(file=f"Login/img1.png")
        self.b1 = Button(
            image=self.img1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.to_page(
                page=ImportPage,
                previous_page=LoginPage
            ),
            cursor="hand2",
            relief="flat")

        self.b1.place(
            x=307, y=334,
            width=185,
            height=33)

        self.img2 = PhotoImage(file=f"Login/img2.png")
        self.b2 = Button(
            image=self.img2,
            borderwidth=0,
            highlightthickness=0,
            command=self.show_account_list,
            relief="flat",
            cursor="hand2")

        self.b2.place(
            x=673, y=445,
            width=104,
            height=16
        )

    def login(self):
        try:
            private_key = utility_functions.get_private_key(self.web3, self.entry0.get())
            account = self.web3.eth.account.from_key(private_key)

            utility_functions.create_qrcode(account.address)

            for widget in self.root.winfo_children():
                widget.destroy()

            self.to_page(
                page=AppPageManager,
                previous_page=None,
                eth_account=EthereumAccount(web3=self.web3, account=account),
                default_active_page=WalletPage
            )

        except ValueError:
            self.entry0.show_error(error=constants.ERRORS["ERROR_PASSWORD_WRONG"])

    def show_account_list(self):
        if utility_functions.toplevel_exist(toplevel=self.account_list_toplevel) is False:
            self.account_list_toplevel = AccountList(
                self.root,
                self.web3,
                bg="white"
            )
            self.account_list_toplevel.mainloop()
