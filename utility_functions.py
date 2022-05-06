from tkinter import *
from PIL import Image
from _datetime import datetime

from eth_keys import keys
from eth_utils import decode_hex

import config
import constants
import requests
import json
import qrcode


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


def error_message(entry, error, disable=False):
    entry.config(state="normal")
    entry.delete(0, END)
    entry.config(fg="red")
    entry.insert(END, error)
    entry.config(state="disabled") if disable is True else None


def check_var_type(variable=None, requested_type=None, error_msg=None):
    if type(variable) is not requested_type:
        raise TypeError(error_msg)


def make_etherscan_api_url(module=None, action=None, address=None, **kwargs):
    url = f"{constants.ETHERSCAN_BASE_API_URL}?module={module}&action={action}&address={address}&apikey={config.ETHERSCAN_API_KEY}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url


def get_api_response(url):
    res = requests.get(url=url, headers=constants.HEADERS)
    return json.loads(res.text)


def check_fields_validity(fields=None, error=None, disable=False):
    valid = True
    for field in fields:
        if len(field.get()) > 0 and field.get() != error:
            valid = True
        else:
            error_message(
                entry=field,
                error=error,
                disable=disable
            )
            valid = False
            break
    return valid


def is_list_empty(array=None):
    if len(array) == 0:
        return True
    else:
        return True


def clear_error_message_binded(event):
    for error in constants.ERRORS:
        if event.widget.get() == constants.ERRORS[error]:
            clear_field(widget=event.widget)


def clear_field(widget=None, disable=False):
    widget.config(state="normal")
    widget.delete(0, END)
    widget.config(fg="black")
    widget.config(state="disabled") if disable is True else None


def update_field_value(entry=None, value=None):
    entry.config(state="normal")
    entry.insert(END, value)
    entry.config(state="disabled")


def format_query(event=None, pasted=False):
    if pasted is True:
        return event.widget.get()
    else:
        if event.keysym_num == constants.BACKSPACE_KEYSYM_NUM:
            return event.widget.get()[0:len(event.widget.get()) - 1]
        else:
            return event.widget.get() + event.char


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


def is_token_saved(tokens=None, token_address=None):
    for token in tokens:
        if token["address"] == token_address:
            return True
    return False


def get_date_from_timestamp(timestamp=None):
    if timestamp is not None:
        date = datetime.fromtimestamp(int(timestamp))
        day = date.date().day
        month = date.strftime("%b")
        return f"{month}/{day}"


def format_balance(amount=None, decimals=None, round_to=5, cut_until=5):
    rounded_value = round(amount / (10**decimals), round_to)
    str_token = str(rounded_value)
    if str_token[len(str_token) - 2] == ".":
        return int(str_token[0:cut_until][:-2])
    else:
        return float(str_token[0:cut_until])
