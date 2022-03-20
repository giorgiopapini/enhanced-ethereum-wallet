from tkinter import *

import constants
import utility_functions
from Homepage.Homepage import Homepage
from KeyImport.ImportPage import ImportPage
from Page import Page


class LoginPage(Page):
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
            relief="flat")

        self.b0.place(
            x=307, y=279,
            width=185,
            height=59)

        self.entry0_img = PhotoImage(file=f"Login/img_textBox0.png")
        self.entry0_bg = self.canvas.create_image(
            398.5, 228.5,
            image=self.entry0_img)

        self.entry0 = Entry(
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
            relief="flat")

        self.b1.place(
            x=307, y=334,
            width=185,
            height=33)

        self.entry0.bind("<Button>", utility_functions.clear_error_message)

    def render_import(self):
        ImportPage(self.root, self.web3, previous_page=LoginPage)

    def login(self):
        self.password = self.entry0.get()
        try:
            private_key = utility_functions.get_private_key(self.web3, self.password)
            account = self.web3.eth.account.from_key(private_key)
            print(private_key)
            print(f"address derived: {account.address}")

            utility_functions.create_qrcode(account.address)

            for widget in self.root.winfo_children():
                widget.destroy()

            self.to_page(
                page=Homepage,
                previous_page=None,
                account=account,  # passare la variabile di tipo Account, non solo l'address
            )

        except ValueError:
            utility_functions.error_message(self.entry0, constants.ERRORS["ERROR_PASSWORD_WRONG"])

