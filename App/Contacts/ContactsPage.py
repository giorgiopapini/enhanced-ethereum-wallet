from tkinter import *

from App.Contacts.ContactTile.ContactTile import ContactTile
from App.ReusableComponents.ListElement import ListElement
from App.ReusableComponents.ListWidget import ListWidget
from Page import Page


class ContactsPage(Page):

    BACKGROUND_IMG = "App/Contacts/background.png"
    SEARCH_BOX_IMAGE = "App/Contacts/search_box.png"

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        # This canvas will be created for every page, should I declare a general canvas inside AppPageManager
        # and pass it as a **kwarg to every page?

        self.canvas = Canvas(
            self.frame,
            bg="#ffffff",
            height=466,
            width=522,
            bd=0,
            highlightthickness=0,
            relief="ridge")
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

        self.contacts_list_frame = Frame(self.frame)
        self.contacts_list_frame.place(
            x=59, y=177,
            width=435,
            height=267
        )
        self.contacts_list = ListWidget(
            parent=self.contacts_list_frame,
            space_between=1,
            elements=[
                ListElement(
                    widget=ContactTile,
                    name="Giorgio",
                    address="0x0er303403904930",
                    height=50,
                    width=435  # This value should not be hardcoded. It should equals to parent frame width
                )
            ],
        )

