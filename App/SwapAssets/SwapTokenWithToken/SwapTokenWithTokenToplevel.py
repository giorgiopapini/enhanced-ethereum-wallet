from tkinter import *

import constants
import eth_generic_functions
import utility_functions
from App.ReusableComponents.TextField import TextField


class SwapTokenWithToken(Toplevel):

    BACKGROUND = "App/SwapAssets/SwapTokenWithToken/background.png"
    TEXTFIELD_ACTIVE = "App/SwapAssets/SwapETHWithToken/address_field_active.png"
    TEXTFIELD_DISABLED = "App/SwapAssets/SwapETHWithToken/address_field_disabled.png"
    TEXTFIELD_AMOUNT = "App/SwapAssets/SwapETHWithToken/amount_textbox_img.png"
    TEXTFIELD_AMOUNT_DISABLED = "App/SwapAssets/SwapETHWithToken/amount_textbox_disabled.png"
    APPROVE_BTN_IMG = "App/SwapAssets/SwapETHWithToken/approve_btn_img.png"
    SWAP_BTN_IMG = "App/SwapAssets/SwapETHWithToken/swap_btn_img.png"
    INTERCHANGE_BTN_IMG = "App/SwapAssets/SwapETHWithToken/interchange_fields_btn_img.png"

    def __init__(self, root, web3, eth_account=None, **kwargs):
        super().__init__(**kwargs)

        self.root = root
        self.web3 = web3
        self.eth_account = eth_account

        self.title("Swap ERC20 token with ERC20 token")
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
            193.0, 167.0,
            image=self.background_img
        )

        self.active_textfield_img = PhotoImage(file=self.TEXTFIELD_ACTIVE)
        self.disabled_textfield_img = PhotoImage(file=self.TEXTFIELD_DISABLED)
        self.disabled_textfield_amount_img = PhotoImage(file=self.TEXTFIELD_AMOUNT_DISABLED)

        self.textfield_from_img = self.canvas.create_image(
            178.5, 178.5,
            image=self.active_textfield_img
        )

        self.textfield_from = TextField(
            master=self,
            genesis_root=self.root,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
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
            bg="#ffffff",
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
            genesis_root=self.root,
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
            genesis_root=self.root,
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            callback_on_click=self.clean_min_amount
        )

        self.textfield_amount.place(
            x=44.5, y=314,
            width=123.0,
            height=27
        )

        self.min_amount_label = Label(
            self,
            text="",
            font=("OpenSansRoman-SemiBold", int(9)),
            fg="red",
            bg="white"
        )

        self.min_amount_label.place(
            x=26, y=349
        )

        self.approve_btn_img = PhotoImage(file=self.APPROVE_BTN_IMG)
        self.approve_btn = Button(
            self,
            image=self.approve_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.check_liquidity_in_pool,
            relief="flat",
            cursor="hand2"
        )

        self.approve_btn.place(
            x=247, y=312,
            width=117,
            height=39
        )

        self.approving_label = Label(
            self,
            text="Approving...",
            font=("OpenSansRoman-SemiBold", int(10.8)),
            fg="green",
            bg="white"
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

    def interchange_fields(self):
        to_textfield_text = self.textfield_to.get()
        from_textfield_text = self.textfield_from.get()

        self.textfield_from.override_text(text=to_textfield_text)
        self.textfield_to.override_text(text=from_textfield_text)

    def check_liquidity_in_pool(self):
        try:
            decimals = eth_generic_functions.get_token_decimals(token_address=self.textfield_from.get(), web3=self.web3)
            amount_int = int(float(self.textfield_amount.get()) * (10 ** decimals))

            liquidity = eth_generic_functions.uniswap_get_amounts_out(
                path=[self.textfield_from.get(), self.textfield_to.get()],
                amount_in=amount_int,
                web3=self.web3
            )

            if liquidity[1] == 0:
                self.textfield_amount.show_error(
                    error=utility_functions.format_string(
                        string=constants.ERRORS["ERROR_INSUFFICIENT_INPUT_AMOUNT"],
                        cut_to=21
                    )
                )

                min_amount = eth_generic_functions.uniswap_get_min_amount_in(
                    path=[self.textfield_from.get(), self.textfield_to.get()],
                    web3=self.web3
                )

                self.min_amount_label.config(
                    text=f"Min amount: {float(min_amount / (10 ** decimals))}"
                )
            else:
                self.check_token_amount_and_approve()
        except:
            self.textfield_from.show_error(error=constants.ERRORS["ERROR_NOT_ENOUGH_LIQUIDITY"])
            self.textfield_to.show_error(error=constants.ERRORS["ERROR_NOT_ENOUGH_LIQUIDITY"])
            self.textfield_amount.show_error(
                error=utility_functions.format_string(
                    string=constants.ERRORS["ERROR_NOT_ENOUGH_LIQUIDITY"],
                    cut_to=21
                )
            )

    def check_token_amount_and_approve(self):
        enough_erc20 = self.eth_account.user_has_enough_erc20(
            erc20_address=self.textfield_from.get(),
            amount=self.textfield_amount.get()
        )

        if enough_erc20 is True:
            self.freeze_fields()
            self.approve_transaction()
        else:
            self.textfield_from.show_error(error=constants.ERRORS["ERROR_NOT_ENOUGH_ERC20"])
            self.textfield_amount.show_error(
                error=utility_functions.format_string(
                    string=constants.ERRORS["ERROR_NOT_ENOUGH_ERC20"],
                    cut_to=21
                )
            )

    def approve_transaction(self):
        approved = self.eth_account.token_transfer_approved(  # check if transaction is already approved
            token_address=self.textfield_from.get(),
            user_address=self.eth_account.account.address,
            amount=self.textfield_amount.get()
        )

        if not approved:
            self.eth_account.approve_token(
                token_address=self.textfield_from.get(),
                amount=self.textfield_amount.get()
            )

            self.approve_btn.place_forget()
            self.show_approving_label()

            self.check_allowance()
        else:
            self.approve_btn.place_forget()
            self.show_swap_btn()

    def check_allowance(self):
        approved = self.eth_account.token_transfer_approved(
            token_address=self.textfield_from.get(),
            user_address=self.eth_account.account.address,
            amount=self.textfield_amount.get()
        )

        if approved is True:
            self.show_swap_btn()
        else:
            self.root.after(2000, self.check_allowance)

    def show_approving_label(self):
        self.approving_label.place(
            x=255, y=312,
        )

    def show_swap_btn(self):
        self.swap_btn.place(
            x=255, y=312,
            width=102,
            height=39
        )

    def swap_assets(self):
        self.eth_account.swap_token_for_token(
            from_token_address=self.textfield_from.get(),
            to_token_address=self.textfield_to.get(),
            amount=self.textfield_amount.get()
        )
        self.destroy()

    def freeze_fields(self):
        self.interchange_btn["state"] = "disabled"

        self.canvas.itemconfig(self.textfield_from_img, image=self.disabled_textfield_img)
        self.textfield_from.disable()
        self.textfield_from.override_text(text=self.textfield_from.get())

        self.canvas.itemconfig(self.textfield_to_img, image=self.disabled_textfield_img)
        self.textfield_to.disable()
        self.textfield_to.override_text(text=self.textfield_to.get())

        self.canvas.itemconfig(self.textfield_amount_img, image=self.disabled_textfield_amount_img)
        self.textfield_amount.disable()
        self.textfield_amount.override_text(text=self.textfield_amount.get())

    def clean_min_amount(self):
        self.min_amount_label.config(text="")
