from tkinter import *

import constants
import utility_functions
from App.ReusableComponents.TextField import TextField
import json


class AddContactPage(Toplevel):

    BACKGROUND_IMG = "App/Contacts/AddContact/background.png"
    INPUT_FIELD_IMG = "App/Contacts/AddContact/field_img.png"
    CREATE_CONTACT_IMG = "App/Contacts/AddContact/create_contact_img.png"

    def __init__(self, root, web3, callback=None, address=None, **kwargs):
        super().__init__(**kwargs)

        self.root = root
        self.web3 = web3
        self.callback = callback
        self.address = address

        self.title("Add contact")
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

        self.background_img = PhotoImage(file=self.BACKGROUND_IMG)
        self.background = self.canvas.create_image(
            183.0, 167.0,
            image=self.background_img
        )

        self.new_contact_label = Label(
            self,
            text="New contact",
            font=("OpenSansRoman-SemiBold", 30),
            bg="white"
        )
        self.new_contact_label.place(
            x=23, y=24
        )

        self.description_label = Label(
            self,
            text=f"Add a new contact to your address book",
            font=("OpenSansRoman-Regular", int(13.7)),
            bg="white"
        )
        self.description_label.place(
            x=26, y=73
        )

        self.username_field_img = PhotoImage(file=self.INPUT_FIELD_IMG)
        self.username_field_bg = self.canvas.create_image(
            178.5, 259.5,
            image=self.username_field_img
        )

        self.username_field = TextField(
            master=self,
            genesis_root=self.root,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.username_field.place(
            x=44.5, y=170,
            width=268.0,
            height=27

        )

        self.address_field_img = PhotoImage(file=self.INPUT_FIELD_IMG)
        self.address_field_bg = self.canvas.create_image(
            178.5, 182.5,
            image=self.address_field_img
        )

        self.address_field = TextField(
            master=self,
            genesis_root=self.root,
            bd=0,
            bg="#ffffff",
            highlightthickness=0)

        self.address_field.place(
            x=44.5, y=247,
            width=268.0,
            height=27
        )

        self.add_button_img = PhotoImage(file=self.CREATE_CONTACT_IMG)
        self.add_button = Button(
            self,
            image=self.add_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.add_contact,
            relief="flat",
            cursor="hand2"
        )

        self.add_button.place(
            x=179, y=311,
            width=180,
            height=42
        )

    def add_contact(self):
        username = self.username_field.get()
        address = self.address_field.get()

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
            path = f"App/Accounts/{self.address}/contacts.json"
            with open(path, "r+") as file:
                contacts = json.load(file)
                contacts.append({"name": username.lower().capitalize(), "address": address})
                contacts.sort(key=lambda x: x["name"])

                file.seek(0)
                json.dump(contacts, file)
                file.truncate()

                self.callback()
                self.destroy()
