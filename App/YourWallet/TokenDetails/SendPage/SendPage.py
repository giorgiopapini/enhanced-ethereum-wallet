from tkinter import *

import constants
import utility_functions
from App.ReusableComponents.TextField import TextField


class SendPage(Toplevel):

    BACKGROUND = "App/YourWallet/TokenDetails/SendPage/background.png"
    AMOUNT_FIELD_IMAGE = "App/YourWallet/TokenDetails/SendPage/amount_field.png"
    SENDER_FIELD_IMAGE = "App/YourWallet/TokenDetails/SendPage/sender_field_image.png"
    RECEIVER_FIELD_IMAGE = "App/YourWallet/TokenDetails/SendPage/receiver_field_image.png"
    SEND_BUTTON_IMG = "App/YourWallet/TokenDetails/SendPage/send_button_image.png"

    def __init__(self, root, web3, token=None, eth_account=None, **kwargs):
        super().__init__(**kwargs)

        self.root = root
        self.web3 = web3
        self.token = token
        self.eth_account = eth_account

        self.token_symbol = self.token["symbol"] if self.token is not None else "ETH"

        self.title(f"Send {self.token_symbol} Page")
        self.geometry("380x380")
        self.resizable(False, False)

        self.canvas = Canvas(
            self,
            bg="#ffffff",
            height=380,
            width=380,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=self.BACKGROUND)
        self.background = self.canvas.create_image(
            179.0, 200.5,
            image=self.background_img
        )

        self.send_label = Label(
            self,
            text=f"Send {utility_functions.format_string(string=self.token_symbol, cut_to=10)}",
            font=("OpenSansRoman-SemiBold", 30),
            bg="white"
        )
        self.send_label.place(
            x=23, y=24
        )

        self.description_label = Label(
            self,
            text=f"Send {'ETH' if self.token is None else 'token'} to an Ethereum address",
            font=("OpenSansRoman-Regular", 14),
            bg="white"
        )
        self.description_label.place(
            x=23, y=70
        )

        self.sender_field_img = PhotoImage(file=self.SENDER_FIELD_IMAGE)
        self.sender_field_bg = self.canvas.create_image(
            175, 178.5,
            image=self.sender_field_img
        )

        self.sender_field = TextField(
            master=self,
            genesis_root=self.root,
            state="disabled",
            placeholder_text=self.eth_account.account.address,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.sender_field.place(
            x=42, y=166,
            width=268.0,
            height=27
        )

        self.receiver_field_img = PhotoImage(file=self.RECEIVER_FIELD_IMAGE)
        self.receiver_field_bg = self.canvas.create_image(
            175, 252.5,
            image=self.receiver_field_img
        )

        self.receiver_field = TextField(
            master=self,
            genesis_root=self.root,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.receiver_field.place(
            x=42, y=240,
            width=268.0,
            height=27
        )

        self.amount_field_img = PhotoImage(file=self.AMOUNT_FIELD_IMAGE)
        self.amount_field_bg = self.canvas.create_image(
            80.5, 326.5,
            image=self.amount_field_img
        )

        self.amount_field = TextField(
            master=self,
            genesis_root=self.root,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.amount_field.place(
            x=42, y=314,
            width=77.0,
            height=27
        )

        self.token_symbol_label = Label(
            self,
            text=utility_functions.format_string(string=self.token_symbol, cut_to=9),
            font=("OpenSansRoman-Regular", 12),
            bg="white"
        )
        self.token_symbol_label.place(
            x=140.5, y=316
        )

        self.send_button_image = PhotoImage(file=self.SEND_BUTTON_IMG)
        self.send_button = Button(
            self,
            image=self.send_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.send_amount,
            relief="flat"
        )

        self.send_button.place(
            x=255, y=312,
            width=102,
            height=39
        )

    def send_amount(self):
        try:
            if self.token is None:
                self.eth_account.send_ether(
                    receiver_addr=self.receiver_field.text,
                    amount_in_eth=self.amount_field.text
                )
            else:
                self.eth_account.send_erc20_token(
                    erc20_address=self.token["address"],
                    receiver_addr=self.receiver_field.text,
                    amount=self.amount_field.text
                )
            self.destroy()
            self.update()
        except:
            self.receiver_field.show_error(error=constants.ERRORS["ERROR_SENDING_ERC20"])
            self.amount_field.show_error(
                error=utility_functions.format_string(string=constants.ERRORS["ERROR_SENDING_ERC20"], cut_to=15)
            )
