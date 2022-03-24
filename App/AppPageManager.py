from tkinter import *
from PIL import Image
import constants
import utility_functions
from Page import Page


class AppPageManager(Page):

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

        self.img0 = PhotoImage(file=f"App/img0.png")
        self.b0 = Button(
            image=self.img0,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat")

        self.b0.place(
            x=28, y=380,
            width=202,
            height=42)

        self.img1 = PhotoImage(file=f"App/img1.png")
        self.b1 = Button(
            image=self.img1,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat")

        self.b1.place(
            x=28, y=334,
            width=204,
            height=42)

        self.img2 = PhotoImage(file=f"App/img2.png")
        self.b2 = Button(
            image=self.img2,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat")

        self.b2.place(
            x=28, y=288,
            width=202,
            height=42)

        self.img3 = PhotoImage(file=f"App/img3.png")
        self.b3 = Button(
            image=self.img3,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat")

        self.b3.place(
            x=28, y=240,
            width=202,
            height=42)

    # self.b0.bind("<Button-1>", lambda _: "break", add=True)  Serve per disabilitare l'animazione del click sul button

    def btn_clicked(self):
        print("clicked")
