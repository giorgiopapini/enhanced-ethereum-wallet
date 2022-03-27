from tkinter import *
from Page import Page


class ContactsPage(Page):

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.contacts = Label(
            self.frame,
            text="Sample Contacts"
        )

        self.contacts.place(
            x=170, y=104
        )
