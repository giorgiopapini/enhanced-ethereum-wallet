from tkinter import *
from PIL import Image
import constants
import utility_functions
from Page import Page


class AppPageManager(Page):
    WALLET_BTN = "App/wallet_btn.png"
    WALLET_BTN_FOCUS = "App/wallet_btn_focus.png"

    FUNDS_BTN = "App/funds_btn.png"
    CONTACTS_BTN = "App/contacts_btn.png"
    AUTOMATION_BTN = "App/automation_btn.png"

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.account = kwargs.get("account")

        self.canvas = Canvas(
            root,
            bg="#ffffff",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        utility_functions.resize_image(
            image=Image.open("public_key_qrcode.png"),
            width=120,
            heigth=120,
            path="App/resized_qrcode.png",
        )

        self.img_qr_code = PhotoImage(file=f"App/resized_qrcode.png")
        self.qr_code = Label(
            image=self.img_qr_code
        )

        self.qr_code.place(
            x=78, y=67,
            width=105,
            height=105
        )

        self.background_img = PhotoImage(file=f"App/background.png")
        self.background = self.canvas.create_image(
            133.5, 240.0,
            image=self.background_img)

        self.img_wallet = PhotoImage(file=self.WALLET_BTN)
        self.wallet_btn = Button(
            image=self.img_wallet,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat")

        self.wallet_btn.place(
            x=28, y=240,
            width=202,
            height=42)

        self.img_funds = PhotoImage(file=self.FUNDS_BTN)
        self.funds_btn = Button(
            image=self.img_funds,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat")

        self.funds_btn.place(
            x=28, y=288,
            width=202,
            height=42)

        self.img_contacts = PhotoImage(file=self.CONTACTS_BTN)
        self.contacts_btn = Button(
            image=self.img_contacts,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat")

        self.contacts_btn.place(
            x=28, y=334,
            width=204,
            height=42)

        self.img_automation = PhotoImage(file=self.AUTOMATION_BTN)
        self.automation_btn = Button(
            image=self.img_automation,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat")

        self.automation_btn.place(
            x=28, y=380,
            width=202,
            height=42)

    # self.b0.bind("<Button-1>", lambda _: "break", add=True)  Serve per disabilitare l'animazione del click sul button

    def btn_clicked(self):
        print("clicked")
