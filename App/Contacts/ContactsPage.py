from tkinter import *
import json

from App.Contacts.AddContact.AddContactPage import AddContactPage
from App.Contacts.ContactTile.ContactTile import ContactTile
from App.ReusableComponents.ListElement import ListElement
from App.ReusableComponents.ListWidget import ListWidget
from Page import Page


class ContactsPage(Page):

    BACKGROUND_IMG = "App/Contacts/background.png"
    SEARCH_BOX_IMAGE = "App/Contacts/search_box.png"
    ADD_CONTACT_IMAGE = "App/Contacts/add_contact_img.png"
    CONTACTS_JSON_PATH = "App/Contacts/contacts.json"

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        # This canvas will be created for every page, should I declare a general canvas inside AppPageManager
        # and pass it as a **kwarg to every page?

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
            162.5, 72.5,
            image=self.background_img
        )

        self.search_box_image = PhotoImage(file=self.SEARCH_BOX_IMAGE)
        self.search_box_bg = self.canvas.create_image(
            201.5, 136.5,
            image=self.search_box_image
        )

        self.search_box = Entry(
            self.frame,
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.search_box.place(
            x=73.5, y=124,
            width=256.0,
            height=27
        )

        self.new_contact_img = PhotoImage(file=f"{self.ADD_CONTACT_IMAGE}")
        self.new_contact_label = Button(
            self.frame,
            image=self.new_contact_img,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            command=lambda: self.to_page(
                page=AddContactPage,
                frame=self.frame,
                previous_page=ContactsPage
            )
        )

        self.new_contact_label.place(
            x=380, y=128
        )

        self.contacts_list_frame = Frame(self.frame, bg="white")
        self.contacts_list_frame.place(
            x=59, y=179,
            width=435,
            height=267
        )
        self.contacts_list = ListWidget(
            parent=self.contacts_list_frame,
            space_between=1,
            elements=self.get_contacts()
        )

    def get_contacts(self):
        contact_list = []
        try:
            with open(self.CONTACTS_JSON_PATH, "r") as file:
                contacts = json.load(file)
                for contact in contacts:
                    contact_list.append(
                        ListElement(
                            widget=ContactTile,
                            genesis_root=self.root,
                            username=contact["name"],
                            address=contact["address"],
                            height=50,
                        )
                    )
                return contact_list
        except (FileNotFoundError, ValueError):
            return []
