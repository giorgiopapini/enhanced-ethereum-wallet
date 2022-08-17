from tkinter import *
import json

import utility_functions
from App.Contacts.AddContact.AddContactPage import AddContactPage
from App.Contacts.ContactTile.ContactTile import ContactTile
from App.ReusableComponents.ListElement import ListElement
from App.ReusableComponents.ListWidget import ListWidget
from Page import Page


class ContactsPage(Page):

    BACKGROUND_IMG = "App/Contacts/background.png"
    SEARCH_BOX_IMAGE = "App/Contacts/search_box.png"
    CLEAN_BUTTON_IMAGE = "App/Contacts/clean_button.png"
    ADD_CONTACT_IMAGE = "App/Contacts/add_contact_img.png"
    CONTACTS_JSON_PATH = "App/Contacts/contacts.json"

    add_contact_page = None

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
            162.5, 72.5,
            image=self.background_img
        )

        self.search_box_image = PhotoImage(file=self.SEARCH_BOX_IMAGE)
        self.search_box_bg = self.canvas.create_image(
            186.5, 136.5,
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
            width=226.0,
            height=27
        )

        self.search_button_img = PhotoImage(file=self.CLEAN_BUTTON_IMAGE)
        self.search_button = Button(
            self.frame,
            image=self.search_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.clean_search_box,
            relief="flat",
            cursor="hand2"
        )

        self.search_button.place(
            x=323, y=117,
            width=39,
            height=39
        )

        self.new_contact_img = PhotoImage(file=f"{self.ADD_CONTACT_IMAGE}")
        self.new_contact_label = Button(
            self.frame,
            image=self.new_contact_img,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            command=self.show_add_contact_page,
            cursor="hand2"
        )

        self.new_contact_label.place(
            x=385, y=128
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

        self.search_box.bind("<Key>", self.filter_contacts)

    def show_add_contact_page(self):
        if utility_functions.toplevel_exist(toplevel=self.add_contact_page) is False:
            self.add_contact_page = AddContactPage(
                self.root,
                self.web3,
                callback=lambda: self.contacts_list.refresh_list(
                    parent_frame=self.contacts_list_frame,
                    elements=self.get_contacts()
                ),
                bg="white"
            )
            self.add_contact_page.mainloop()

    def get_contacts(self):
        try:
            with open(self.CONTACTS_JSON_PATH, "r") as file:
                raw_contacts = json.load(file)
                contacts = self.create_list_elements(raw_contacts=raw_contacts)
                return contacts
        except (FileNotFoundError, ValueError):
            return []

    def filter_contacts(self, event):
        query = utility_functions.format_query(event=event)
        with open(self.CONTACTS_JSON_PATH, "r") as file:
            raw_contacts = json.load(file)
            filtered_raw_contacts = []
            for contact in raw_contacts:
                if query.lower() in contact["name"].lower():
                    filtered_raw_contacts.append(contact)

        contacts = self.create_list_elements(raw_contacts=filtered_raw_contacts)
        self.contacts_list.refresh_list(parent_frame=self.contacts_list_frame, elements=contacts)

    def clean_search_box(self):
        self.search_box.delete(0, END)
        self.__init__(
            self.root,
            self.web3,
            frame=self.frame,
            eth_account=self.eth_account
        )

    def create_list_elements(self, raw_contacts):
        contact_list = []
        for contact in raw_contacts:
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
