from tkinter import *
from tkinterweb import HtmlFrame
import utility_functions


class NFTTile(Frame):

    BACKGROUND = "App/YourWallet/NFTDetails/NFTTile/background.png"
    IMAGE_ICON = "App/YourWallet/NFTDetails/NFTTile/image_icon.png"
    ARROW_IMG = "App/YourWallet/TokenTile/arrow_img.png"

    nft_toplevel = None

    def __init__(self, genesis_root=None, web3=None, next_page_frame=None, previous_page=None, eth_account=None, nft=None, callback=None, **kwargs):
        super().__init__(**kwargs)

        self.genesis_root = genesis_root
        self.web3 = web3
        self.next_page_frame = next_page_frame
        self.previous_page = previous_page
        self.eth_account = eth_account

        self.nft = nft
        self.callback = callback

        self.background_img = PhotoImage(file=self.BACKGROUND)
        self.background = Label(
            self,
            image=self.background_img,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            cursor="hand2"
        )
        self.background.pack()

        self.image_icon_img = PhotoImage(file=self.IMAGE_ICON)
        self.image_icon = Label(
            self,
            image=self.image_icon_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            cursor="hand2"
        )

        self.image_icon.place(
            x=21, y=9,
            width=32,
            height=32
        )

        self.nft_name = Label(
            self,
            text=utility_functions.format_string(string=self.nft['name'], cut_to=30),
            font=("OpenSansRoman", int(13.0)),
            cursor="hand2",
            bg="white"
        )
        self.nft_name.place(
            x=67, y=14.1
        )

        self.arrow_img = PhotoImage(file=self.ARROW_IMG)
        self.arrow = Button(
            self,
            image=self.arrow_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.arrow_clicked,
            relief="flat",
            cursor="hand2"
        )

        self.arrow.place(
            x=336, y=15,
            width=15,
            height=19
        )

        self.background.bind("<Button>", self.render_image)
        self.image_icon.bind("<Button>", self.render_image)
        self.nft_name.bind("<Button>", self.render_image)

    def render_image(self, event):
        if utility_functions.toplevel_exist(toplevel=self.nft_toplevel) is False:
            self.nft_toplevel = Toplevel(self.genesis_root, bg="white")
            self.nft_toplevel.title(self.nft["name"])
            self.nft_toplevel.geometry('600x600')

            url_text = Text(self.nft_toplevel, height=1, borderwidth=0, font=("OpenSansRoman", int(10.5)))
            url_text.insert(1.0, f"URL: {self.nft['image']}")
            url_text.pack()
            url_text.configure(state="disabled")
            url_text.configure(inactiveselectbackground=url_text.cget("selectbackground"))
            url_text.pack()

            frame = HtmlFrame(self.nft_toplevel)
            frame.load_website(self.nft["image"])
            frame.pack(expand=True, fill=Y)
            self.nft_toplevel.mainloop()

    def arrow_clicked(self):

        self.callback(nft_clicked=self.nft)
