from tkinter import *
from tkinterweb import HtmlFrame
import utility_functions


class NFTTile(Frame):

    BACKGROUND = "App/YourWallet/NFTDetails/NFTTile/background.png"
    NFT_RENDER_IMG = "App/YourWallet/NFTDetails/NFTTile/render_nft_image.png"
    ARROW_IMG = "App/YourWallet/TokenTile/arrow_img.png"

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
            relief="ridge"
        )
        self.background.pack()

        self.render_button_img = PhotoImage(file=self.NFT_RENDER_IMG)
        self.render_button = Button(
            self,
            image=self.render_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.render_image,
            relief="flat"
        )

        self.render_button.place(
            x=21, y=9,
            width=32,
            height=32
        )

        self.nft_name = Label(
            self,
            text=utility_functions.format_string(string=self.nft['name'], cut_to=30),
            font=("OpenSansRoman", int(13.0)),
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

    def render_image(self):
        top = Toplevel(self.genesis_root, bg="white")
        top.title(self.nft["name"])
        top.geometry('600x600')

        url_text = Text(top, height=1, borderwidth=0, font=("OpenSansRoman", int(10.5)))
        url_text.insert(1.0, f"URL: {self.nft['image']}")
        url_text.pack()
        url_text.configure(state="disabled")
        url_text.configure(inactiveselectbackground=url_text.cget("selectbackground"))
        url_text.pack()

        frame = HtmlFrame(top)
        frame.load_website(self.nft["image"])
        frame.pack(expand=True, fill=Y)
        top.mainloop()

    def arrow_clicked(self):
        self.callback(nft_clicked=self.nft)
