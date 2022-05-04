from tkinter import *
from Page import Page


class TokenDetailsPage(Page):

    BACKGROUND_IMG = "App/YourWallet/TokenDetails/background.png"
    SEND_BUTTON_IMG = "App/YourWallet/TokenDetails/send_button_img.png"
    BUY_BUTTON_IMG = "App/YourWallet/TokenDetails/buy_button_img.png"
    BACK_ARROW_IMG = "KeyImport/img1.png"

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
            167.5, 120.0,
            image=self.background_img
        )

        self.send_button_img = PhotoImage(file=self.SEND_BUTTON_IMG)
        self.send_button = Button(
            self.frame,
            image=self.send_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat"
        )

        self.send_button.place(
            x=60, y=108,
            width=170,
            height=46
        )

        self.buy_button_img = PhotoImage(file=self.BUY_BUTTON_IMG)
        self.buy_button = Button(
            self.frame,
            image=self.buy_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat"
        )

        self.buy_button.place(
            x=294, y=108,
            width=170,
            height=46
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
            x=60, y=350
        )

    def btn_clicked(self):
        pass
