from tkinter import *

import utility_functions


class TransactionTile(Frame):

    SENT_BUTTON_IMG = "App/YourWallet/TokenDetails/TransactionTile/sent_img.png"
    RECEIVED_BUTTON_IMG = "App/YourWallet/TokenDetails/TransactionTile/received_img.png"
    TILE_BACKGROUND = "App/YourWallet/TokenDetails/TransactionTile/tile_background.png"

    def __init__(self, genesis_root=None, web3=None, transaction_json=None, eth_account=None, **kwargs):
        super().__init__(**kwargs)

        self.genesis_root = genesis_root,
        self.web3 = web3
        self.transaction_json = transaction_json
        self.eth_account = eth_account

        self.background_img = PhotoImage(file=self.TILE_BACKGROUND)
        self.background = Label(
            self,
            image=self.background_img,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.background.pack()

        self.action_img = PhotoImage(
            file=self.SENT_BUTTON_IMG if self.is_sent() is True else self.RECEIVED_BUTTON_IMG
        )
        self.action = Label(
            self,
            image=self.action_img,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.action.place(
            x=22, y=10,
            width=30,
            height=30
        )

        self.action_label = Label(
            self,
            text="Sent" if self.is_sent() is True else "Received",
            font=("Arial", 12),
            bg="white",
        )
        self.action_label.place(
            x=68, y=6,
        )

        self.transaction_details = Label(
            self,
            text=f"{utility_functions.get_date_from_timestamp(self.transaction_json['timeStamp'])} · " +
                 (
                     f"To: {self.transaction_json['to'][0:6]}...{self.transaction_json['to'][38:42]}" if self.is_sent()
                     else f"From:{transaction_json['from'][0:6]}...{self.transaction_json['from'][38:42]}"
                 ),
            font=("Lucida Console", 9),
            bg="white",
        )
        self.transaction_details.place(
            x=68, y=28
        )

        self.amount_transacted = Label(
            self,
            text=("-" if self.is_sent() else "+") + f"{round(self.get_transaction_value(), 3)}",
            font=("Arial", 13),
            fg="red" if self.is_sent() else "green",
            bg="white"
        )
        self.amount_transacted.place(
            x=300, y=15
        )

    def is_sent(self):
        if self.transaction_json["from"] == self.eth_account.account.address.lower():
            return True
        else:
            return False  # Transaction not sent means transaction received

    def get_transaction_value(self):
        value = int(self.transaction_json['value'])
        return self.web3.fromWei(value, 'ether')
