from tkinter import *


class ContactTile(Frame):

    CONTACT_BG_IMG = "App/Contacts/ContactTile/background.png"

    def __init__(self, name=None, address=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.address = address

        self.background_img = PhotoImage(file=self.CONTACT_BG_IMG)
        self.background = Label(
            self,
            image=self.background_img

        )
        self.background.pack()

        # add copy and delete buttons --> add labels that show name and address

    def config(self, *args, **kwargs):
        self.name = kwargs.get('name', self.name)
        self.address = kwargs.get('address', self.address)
        kwargs.pop("name")
        kwargs.pop("address")
        return super(ContactTile, self).configure(*args, **kwargs)

