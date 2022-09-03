import mimetypes
from decimal import *
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


def check_var_type(variable=None, requested_type=None, error_msg=None):
    if type(variable) is not requested_type:
        raise TypeError(error_msg)


def make_etherscan_api_url(base_url=constants.ETHERSCAN_BASE_API_URL, module=None, action=None, **kwargs):
    url = f"{base_url}?module={module}&action={action}&apikey={config.ETHERSCAN_API_KEY}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url


def make_coingecko_coins_api_url(base_url=constants.COINGECKO_BASE_API_URL, coin_id="", action="", **kwargs):
    url = f"{base_url}/coins/{coin_id}/{action}?"
    for key, value in kwargs.items():
        url += f"&{str(key)}={str(value)}"
    return url


def get_api_response(url):
    res = requests.get(url=url, headers=constants.HEADERS)
    return json.loads(res.text)


def get_file_extension_from_url(url=None):
    res = requests.get(url)

    return mimetypes.guess_extension(res.headers['content-type'])


def check_fields_validity(fields=None, error=None):
    valid = True
    for field in fields:
        if len(field.get()) > 0 and field.get() != error:
            valid = True
        else:
            valid = False
            field.show_error(error=error)
            break
    return valid


def check_address_field_validity(address_field=None, error=None, web3=None):
    if web3.isAddress(address_field.get()) is False:
        address_field.show_error(error=error)
        return False
    return True


def is_list_empty(array=None):
    if len(array) == 0:
        return True
    else:
        return True


def format_query(event=None, pasted=False):
    text = event.widget.get()
    if pasted is True:
        return text
    else:
        if event.keysym_num == constants.BACKSPACE_KEYSYM_NUM:
            return text[0:len(event.widget.get()) - 1]
        else:
            return text + event.char


def format_nft_name(nft_metadata=None, contract_name=None, token_id=None):
    if "name" in nft_metadata and nft_metadata["name"][0] != "#":
        return nft_metadata["name"]
    else:
        return f"{contract_name} #{token_id}"


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


def is_nft_saved(nfts=None, token_address=None, token_id=None):
    for nft in nfts:
        if nft["address"] == token_address and nft["token_id"] == token_id:
            return True
    return False


def get_date_from_timestamp(timestamp=None):
    if timestamp is not None:
        date = datetime.fromtimestamp(int(timestamp))
        day = date.date().day
        month = date.strftime("%b")
        return f"{month}/{day}"


def format_balance(amount=None, decimals=None, round_to=5, cut_until=5):
    rounded_value = round(amount / (10 ** decimals), round_to)
    str_token = str(rounded_value)
    if str_token[len(str_token) - 2] == ".":
        return int(str_token[0:cut_until][:-2])
    else:
        return float(str_token[0:cut_until])


def convert_exponential_to_decimal(number=None, decimals=None):
    exp = float(number) / int(10 ** decimals)
    formatting_string = f".{decimals}f"
    formatted_num = f"{exp:{formatting_string}}".rstrip("0").rstrip(".")
    return formatted_num


def format_string(string="", cut_to=20):
    if len(string) > cut_to:
        return f"{string}"[0:(cut_to - 3)] + "..."
    return string[0:cut_to]


def toplevel_exist(toplevel=None):
    if toplevel is None or not Toplevel.winfo_exists(toplevel):
        return False
    return True


def bind_all_components(obj=None, sequence=None, func=None, add=None):
    obj.bind(sequence, func, add)
    for child in obj.winfo_children():
        child.bind(sequence, func, add)
