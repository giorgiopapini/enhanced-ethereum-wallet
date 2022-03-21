from tkinter import *
import constants
import utility_functions
from Page import Page


class AppPageManager(Page):

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        # Page content change here