import json

import constants
import config

import utility_functions
import urllib.request


def get_nft_image(contract_address=None, web3=None, token_id=None):
    contract = web3.eth.contract(address=contract_address, abi=constants.ERC721_ABI)
    uri = contract.functions.tokenURI(token_id).call()
    response = utility_functions.get_api_response(
        url=f"{constants.IPFS_BASE_URL}{uri.replace('ipfs://', '')}" if "ipfs" in uri else uri
    )

    urllib.request.urlretrieve(response["image"], f"App/YourWallet/NFTs/{contract_address}-{token_id}.png")

    add_nft_to_json(
        name=response["name"],
        address=contract_address,
        token_id=token_id,
        image_url=response["image"]
    )


def add_nft_to_json(name=None, address=None, token_id=None, image_url=None):
    with open("App/YourWallet/nfts.json", "r+") as file:
        nfts = json.load(file)
        nfts.append({"name": name, "address": address, "token_id": token_id, "image_url": image_url})
        nfts.sort(key=lambda x: x["name"])

        file.seek(0)
        json.dump(nfts, file)
        file.truncate()


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
