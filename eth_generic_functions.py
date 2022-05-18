import requests

import constants
import config
import os

import utility_functions
import urllib.request


def get_nft_metadata(contract_address=None, web3=None, token_id=None):
    contract = web3.eth.contract(address=contract_address, abi=constants.ERC721_ABI)
    uri = contract.functions.tokenURI(token_id).call()
    response = utility_functions.get_api_response(
        url=f"{constants.IPFS_BASE_URL}{uri.replace('ipfs://', '')}" if "ipfs://" in uri else uri
    )
    response["image"] = format_ipfs_url(url=response["image"])

    name = utility_functions.format_nft_name(
        nft_metadata=response,
        contract_name=contract.functions.name().call(),
        token_id=token_id
    )

    return {
        "name": name,
        "address": contract_address,
        "token_id": token_id,
        "image": response["image"]
    }


def format_ipfs_url(url=None):
    if "https://" not in url and "ipfs" in url:
        return f"{constants.IPFS_BASE_URL}{url.replace('ipfs://', '')}"
    return url


def save_nft(nft_metadata=None):
    folder_name = utility_functions.format_folder_name(nft_name=nft_metadata["name"])
    nfts_folder = f"{os.getcwd()}/App/YourWallet/NFTs/{folder_name}"
    if os.path.isdir(nfts_folder) is False:
        os.mkdir(nfts_folder)

    extension = utility_functions.get_file_extension_from_url(url=nft_metadata["image"])

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    urllib.request.urlretrieve(
        nft_metadata["image"],
        f"App/YourWallet/NFTs/{folder_name}/{nft_metadata['name']}{extension}"
    )


def get_contract_name(contract_address=None, web3=None):
    contract = web3.eth.contract(address=contract_address, abi=constants.ERC20_ABI)
    return contract.functions.name().call()


def get_token_symbol(token_address=None, web3=None):
    contract = web3.eth.contract(address=token_address, abi=constants.ERC20_ABI)
    return contract.functions.symbol().call()


def get_token_decimals(token_address=None, web3=None):
    contract = web3.eth.contract(address=token_address, abi=constants.ERC20_ABI)
    return contract.functions.decimals().call()


def get_token_amount(token_address=None, user_address=None, web3=None):
    token = web3.eth.contract(address=token_address, abi=constants.ERC20_ABI)
    token_amount = token.functions.balanceOf(user_address).call()
    decimals = get_token_decimals(token_address=token_address, web3=web3)
    token_amount = utility_functions.format_balance(amount=token_amount, decimals=decimals)
    return token_amount


def get_eth_transactions(user_address=None):
    url = utility_functions.make_etherscan_api_url(
        module="account",
        action="txlist",
        address=user_address,
        startblock="0",
        endblock="latest",
        sort="desc",
        apikey=config.ETHERSCAN_API_KEY
    )
    return utility_functions.get_api_response(url=url)["result"]


def get_token_transactions(token_address=None, user_address=None):
    if token_address is None:
        return get_eth_transactions(user_address=user_address)
    else:
        url = utility_functions.make_etherscan_api_url(
            module="account",
            action="tokentx",
            contractaddress=token_address,
            address=user_address,
            startblock="0",
            endblock="latest",
            sort="desc",
            apikey=config.ETHERSCAN_API_KEY
        )
        return utility_functions.get_api_response(url=url)["result"]
