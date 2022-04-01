from tkinter import *

from EthereumAccount import EthereumAccount
from Page import Page
from SignUp.SignUpPage import SignUpPage
from KeyImport.ImportPage import ImportPage


class WelcomePage(Page):
    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.account = ""

        self.canvas = Canvas(
            root,
            bg="#ffffff",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=f"Welcome/background.png")
        self.background = self.canvas.create_image(
            524.5, 203.0,
            image=self.background_img)

        self.img0 = PhotoImage(file=f"Welcome/img0.png")
        self.b0 = Button(
            image=self.img0,
            borderwidth=0,
            highlightthickness=0,
            command=self.render_sign_up,
            relief="flat")

        self.b0.place(
            x=306, y=263,
            width=185,
            height=55)

        self.img1 = PhotoImage(file=f"Welcome/img1.png")
        self.b1 = Button(
            image=self.img1,
            borderwidth=0,
            highlightthickness=0,
            command=self.render_import,
            relief="flat")

        self.b1.place(
            x=307, y=318,
            width=185,
            height=33)

    def render_import(self):
        self.to_page(
            page=ImportPage,
            previous_page=WelcomePage,
        )

    def render_sign_up(self):
        self.account = self.web3.eth.account.create()
        self.to_page(
            page=SignUpPage,
            previous_page=WelcomePage,
            eth_account=EthereumAccount(web3=self.web3, account=self.account)
        )
