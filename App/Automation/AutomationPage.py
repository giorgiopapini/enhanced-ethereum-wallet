from tkinter import *
from Page import Page


class AutomationPage(Page):

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.automation = Label(
            self.frame,
            text="Sample Automation"
        )

        self.automation.place(
            x=123, y=111
        )

