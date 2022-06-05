from tkinter import *


class TransactionDetails(Toplevel):

    def __init__(self, root, web3, transaction_json=None, **kwargs):
        super().__init__(**kwargs)

        self.root = root
        self.web3 = web3
        self.transaction_json = transaction_json

        self.title(f"Transaction #{transaction_json['nonce']} details")
        self.geometry("380x380")
        self.resizable(False, False)
