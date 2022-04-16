from tkinter import *
from Page import Page


class ContactsPage(Page):

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

        self.background_img = PhotoImage(file=f"App/Contacts/background.png")
        self.background = self.canvas.create_image(
            162.5, 72.5,
            image=self.background_img)

        self.search_box_image = PhotoImage(file=f"App/Contacts/img_textBox0.png")
        self.search_box_bg = self.canvas.create_image(
            201.5, 136.5,
            image=self.search_box_image)

        self.search_box = Entry(
            self.frame,
            bd=0,
            bg="#ffffff",
            highlightthickness=0)

        self.search_box.place(
            x=73.5, y=124,
            width=256.0,
            height=27)

