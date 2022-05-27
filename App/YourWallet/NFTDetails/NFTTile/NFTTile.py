from tkinter import *

import utility_functions


class NFTTile(Frame):

    BACKGROUND = "App/YourWallet/NFTDetails/NFTTile/background.png"
    NFT_RENDER_IMG = "App/YourWallet/NFTDetails/NFTTile/render_nft_image.png"
    ARROW_IMG = "App/YourWallet/TokenTile/arrow_img.png"

    def __init__(self, genesis_root=None, web3=None, next_page_frame=None, previous_page=None, eth_account=None, nft=None, **kwargs):
        super().__init__(**kwargs)

        self.genesis_root = genesis_root
        self.web3 = web3
        self.next_page_frame = next_page_frame
        self.previous_page = previous_page
        self.eth_account = eth_account

        self.nft = nft

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
            relief="flat"
        )

        self.arrow.place(
            x=336, y=15,
            width=15,
            height=19
        )

    def render_image(self):
        print(self.nft["image"])
        # Create another window in which the nft is displayed (maybe through tkinter webview)

    # Arrow button should call a callback function to NFTDetailsPage --> Change the currently selected NFT
