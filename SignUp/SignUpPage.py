import json
from tkinter import *
import constants
import utility_functions
from App.Homepage.Homepage import Homepage

from Page import Page


class SignUpPage(Page):

    #self.root
    #self.private_key
    #self.password

    def __init__(self, root, web3, **kwargs):
        super().__init__(root, web3, **kwargs)

        self.account = kwargs.get("account", None)
        self.password = ""

        self.canvas = Canvas(
            root,
            bg="#ffffff",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.img1 = PhotoImage(file=f"SignUp/img1.png")
        self.b1 = Button(
            image=self.img1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.to_page(
                page=self.previous_page,
            ),
            relief="flat")

        self.b1.place(
            x=16, y=106,
            width=38,
            height=38)

        self.img0 = PhotoImage(file=f"SignUp/img0.png")
        self.b0 = Button(
            image=self.img0,
            borderwidth=0,
            highlightthickness=0,
            command=self.sign_up,
            relief="flat")

        self.b0.place(
            x=220, y=409,
            width=130,
            height=47)

        self.entry0_img = PhotoImage(file=f"SignUp/img_textBox0.png")
        self.entry0_bg = self.canvas.create_image(
            199.5, 283.5,
            image=self.entry0_img)

        self.entry0 = Entry(
            bd=0,
            bg="#ffffff",
            disabledbackground="#ffffff",
            highlightthickness=0)

        self.entry0.insert(END, self.account.privateKey.hex())
        self.entry0.config(state=DISABLED)

        self.entry0.place(
            x=73.5, y=269,
            width=252.0,
            height=31)

        self.entry1_img = PhotoImage(file=f"SignUp/img_textBox1.png")
        self.entry1_bg = self.canvas.create_image(
            199.5, 359.5,
            image=self.entry1_img)

        self.entry1 = Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0)

        self.entry1.place(
            x=73.5, y=345,
            width=252.0,
            height=31)

        self.entry1.bind("<Button>", utility_functions.clear_error_message)

        self.background_img = PhotoImage(file=f"SignUp/background.png")
        self.background = self.canvas.create_image(
            400.0, 186.0,
            image=self.background_img)

    def sign_up(self):
        self.password = self.entry1.get()
        if len(self.password) > constants.MIN_LENGTH_PASSWORD and self.password != constants.ERRORS["ERROR_PASSWORD_LENGTH"]:
            for widget in self.root.winfo_children():
                widget.destroy()
            json_string = json.dumps(self.account.encrypt(self.password))
            print(json_string)
            print(self.account.address)
            with open("encrypted_private_keys.json", "w+") as priv_key_json:
                priv_key_json.write(json.dumps({"keys": [json_string]}))

            self.to_page(
                page=Homepage,
                previous_page=None,
                account=self.account,
            )
            print(self.web3.eth.account.decrypt(json_string, self.password).hex())
        else:
            utility_functions.error_message(self.entry1, constants.ERRORS["ERROR_PASSWORD_LENGTH"])

    def show_entire_private_key(self):
        # IMPORTANTE!!! --> Creare tasto che crei un popup che mostri la private key per intero --> La private key
        # é piú lunga del textbox, quindi é necessario che per procede l'utenta debba attivare e il popup --> Tramite
        # una variabile booleana verificare se l'utente ha preso visione del popup e permettergli (dopo aver inserito
        # la password) di procedere alla schermata successiva
        pass

