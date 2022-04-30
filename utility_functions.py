from tkinter import *
from PIL import Image

from eth_keys import keys
from eth_utils import decode_hex

import constants
import json
import qrcode

from web3 import Web3
from threading import Thread


def user_is_registered():
    try:
        with open("encrypted_private_keys.json", "r") as json_file:
            # IMPORTANTE!!! --> Cambiare condizioni (verificare che il file esiste e verificare che l'array di private
            # keys non sia vuoto)
            if not json_file.read(1):
                return False
            else:
                return True
    except FileNotFoundError:
        return False


def error_message(entry, error):
    entry.delete(0, END)
    entry.config(fg="red")
    entry.insert(END, error)


def check_var_type(variable=None, requested_type=None, error_msg=None):
    if type(variable) is not requested_type:
        raise TypeError(error_msg)


def check_fields_validity(fields=None, error=None):
    valid = True
    for field in fields:
        if len(field.get()) > 0 and field.get() != error:
            valid = True
        else:
            error_message(
                entry=field,
                error=error
            )
            valid = False
            break
    return valid


def is_list_empty(array=None):
    if len(array) == 0:
        return True
    else:
        return True


def clear_error_message(event):
    for error in constants.ERRORS:
        if event.widget.get() == constants.ERRORS[error]:
            event.widget.delete(0, END)
            event.widget.config(fg="black")


def create_qrcode(data):
    img = qrcode.make(data)
    img.save("public_key_qrcode.png")


def resize_image(image=None, width=None, heigth=None, path=None):
    try:
        res_qrcode = Image.open(path)
    except FileNotFoundError:
        img = image.resize((width, heigth))
        img.save(path)


def get_private_key(web3, password):
    with open("encrypted_private_keys.json", "r") as json_file:
        user_data = json.load(json_file)["keys"][0]
        print(user_data)
        return web3.eth.account.decrypt(user_data, password).hex()


def get_address(private_key):
    priv_key_bytes = decode_hex(private_key)
    priv_key = keys.PrivateKey(priv_key_bytes)
    pub_key = priv_key.public_key
    address = pub_key.to_checksum_address()
    return address


def get_contract_name(contract_address=None, web3=None):
    print(constants.ERC20_ABI)
    contract = web3.eth.contract(address=contract_address, abi=constants.ERC20_ABI)
    print(contract.functions.name().call())


def get_token_amount(token_address=None, user_address=None, web3=None):
    token = web3.eth.contract(address=token_address, abi=constants.ERC20_ABI)
    print(token.functions.balanceOf(user_address).call())
    return token.functions.balanceOf(user_address).call()


def format_query(event=None, pasted=False):
    if pasted is True:
        return event.widget.get()
    else:
        if event.keysym_num == constants.BACKSPACE_KEYSYM_NUM:
            return event.widget.get()[0:len(event.widget.get()) - 1]
        else:
            return event.widget.get() + event.char
