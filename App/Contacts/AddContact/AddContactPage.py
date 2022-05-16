from tkinter import *

import constants
import utility_functions
from App.ReusableComponents.TextField import TextField
from Page import Page
import json


class AddContactPage(Page):

    BACKGROUND_IMG = "App/Contacts/AddContact/background.png"
    INPUT_FIELD_IMG = "App/Contacts/AddContact/img_textBox.png"
    BACK_ARROW_IMG = "KeyImport/img1.png"
    CREATE_CONTACT_IMG = "App/Contacts/AddContact/create_btn_img.png"
    CONTACTS_JSON_PATH = "App/Contacts/contacts.json"

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
            189.0, 132.5,
            image=self.background_img
        )

        self.username_field_img = PhotoImage(file=self.INPUT_FIELD_IMG)
        self.username_field_bg = self.canvas.create_image(
            217.0, 159.5,
            image=self.username_field_img
        )

        self.username_field = TextField(
            master=self.frame,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.username_field.place(
            x=73.5, y=147,
            width=287.0,
            height=27
        )

        self.address_field_img = PhotoImage(file=self.INPUT_FIELD_IMG)
        self.address_field_bg = self.canvas.create_image(
            217.0, 254.5,
            image=self.address_field_img
        )

        self.address_field = TextField(
            master=self.frame,
            genesis_root=self.root,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.address_field.place(
            x=73.5, y=242,
            width=287.0,
            height=27
        )

        self.back_button_img = PhotoImage(file=self.BACK_ARROW_IMG)
        self.back_button = Button(
            self.frame,
            image=self.back_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.to_page(
                page=self.previous_page,
                frame=self.frame
            ),
            relief="flat"
        )
        self.back_button.place(
            x=60, y=350
        )

        self.add_button_img = PhotoImage(file=self.CREATE_CONTACT_IMG)
        self.add_button = Button(
            self.frame,
            image=self.add_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.add_contact,
            relief="flat"
        )

        self.add_button.place(
            x=246, y=350,
            width=229,
            height=59
        )

    def add_contact(self):
        username = self.username_field.text
        address = self.address_field.text

        valid = utility_functions.check_fields_validity(
            fields=[self.username_field, self.address_field],
            error=constants.ERRORS["ERROR_EMPTY_FIELD"]
        )

        valid = utility_functions.check_address_field_validity(
            address_field=self.address_field,
            error=constants.ERRORS["ERROR_ADDRESS_NOT_VALID"],
            web3=self.web3
        )

        if valid is True:
            with open(self.CONTACTS_JSON_PATH, "r+") as file:
                contacts = json.load(file)
                contacts.append({"name": username.lower().capitalize(), "address": address})
                contacts.sort(key=lambda x: x["name"])

                file.seek(0)
                json.dump(contacts, file)
                file.truncate()

            self.to_page(
                page=self.previous_page,
                frame=self.frame
            )

