from tkinter import *

import utility_functions
from App.YourWallet.TokenDetails.TransactionTile.TransactionDetails.TransactionDetails import TransactionDetails


class TransactionTile(Frame):

    SENT_BUTTON_IMG = "App/YourWallet/TokenDetails/TransactionTile/sent_img.png"
    RECEIVED_BUTTON_IMG = "App/YourWallet/TokenDetails/TransactionTile/received_img.png"
    TILE_BACKGROUND = "App/YourWallet/TokenDetails/TransactionTile/tile_background.png"

    def __init__(self, genesis_root=None, web3=None, transaction_json=None, eth_account=None, token=None, **kwargs):
        super().__init__(**kwargs)

        self.genesis_root = genesis_root,
        self.web3 = web3
        self.transaction_json = transaction_json
        self.eth_account = eth_account
        self.token = token
        self.transaction_details_page = None

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
            text=("-" if self.is_sent() else "+") + f"{str(self.get_transaction_value())}",
            font=("Arial", 12),
            fg="red" if self.is_sent() else "green",
            bg="white"
        )
        self.amount_transacted.place(
            x=300, y=6
        )

        self.token_symbol = Label(
            self,
            text="ETH" if self.token is None else utility_functions.format_string(string=self.token["symbol"], cut_to=9),
            font=("Arial", 8),
            bg="white"
        )
        self.token_symbol.place(
            x=302, y=26,
        )

        utility_functions.bind_all_components(
            obj=self,
            sequence="<Button>",
            func=self.show_transaction_details,
        )

    def is_sent(self):
        if self.transaction_json["from"] == self.eth_account.account.address.lower():
            return True
        else:
            return False  # Transaction not sent means transaction received

    def get_transaction_value(self):
        value = float(self.transaction_json['value'])
        gas_fee = float((int(self.transaction_json['gasUsed']) * int(self.transaction_json["gasPrice"])))
        total = value  #+ gas_fee
        if self.token is None:
            str_amount = str(round(self.web3.fromWei(total, 'ether'), 5))[0:5]
            return float(str_amount)
        else:
            return utility_functions.format_balance(amount=total, decimals=self.token['decimals'], cut_until=5)

    def show_transaction_details(self, event):
        if utility_functions.toplevel_exist(toplevel=self.transaction_details_page) is False:
            self.transaction_details_page = TransactionDetails(
                self.genesis_root,
                self.web3,
                transaction_json=self.transaction_json,
                token=self.token,
                is_sent=self.is_sent(),
                bg="white"
            )
            self.transaction_details_page.mainloop()
