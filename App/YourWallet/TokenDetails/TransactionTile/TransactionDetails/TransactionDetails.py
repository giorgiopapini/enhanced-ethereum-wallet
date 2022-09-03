from tkinter import *
import eth_generic_functions
import utility_functions


class TransactionDetails(Toplevel):

    BACKGROUND = "App/YourWallet/TokenDetails/TransactionTile/TransactionDetails/background.png"
    COPY_BUTTON_IMG = "App/YourWallet/TokenDetails/TransactionTile/TransactionDetails/copy_button.png"

    def __init__(self, root, web3, transaction_json=None, token=None, is_sent=None, **kwargs):
        super().__init__(**kwargs)

        self.root = root
        self.web3 = web3
        self.transaction_json = transaction_json
        self.token = token

        self.title(f"Transaction #{transaction_json['nonce']}")
        self.geometry("301x380")
        self.resizable(False, False)

        self.canvas = Canvas(
            self,
            bg="#ffffff",
            height=380,
            width=301,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.title_label = Label(
            self,
            text=f"{'Sent' if is_sent else 'Received'}",
            font=("OpenSansRoman-SemiBold", 28),
            bg="white"
        )
        self.title_label.place(
            x=26, y=20.5
        )

        self.from_label = Label(
            self,
            text=self.format_address(address=self.transaction_json["from"]),
            font=("OpenSansRoman-SemiBold", int(10.8)),
            bg="white"
        )
        self.from_label.place(
            x=70, y=77
        )

        self.copy_btn_img = PhotoImage(file=self.COPY_BUTTON_IMG)
        self.copy_from_btn = Button(
            self,
            image=self.copy_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.copy_to_clipboard(self.transaction_json["from"]),
            relief="flat"
        )

        self.copy_from_btn.place(
            x=255, y=80,
            width=18,
            height=17
        )

        self.to_label = Label(
            self,
            text=self.format_address(address=self.transaction_json["to"]),
            font=("OpenSansRoman-SemiBold", int(10.8)),
            bg="white"
        )
        self.to_label.place(
            x=52, y=106
        )

        self.copy_to_btn = Button(
            self,
            image=self.copy_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.copy_to_clipboard(self.transaction_json["to"]),
            relief="flat"
        )

        self.copy_to_btn.place(
            x=255, y=109,
            width=18,
            height=17
        )

        self.status_label = Label(
            self,
            text=eth_generic_functions.get_transaction_status(tx_hash=self.transaction_json["hash"]),
            font=("OpenSansRoman-SemiBold", int(10.8)),
            fg="green" if eth_generic_functions.get_transaction_status(tx_hash=self.transaction_json["hash"]) is "Confirmed" else "red",
            bg="white"
        )
        self.status_label.place(
            x=77.5, y=185
        )

        self.nonce_label = Label(
            self,
            text=self.transaction_json["nonce"],
            font=("OpenSansRoman-SemiBold", int(10.8)),
            bg="white"
        )
        self.nonce_label.place(
            x=79, y=213
        )

        self.amount_label = Label(
            self,
            text=f"{utility_functions.convert_exponential_to_decimal(number=self.transaction_json['value'], decimals=self.get_decimals())} "
                 f"{'ETH' if self.token is None else self.token['symbol']}",
            font=("OpenSansRoman-SemiBold", int(10.8)),
            bg="white"
        )
        self.amount_label.place(
            x=88.5, y=244
        )

        self.gas_used_label = Label(
            self,
            text=self.transaction_json["gasUsed"],
            font=("OpenSansRoman-SemiBold", int(10.8)),
            bg="white"
        )
        self.gas_used_label.place(
            x=96.5, y=275
        )

        self.gas_price_label = Label(
            self,
            text=f"{utility_functions.convert_exponential_to_decimal(number=self.transaction_json['gasPrice'], decimals=9)} "
                 f"GWEI",
            font=("OpenSansRoman-SemiBold", int(10.8)),
            bg="white"
        )
        self.gas_price_label.place(
            x=96.5, y=307.8
        )

        self.total_gas_fee_label = Label(
            self,
            text=f"{self.get_total_gas_fee()} ETH",
            font=("OpenSansRoman-SemiBold", int(10.8)),
            bg="white"
        )
        self.total_gas_fee_label.place(
            x=118.2, y=338.8
        )

        self.background_img = PhotoImage(file=self.BACKGROUND)
        self.background = self.canvas.create_image(
            149.5, 228.0,
            image=self.background_img
        )

    def get_decimals(self):
        if self.token is None:
            return 18
        else:
            return self.token["decimals"]

    def format_address(self, address=None):
        return f"{address[0:11]}...{address[31:len(address)]}"

    def get_total_gas_fee(self):
        num = utility_functions.convert_exponential_to_decimal(
            number=float((int(self.transaction_json['gasUsed']) * int(self.transaction_json["gasPrice"]))),
            decimals=self.get_decimals()
        )
        return num

    def copy_to_clipboard(self, data):
        if self.root is not None:
            self.root[0].clipboard_clear()
            self.root[0].clipboard_append(data)
            self.root[0].update()
