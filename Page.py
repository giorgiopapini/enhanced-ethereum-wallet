from tkinter import *


class Page(Frame):

    def __init__(self, root=None, web3=None, **kwargs):
        Frame.__init__(self, root)
        self.root = root
        self.web3 = web3
        self.previous_page = kwargs.get("previous_page", None)
        self.frame = kwargs.get("frame", None)
        self.eth_account = kwargs.get("eth_account", None)

    def to_page(self, page=None, **kwargs):
        if page is not None:
            page(self.root, self.web3, **kwargs)

    @staticmethod
    def render_page(root=None, web3=None, page=None, **kwargs):
        if page is not None:
            page(root, web3, **kwargs)
