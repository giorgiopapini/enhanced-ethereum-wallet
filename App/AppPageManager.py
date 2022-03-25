from tkinter import *
from PIL import Image
import utility_functions
from App.MenuButton import MenuButton
from Page import Page


class AppPageManager(Page):
    WALLET_BTN = "App/BtnAssets/wallet_btn.png"
    WALLET_BTN_FOCUS = "App/BtnAssets/wallet_btn_focus.png"

    FUNDS_BTN = "App/BtnAssets/funds_btn.png"
    FUNDS_BTN_FOCUS = "App/BtnAssets/funds_btn_focus.png"

    CONTACTS_BTN = "App/BtnAssets/contacts_btn.png"
    CONTACTS_BTN_FOCUS = "App/BtnAssets/contacts_btn_focus.png"

    AUTOMATION_BTN = "App/BtnAssets/automation_btn.png"
    AUTOMATION_BTN_FOCUS = "App/BtnAssets/automation_btn_focus.png"

    buttons = []

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

        self.root.img_wallet = PhotoImage(file=self.WALLET_BTN)
        self.root.focused_img_wallet = PhotoImage(file=self.WALLET_BTN_FOCUS)
        self.wallet_btn = MenuButton(
            image=self.root.img_wallet,
            focused_image=self.root.focused_img_wallet,
            borderwidth=0,
            highlightthickness=0,
            relief="flat")

        self.wallet_btn.place(
            x=28, y=240,
            width=202,
            height=42)

        self.root.img_funds = PhotoImage(file=self.FUNDS_BTN)
        self.root.focused_img_funds = PhotoImage(file=self.FUNDS_BTN_FOCUS)
        self.funds_btn = MenuButton(
            image=self.root.img_funds,
            focused_image=self.root.focused_img_funds,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
        )

        self.funds_btn.place(
            x=28, y=288,
            width=202,
            height=42)

        self.root.img_contacts = PhotoImage(file=self.CONTACTS_BTN)
        self.root.focused_img_contacts = PhotoImage(file=self.CONTACTS_BTN_FOCUS)
        self.contacts_btn = MenuButton(
            image=self.root.img_contacts,
            focused_image=self.root.focused_img_contacts,
            borderwidth=0,
            highlightthickness=0,
            relief="flat")

        self.contacts_btn.place(
            x=28, y=334,
            width=204,
            height=42)

        self.root.img_automation = PhotoImage(file=self.AUTOMATION_BTN)
        self.root.focused_img_automation = PhotoImage(file=self.AUTOMATION_BTN_FOCUS)
        self.automation_btn = MenuButton(
            image=self.root.img_automation,
            focused_image=self.root.focused_img_automation,
            borderwidth=0,
            highlightthickness=0,
            relief="flat")

        self.automation_btn.place(
            x=28, y=380,
            width=202,
            height=42)

        self.buttons = [self.wallet_btn, self.funds_btn, self.contacts_btn, self.automation_btn]

        self.wallet_btn.bind("<Button>", self.btn_clicked)
        self.funds_btn.bind("<Button>", self.btn_clicked)
        self.contacts_btn.bind("<Button>", self.btn_clicked)
        self.automation_btn.bind("<Button>", self.btn_clicked)

    def btn_clicked(self, event):
        event.widget.config(
            image=event.widget.focused_image
        )
        for btn in self.buttons:
            if btn is not event.widget:
                btn.config(
                    image=btn.default_image
                )

