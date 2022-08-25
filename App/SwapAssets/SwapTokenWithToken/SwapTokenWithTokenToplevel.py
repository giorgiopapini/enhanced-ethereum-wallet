from tkinter import *


class SwapTokenWithToken(Toplevel):

    def __init__(self, root, web3, eth_account=None, **kwargs):
        super().__init__(**kwargs)

        self.root = root
        self.web3 = web3
        self.eth_account = eth_account

        self.title("Swap ERC20 token with ERC20 token")
        self.geometry("400x380")
        self.resizable(False, False)
