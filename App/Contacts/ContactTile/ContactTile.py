from tkinter import *
import json


class ContactTile(Frame):

    CONTACT_BG_IMG = "App/Contacts/ContactTile/background.png"
    LETTER_BG_IMG = "App/Contacts/ContactTile/letter_bg_img.png"
    COPY_BTN_IMG = "App/Contacts/ContactTile/copy_img.png"
    DELETE_BTN_IMG = "App/Contacts/ContactTile/delete_img.png"
    CONTACTS_JSON_PATH = "App/Contacts/contacts.json"

    def __init__(self, genesis_root=None, username=None, address=None, **kwargs):
        super().__init__(**kwargs)
        self.genesis_root = genesis_root
        self.username = username
        self.address = address

        self.background_img = PhotoImage(file=self.CONTACT_BG_IMG)
        self.background = Label(
            self,
            image=self.background_img,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.background.pack()

        self.letter_bg_img = PhotoImage(file=self.LETTER_BG_IMG)
        self.letter_bg = Label(
            self,
            image=self.letter_bg_img,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.letter_bg.place(
            x=8.5, y=4
        )

        self.letter_frame = Frame(
            self,
            height=40,
            width=40,
        )
        self.letter_frame.place(
            x=20.5, y=12
        )

        self.letter = Label(
            self.letter_frame,
            text=f"{self.username[0]}",
            font=("Helvetica", 11, "bold"),
            bg="#ffffff"
        )
        self.letter.pack()

        self.username_label = Label(
            self,
            text=f"{self.username}",
            font=("OpenSansRoman", int(12)),
            bg="white"
        )
        self.username_label.place(
            x=52, y=5
        )

        self.address_label = Label(
            self,
            text=f"{self.address[0:30]}...",
            font=("Lucida Console", 9),
            bg="white"
        )
        self.address_label.place(
            x=52, y=28
        )

        self.copy_btn_img = PhotoImage(file=self.COPY_BTN_IMG)
        self.copy_btn = Button(
            self,
            image=self.copy_btn_img,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            command=self.copy_address,
            cursor="hand2"
        )
        self.copy_btn.place(
            x=295, y=10
        )

        self.delete_btn_img = PhotoImage(file=self.DELETE_BTN_IMG)
        self.delete_btn = Button(
            self,
            image=self.delete_btn_img,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            command=self.delete_contact,
            cursor="hand2"
        )
        self.delete_btn.place(
            x=328, y=9
        )

    def config(self, *args, **kwargs):
        # Avoid hardcoded code like this, config method should be rewritten
        self.username = kwargs.get("username", self.username)
        self.address = kwargs.get("address", self.address)
        self.genesis_root = kwargs.get("genesis_root", self.genesis_root)
        kwargs.pop("username")
        kwargs.pop("address")
        kwargs.pop("genesis_root")
        return super(ContactTile, self).configure(*args, **kwargs)

    def copy_address(self):
        if self.genesis_root is not None:
            self.genesis_root.clipboard_clear()
            self.genesis_root.clipboard_append(self.address)
            self.genesis_root.update()

    def delete_contact(self):
        with open(self.CONTACTS_JSON_PATH, "r+") as file:
            contacts = json.load(file)
            index = contacts.index({"name": self.username, "address": self.address})
            contacts.pop(index)

            file.seek(0)
            json.dump(contacts, file)
            file.truncate()

        self.destroy()
