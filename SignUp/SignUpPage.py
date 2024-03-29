import os
import json
from tkinter import *
import constants
import utility_functions

from App.AppPageManager import AppPageManager
from App.ReusableComponents.TextField import TextField
from App.YourWallet.WalletPage import WalletPage
from Page import Page


class SignUpPage(Page):

    JSON_NFTS_PATH = "App/YourWallet/nfts.json"
    JSON_TOKENS_PATH = "App/YourWallet/tokens.json"

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.account = kwargs.get("eth_account", None)
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

        self.img1 = PhotoImage(file=f"SignUp/img1.png")
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
            x=16, y=106,
            width=38,
            height=38)

        self.img0 = PhotoImage(file=f"SignUp/img0.png")
        self.b0 = Button(
            image=self.img0,
            borderwidth=0,
            highlightthickness=0,
            command=self.sign_up,
            relief="flat",
            cursor="hand2"
        )

        self.b0.place(
            x=220, y=409,
            width=130,
            height=47)

        self.entry0_img = PhotoImage(file=f"SignUp/img_textBox0.png")
        self.entry0_bg = self.canvas.create_image(
            199.5, 283.5,
            image=self.entry0_img)

        self.entry0 = TextField(
            genesis_root=self.root,
            placeholder_text=self.eth_account.account.privateKey.hex(),
            state="disabled",
            bd=0,
            bg="#ffffff",
            disabledbackground="#ffffff",
            highlightthickness=0)

        self.entry0.place(
            x=73.5, y=269,
            width=252.0,
            height=31)

        self.entry1_img = PhotoImage(file=f"SignUp/img_textBox1.png")
        self.entry1_bg = self.canvas.create_image(
            199.5, 359.5,
            image=self.entry1_img)

        self.entry1 = TextField(
            bd=0,
            bg="#ffffff",
            highlightthickness=0)

        self.entry1.place(
            x=73.5, y=345,
            width=252.0,
            height=31)

        self.background_img = PhotoImage(file=f"SignUp/background.png")
        self.background = self.canvas.create_image(
            400.0, 186.0,
            image=self.background_img)

    def sign_up(self):
        if len(self.entry1.text) > constants.MIN_LENGTH_PASSWORD and self.entry1.get() != constants.ERRORS["ERROR_PASSWORD_LENGTH"]:
            for widget in self.root.winfo_children():
                widget.destroy()
            json_string = json.dumps(self.eth_account.account.encrypt(self.entry1.text))

            utility_functions.create_qrcode(self.eth_account.account.address)

            with open("encrypted_private_keys.json", "w+") as priv_key_json:
                priv_key_json.write(json.dumps({"keys": [json_string]}))

            if not self.account_exist():
                self.try_create_folder()

            self.to_page(
                page=AppPageManager,
                previous_page=None,
                eth_account=self.eth_account,
                default_active_page=WalletPage
            )
        else:
            self.entry1.show_error(error=constants.ERRORS["ERROR_PASSWORD_LENGTH"])

    def try_create_folder(self):
        try:
            self.create_account_folder()
        except FileNotFoundError:
            path = "App/Accounts"
            os.mkdir(path)
            self.create_account_folder()

    def create_account_folder(self):
        path = f"App/Accounts/{self.eth_account.account.address}/"
        os.mkdir(path)

        with open(f"{path}tokens.json", "w") as file:
            file.write("[]")

        with open(f"{path}nfts.json", "w") as file:
            file.write("{}")

        with open(f"{path}contacts.json", "w") as file:
            file.write("[]")

    def account_exist(self):
        if os.path.isdir(f"App/Accounts/{self.eth_account.account.address}/"):
            return True
        return False
