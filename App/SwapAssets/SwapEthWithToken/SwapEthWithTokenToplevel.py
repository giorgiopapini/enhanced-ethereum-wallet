from tkinter import *

import constants
import utility_functions
from App.ReusableComponents.TextField import TextField


class SwapETHWithToken(Toplevel):

    BACKGROUND = "App/SwapAssets/SwapETHWithToken/background.png"
    TEXTFIELD_ACTIVE = "App/SwapAssets/SwapETHWithToken/address_field_active.png"
    TEXTFIELD_DISABLED = "App/SwapAssets/SwapETHWithToken/address_field_disabled.png"
    TEXTFIELD_AMOUNT = "App/SwapAssets/SwapETHWithToken/amount_textbox_img.png"
    SWAP_BTN_IMG = "App/SwapAssets/SwapETHWithToken/swap_btn_img.png"
    INTERCHANGE_BTN_IMG = "App/SwapAssets/SwapETHWithToken/interchange_fields_btn_img.png"

    swap_eth_for_token = True

    def __init__(self, root, web3, eth_account=None, **kwargs):
        super().__init__(**kwargs)

        self.root = root
        self.web3 = web3
        self.eth_account = eth_account

        self.title("Swap ETH with ERC20 token")
        self.geometry("400x380")
        self.resizable(False, False)

        self.canvas = Canvas(
            self,
            bg="#ffffff",
            height=380,
            width=400,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=self.BACKGROUND)
        self.background = self.canvas.create_image(
            194.0, 167.0,
            image=self.background_img
        )

        self.active_textfield_img = PhotoImage(file=self.TEXTFIELD_ACTIVE)
        self.disabled_textfield_img = PhotoImage(file=self.TEXTFIELD_DISABLED)

        self.textfield_from_img = self.canvas.create_image(
            178.5, 178.5,
            image=self.disabled_textfield_img
        )

        self.textfield_from = TextField(
            master=self,
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            placeholder_text="ETH",
            state="disabled"
        )

        self.textfield_from.place(
            x=44.5, y=166,
            width=268.0,
            height=27
        )

        self.interchange_btn_img = PhotoImage(file=self.INTERCHANGE_BTN_IMG)
        self.interchange_btn = Button(
            self,
            image=self.interchange_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.interchange_fields,
            relief="flat",
            cursor="hand2"
        )

        self.interchange_btn.place(
            x=338, y=196,
            width=40,
            height=39
        )

        self.textfield_to_img = self.canvas.create_image(
            178.5, 252.5,
            image=self.active_textfield_img
        )

        self.textfield_to = TextField(
            master=self,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.textfield_to.place(
            x=44.5, y=240,
            width=268.0,
            height=27
        )

        self.textfield_amount_img_bg = PhotoImage(file=self.TEXTFIELD_AMOUNT)
        self.textfield_amount_img = self.canvas.create_image(
            106.0, 326.5,
            image=self.textfield_amount_img_bg
        )

        self.textfield_amount = TextField(
            master=self,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.textfield_amount.place(
            x=44.5, y=314,
            width=123.0,
            height=27
        )

        self.swap_btn_img = PhotoImage(file=self.SWAP_BTN_IMG)
        self.swap_btn = Button(
            self,
            image=self.swap_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.swap_assets,
            relief="flat",
            cursor="hand2"
        )

        self.swap_btn.place(
            x=255, y=312,
            width=102,
            height=39
        )

    def swap_assets(self):
        if self.swap_eth_for_token is True:
            self.eth_to_token()
        else:
            self.token_to_eth()

    def eth_to_token(self):
        try:
            self.eth_account.swap_eth_for_token(
                amount_int_eth=self.textfield_amount.get(),
                token_address=self.textfield_to.get()
            )
        except:
            self.textfield_amount.show_error(
                error=utility_functions.format_string(
                    string=constants.ERRORS["ERROR_SWAP_FAILED"],
                    cut_to=21
                )
            )
            self.textfield_to.show_error(error=constants.ERRORS["ERROR_SWAP_FAILED"])

    def token_to_eth(self):
        pass

    def interchange_fields(self):
        if self.swap_eth_for_token is True:
            self.set_fields_eth_to_token()
        else:
            self.set_fields_token_to_eth()

    def set_fields_eth_to_token(self):
        self.canvas.itemconfig(self.textfield_from_img, image=self.active_textfield_img)
        self.textfield_from.enable()
        self.textfield_from.override_text(text=self.textfield_to.get())

        self.canvas.itemconfig(self.textfield_to_img, image=self.disabled_textfield_img)
        self.textfield_to.disable()
        self.textfield_to.override_text(text="ETH")

        self.swap_eth_for_token = False

    def set_fields_token_to_eth(self):
        self.canvas.itemconfig(self.textfield_to_img, image=self.active_textfield_img)
        self.textfield_to.enable()
        self.textfield_to.override_text(text=self.textfield_from.get())

        self.canvas.itemconfig(self.textfield_from_img, image=self.disabled_textfield_img)
        self.textfield_from.disable()
        self.textfield_from.override_text(text="ETH")

        self.swap_eth_for_token = True
