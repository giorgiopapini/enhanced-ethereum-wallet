from tkinter import *
import constants
import utility_functions
from Page import Page


class AppPageManager(Page):

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.account = kwargs.get("account")

        # Page content change here

    def view_page(self, page):
        self.to_page(
            page=page
        )
