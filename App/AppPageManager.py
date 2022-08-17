from tkinter import *
from PIL import Image
import utility_functions
from App.MarketAnalysis.MarketAnalysisPage import MarketAnalysisPage
from App.Contacts.ContactsPage import ContactsPage
from App.ManageFunds.FundsPage import FundsPage
from App.MenuButton import MenuButton
from App.YourWallet.WalletPage import WalletPage
from Page import Page


class AppPageManager(Page):

    WALLET_BTN = "App/BtnAssets/wallet_btn.png"
    WALLET_BTN_FOCUS = "App/BtnAssets/wallet_btn_focus.png"

    FUNDS_BTN = "App/BtnAssets/funds_btn.png"
    FUNDS_BTN_FOCUS = "App/BtnAssets/funds_btn_focus.png"

    CONTACTS_BTN = "App/BtnAssets/contacts_btn.png"
    CONTACTS_BTN_FOCUS = "App/BtnAssets/contacts_btn_focus.png"

    MARKET_ANALYSIS_BTN = "App/BtnAssets/market_analysis_btn.png"
    MARKET_ANALYSIS_BTN_FOCUS = "App/BtnAssets/market_analysis_btn_focus.png"

    buttons = []

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.default_active_page = kwargs.get("default_active_page", None)

        self.canvas = Canvas(
            root,
            bg="#ffffff",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.content_frame = Frame(root, bg="white")
        self.content_frame.place(
            x=268, y=7,
            width=522,
            height=466
        )

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
            related_page=WalletPage,
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
            related_page=FundsPage,
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
            related_page=ContactsPage,
            borderwidth=0,
            highlightthickness=0,
            relief="flat")

        self.contacts_btn.place(
            x=28, y=334,
            width=204,
            height=42)

        self.root.img_market = PhotoImage(file=self.MARKET_ANALYSIS_BTN)
        self.root.focused_img_market = PhotoImage(file=self.MARKET_ANALYSIS_BTN_FOCUS)
        self.market_analysis_btn = MenuButton(
            image=self.root.img_market,
            focused_image=self.root.focused_img_market,
            related_page=MarketAnalysisPage,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.market_analysis_btn.place(
            x=28, y=380,
            width=202,
            height=42)

        self.buttons = [self.wallet_btn, self.funds_btn, self.contacts_btn, self.market_analysis_btn]

        self.wallet_btn.bind("<Button>", self.btn_clicked)
        self.funds_btn.bind("<Button>", self.btn_clicked)
        self.contacts_btn.bind("<Button>", self.btn_clicked)
        self.market_analysis_btn.bind("<Button>", self.btn_clicked)

        self.render_default_page()

    def render_default_page(self):
        for btn in self.buttons:
            if btn.related_page is self.default_active_page:
                self.btn_clicked(def_btn=btn)

    def update_menu(self, clicked_btn):
        clicked_btn.config(
            image=clicked_btn.focused_image
        )
        for btn in self.buttons:
            if btn is not clicked_btn:
                btn.config(
                    image=btn.default_image
                )

    def clean_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def btn_clicked(self, event=None, def_btn=None):
        btn = None
        if def_btn is None:
            btn = event.widget
        elif event is None:
            btn = def_btn

        self.update_menu(btn)
        self.clean_frame()

        self.to_page(
            page=btn.related_page,
            frame=self.content_frame,
            eth_account=self.eth_account,
        )
