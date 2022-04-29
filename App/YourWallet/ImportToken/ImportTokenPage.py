from tkinter import *
import json

from Page import Page


class ImportTokenPage(Page):

    BACKGROUND_IMG = "App/YourWallet/ImportToken/background.png"
    TEXT_BOX_IMAGE = "App/Contacts/AddContact/img_textBox.png"
    BACK_ARROW_IMG = "KeyImport/img1.png"
    IMPORT_BUTTON_IMAGE = "App/YourWallet/ImportToken/import_button_img.png"

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

        self.contract_addr_field = Entry(
            self.frame,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.contract_addr_field.place(
            x=73.5, y=142,
            width=287.0,
            height=27
        )

        self.token_symbol_field_img = PhotoImage(file=self.TEXT_BOX_IMAGE)
        self.token_symbol_field_bg = self.canvas.create_image(
            217.0, 237.5,
            image=self.token_symbol_field_img
        )

        self.token_symbol_field = Entry(
            self.frame,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.token_symbol_field.place(
            x=73.5, y=225,
            width=287.0,
            height=27
        )

        self.decimals_field_img = PhotoImage(file=self.TEXT_BOX_IMAGE)
        self.decimals_field_bg = self.canvas.create_image(
            217.0, 320.5,
            image=self.decimals_field_img
        )

        self.decimals_field = Entry(
            self.frame,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
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
            relief="flat"
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
            relief="flat"
        )
        self.back_button.place(
            x=60, y=383
        )

        self.contract_addr_field.bind("<Key>", self.check_addr)
        # entry bind with <Key> (any key) --> Check the content of address field --> If address field contains an address
        # ask the token symbol and decimal to the blockchain

    def check_addr(self, event):
        print("checking addr")

    def import_token(self):
        # Check if token alredy in list
        # Read json file and save as list
        # Append to list the imported token
        # Write json file
        # Redirect to YourWallet page
        pass
