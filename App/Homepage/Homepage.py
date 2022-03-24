from tkinter import *

from App.AppPageManager import AppPageManager

# IMPORTANTE!!! --> Capire come gestire il rendering delle pagine

class Homepage(AppPageManager):

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)
