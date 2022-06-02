from tkinter import *

import config
import utility_functions
from Welcome.WelcomePage import WelcomePage
from Login.LoginPage import LoginPage
from web3 import Web3


def main():
    root = Tk()
    root.title("UWallet")
    root.geometry('800x480')
    root.resizable(False, False)

    web3 = Web3(Web3.HTTPProvider(config.INFURA_GOERLI_API_URL))

    if utility_functions.user_is_registered():
        LoginPage(root, web3)
    else:
        WelcomePage(root, web3)

    root.mainloop()


if __name__ == '__main__':
    main()
