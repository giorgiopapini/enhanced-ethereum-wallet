from tkinter import *
import webbrowser


class BuyPage(Toplevel):

    BACKGROUND = "App/YourWallet/TokenDetails/BuyPage/background.png"
    MOONPAY_IMG = "App/YourWallet/TokenDetails/BuyPage/moonpay_btn.png"
    WYRE_BTN = "App/YourWallet/TokenDetails/BuyPage/wyre_btn.png"

    MOONPAY_URL = "https://www.moonpay.com/buy"
    WYRE_URL = "https://pay.sendwyre.com/"

    def __init__(self, root, web3, **kwargs):
        super().__init__(**kwargs)

        self.root = root
        self.web3 = web3

        self.title("Buy ETH Page")
        self.geometry("380x380")
        self.resizable(False, False)

        self.canvas = Canvas(
            self,
            bg="#ffffff",
            height=380,
            width=380,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=self.BACKGROUND)
        self.background = self.canvas.create_image(
            190.0, 207.5,
            image=self.background_img
        )

        self.send_label = Label(
            self,
            text=f"Buy ETH",
            font=("OpenSansRoman-SemiBold", 30),
            bg="white"
        )
        self.send_label.place(
            x=23, y=24
        )

        self.description_label = Label(
            self,
            text=f"Buy ETH to exchange money with\naddresses or smart contracts",
            font=("OpenSansRoman-Regular", 14),
            justify=LEFT,
            bg="white"
        )
        self.description_label.place(
            x=25, y=75
        )

        self.moonpay_btn_img = PhotoImage(file=self.MOONPAY_IMG)
        self.moonpay_btn = Button(
            self,
            image=self.moonpay_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: webbrowser.open(self.MOONPAY_URL, new=2),
            relief="flat"
        )

        self.moonpay_btn.place(
            x=99, y=201,
            width=188,
            height=35
        )

        self.wyre_btn_img = PhotoImage(file=self.WYRE_BTN)
        self.wyre_btn = Button(
            self,
            image=self.wyre_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: webbrowser.open(self.WYRE_URL, new=2),
            relief="flat"
        )

        self.wyre_btn.place(
            x=117, y=321,
            width=153,
            height=35
        )
