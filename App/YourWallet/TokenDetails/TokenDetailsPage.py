from tkinter import *

import eth_generic_functions
import utility_functions
from App.ReusableComponents.ListElement import ListElement
from App.ReusableComponents.ListWidget import ListWidget
from App.YourWallet.TokenDetails.BuyPage.BuyPage import BuyPage
from App.YourWallet.TokenDetails.SendPage.SendPage import SendPage
from App.YourWallet.TokenDetails.TransactionTile.TransactionTile import TransactionTile
from Page import Page


class TokenDetailsPage(Page):

    BACKGROUND_IMG = "App/YourWallet/TokenDetails/background.png"
    SEND_BUTTON_IMG = "App/YourWallet/TokenDetails/send_button_img.png"
    BUY_BUTTON_IMG = "App/YourWallet/TokenDetails/buy_button_img.png"
    BACK_ARROW_IMG = "KeyImport/img1.png"

    buy_page = None
    send_page = None

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.token = kwargs.get("token", None)
        self.token_amount = kwargs.get("token_amount", 0)

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
            167.5, 107.5,
            image=self.background_img
        )

        self.token_amount_label = Label(
            self.frame,
            text=f"{self.token_amount}"[0:8],
            font=("Helvetica", 20, "bold"),
            bg="white"
        )

        self.token_amount_label.place(
            x=296, y=38,
        )

        self.send_button_img = PhotoImage(file=self.SEND_BUTTON_IMG)
        self.send_button = Button(
            self.frame,
            image=self.send_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.show_send_page,
            relief="flat",
            cursor="hand2"
        )

        self.send_button.place(
            x=60, y=104,
            width=170,
            height=46
        )

        self.buy_button_img = PhotoImage(file=self.BUY_BUTTON_IMG)
        self.buy_button = Button(
            self.frame,
            image=self.buy_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.show_buy_page,
            relief="flat",
            cursor="hand2"
        )

        self.buy_button.place(
            x=294, y=104,
            width=170,
            height=46
        )

        self.transaction_frame = Frame(self.frame, bg="white")
        self.transaction_frame.place(
            x=74, y=205,
            width=420,
            height=197
        )

        self.transaction_list = ListWidget(
            parent=self.transaction_frame,
            space_between=5,
            elements=self.create_transactions_list()
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

    def create_transactions_list(self):
        transactions = []
        if self.token is None:
            raw_transactions = eth_generic_functions.get_eth_transactions(user_address=self.eth_account.account.address)
        else:
            raw_transactions = eth_generic_functions.get_token_transactions(
                token_address=self.token["address"],
                user_address=self.eth_account.account.address,
            )
        for transaction in raw_transactions:
            if transaction['value'] != '0':
                transactions.append(
                    ListElement(
                        widget=TransactionTile,
                        genesis_root=self.root,
                        web3=self.web3,
                        transaction_json=transaction,
                        eth_account=self.eth_account,
                        token=self.token,
                        height=50
                    )
                )
        return transactions

    def show_buy_page(self):
        if utility_functions.toplevel_exist(toplevel=self.buy_page) is False:
            self.buy_page = BuyPage(self.root, self.web3, bg="white")
            self.buy_page.mainloop()

    def show_send_page(self):
        if utility_functions.toplevel_exist(toplevel=self.send_page) is False:
            self.send_page = SendPage(
                self.root,
                self.web3,
                token=self.token,
                eth_account=self.eth_account,
                bg="white",
            )
            self.send_page.mainloop()
