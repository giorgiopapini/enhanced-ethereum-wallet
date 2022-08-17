from tkinter import *
import json

import constants
import utility_functions
import eth_generic_functions
from App.ReusableComponents.TextField import TextField
from Page import Page


class ImportTokenPage(Page):

    BACKGROUND_IMG = "App/YourWallet/ImportToken/background.png"
    TEXT_BOX_IMAGE = "App/YourWallet/ImportToken/textbox_img.png"
    DISABLED_TEXT_BOX_IMAGE = "App/YourWallet/ImportToken/disabled_textbox_img.png"
    BACK_ARROW_IMG = "KeyImport/img1.png"
    IMPORT_BUTTON_IMAGE = "App/YourWallet/ImportToken/import_button_img.png"
    TOKENS_JSON_PATH = "App/YourWallet/tokens.json"

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.canvas = Canvas(
            self.frame,
            bg="white",
            height=466,
            width=522,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=self.BACKGROUND_IMG)
        self.background = self.canvas.create_image(
            159.0, 165.5,
            image=self.background_img
        )

        self.contract_addr_field_img = PhotoImage(file=self.TEXT_BOX_IMAGE)
        self.contract_addr_field_bg = self.canvas.create_image(
            217.0, 154.5,
            image=self.contract_addr_field_img
        )

        self.contract_addr_field = TextField(
            master=self.frame,
            genesis_root=self.root,
            callback=self.get_token_data,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.contract_addr_field.place(
            x=73.5, y=142,
            width=287.0,
            height=27
        )

        self.token_symbol_field_img = PhotoImage(file=self.DISABLED_TEXT_BOX_IMAGE)
        self.token_symbol_field_bg = self.canvas.create_image(
            217.0, 237.5,
            image=self.token_symbol_field_img
        )

        self.token_symbol_field = TextField(
            master=self.frame,
            genesis_root=self.root,
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            state='disabled'
        )

        self.token_symbol_field.place(
            x=73.5, y=225,
            width=287.0,
            height=27
        )

        self.decimals_field_img = PhotoImage(file=self.DISABLED_TEXT_BOX_IMAGE)
        self.decimals_field_bg = self.canvas.create_image(
            217.0, 320.5,
            image=self.decimals_field_img
        )

        self.decimals_field = TextField(
            master=self.frame,
            genesis_root=self.root,
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            state='disabled'
        )

        self.decimals_field.place(
            x=73.5, y=308,
            width=287.0,
            height=27
        )

        self.import_button_img = PhotoImage(file=self.IMPORT_BUTTON_IMAGE)
        self.import_button = Button(
            self.frame,
            image=self.import_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.import_token,
            relief="flat",
            cursor="hand2"
        )

        self.import_button.place(
            x=290, y=382,
            width=169,
            height=59
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
            x=60, y=383
        )

    def get_token_data(self):
        try:
            token_symbol = eth_generic_functions.get_token_symbol(token_address=self.contract_addr_field.text, web3=self.web3)
            token_decimals = eth_generic_functions.get_token_decimals(token_address=self.contract_addr_field.text, web3=self.web3)

            self.clear_fields()
            self.update_fields(token_symbol=token_symbol, token_decimals=token_decimals)
        except:
            self.show_errors()

    def clear_fields(self):
        self.token_symbol_field.clear_field()
        self.decimals_field.clear_field()

    def update_fields(self, token_symbol=None, token_decimals=None):
        self.token_symbol_field.override_text(text=token_symbol)
        self.decimals_field.override_text(text=token_decimals)

    def show_errors(self):
        self.token_symbol_field.show_error(error=constants.ERRORS["ERROR_ERC20_NOT_FOUND"])
        self.decimals_field.show_error(error=constants.ERRORS["ERROR_ERC20_NOT_FOUND"])

    def import_token(self):
        with open(self.TOKENS_JSON_PATH, "r+") as file:
            tokens = json.load(file)
            token_already_saved = utility_functions.is_token_saved(
                tokens=tokens,
                token_address=self.contract_addr_field.get()
            )
            fields_valid = utility_functions.check_fields_validity(
                fields=[
                    self.token_symbol_field,
                    self.decimals_field
                ],
                error=constants.ERRORS["ERROR_ERC20_NOT_FOUND"],
            )

            if fields_valid is True and token_already_saved is False:
                tokens.append(
                    {
                        "symbol": self.token_symbol_field.get(),
                        "address": self.contract_addr_field.get(),
                        "decimals": int(self.decimals_field.get()),
                    }
                )
                tokens.sort(key=lambda x: x["symbol"].lower())

                file.seek(0)
                json.dump(tokens, file)
                file.truncate()

                self.to_page(
                    page=self.previous_page,
                    previous_page=None,
                    frame=self.frame,
                    eth_account=self.eth_account
                )
            else:
                self.contract_addr_field.show_error(error=constants.ERRORS["ERROR_ERC20_NOT_VALID"])
