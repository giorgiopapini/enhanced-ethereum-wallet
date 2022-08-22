import json
import os
from tkinter import *

from App.ReusableComponents.ListElement import ListElement
from App.ReusableComponents.ListWidget import ListWidget
from Login.AccountList.AccountTile.AccountTile import AccountTile


class AccountList(Toplevel):

    BACKGROUND = "Login/AccountList/background.png"

    def __init__(self, root, web3, **kwargs):
        super().__init__(**kwargs)

        self.root = root
        self.web3 = web3

        self.title("Add contact")
        self.geometry("484x380")
        self.resizable(False, False)

        self.canvas = Canvas(
            self,
            bg="#ffffff",
            height=380,
            width=484,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=self.BACKGROUND)
        self.background = self.canvas.create_image(
            122.5, 48.5,
            image=self.background_img
        )

        self.account_list_frame = Frame(self, bg="white")
        self.account_list_frame.place(
            x=28, y=88,
            width=428,
            height=265
        )

        self.account_list = ListWidget(
            parent=self.account_list_frame,
            space_between=3,
            elements=self.load_accounts()
        )

        self.get_addresses()

    def load_accounts(self):
        accounts = []
        addresses = self.get_addresses()
        current_address = self.get_active_address()

        for address in addresses:
            accounts.append(
                ListElement(
                    widget=AccountTile,
                    genesis_root=self.root,
                    address=address,
                    callback_reload_list=self.reload_accounts,
                    accounts_num=len(addresses),
                    deletable=False if current_address.lower() == address[2:].lower() else True,
                    height=50
                )
            )
        return accounts

    def get_addresses(self):
        return os.listdir("App/Accounts/")

    def get_active_address(self):
        with open("encrypted_private_keys.json", "r") as file:
            json_data = json.load(file)
            data = json.loads(json_data["keys"][0])
            return data["address"]

    def reload_accounts(self):
        self.account_list.refresh_list(
            parent_frame=self.account_list_frame,
            elements=self.load_accounts()
        )
