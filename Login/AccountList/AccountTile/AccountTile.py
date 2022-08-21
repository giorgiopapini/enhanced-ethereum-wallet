from tkinter import *
import os
import shutil


class AccountTile(Frame):

    ACCOUNT_BG_IMG = "Login/AccountList/AccountTile/account_bg_img.png"
    ACCOUNT_ICON_IMG = "Login/AccountList/AccountTile/account_icon_img.png"
    DELETE_BTN_IMG = "Login/AccountList/AccountTile/delete_btn_img.png"

    def __init__(self, genesis_root=None, address=None, callback_reload_list=None, accounts_num=None, **kwargs):
        super().__init__(**kwargs)

        self.genesis_root = genesis_root
        self.address = address
        self.callback_reload_list = callback_reload_list
        self.accounts_num = accounts_num

        self.background_img = PhotoImage(file=self.ACCOUNT_BG_IMG)
        self.background = Label(
            self,
            image=self.background_img,
            bd=0,
            highlightthickness=0,
            relief="flat"
        )
        self.background.pack()

        self.account_icon_img = PhotoImage(file=self.ACCOUNT_ICON_IMG)
        self.account_icon_label = Label(
            self,
            image=self.account_icon_img
        )
        self.account_icon_label.place(
            x=14, y=10,
            width=30,
            height=30
        )

        self.address_label = Label(
            self,
            text=self.address,
            font=("Arial", 8),
            bg="white"
        )
        self.address_label.place(
             x=50, y=16
        )

        self.delete_btn_img = PhotoImage(file=self.DELETE_BTN_IMG)
        self.delete_btn = Button(
            self,
            image=self.delete_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.delete_account_data,
            relief="flat",
            cursor="hand2"
        )
        self.delete_btn.place(
            x=339, y=10,
            width=30,
            height=30
        )

    def delete_account_data(self):
        if self.accounts_num > 1:
            partial_path = f"App\\Accounts\\{self.address}\\"
            shutil.rmtree(f"{os.getcwd()}\\{partial_path}")

            self.callback_reload_list()
