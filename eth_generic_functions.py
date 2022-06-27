import constants
import config

import utility_functions


def get_nft_owner(nft_address=None, nft_id=None, user_address=None, web3=None):
    contract = web3.eth.contract(address=nft_address, abi=constants.ERC721_ABI)
    nft_owner = web3.toChecksumAddress(contract.functions.ownerOf(nft_id).call())
    if web3.toChecksumAddress(user_address) is nft_owner:
        return True
    return False


def send_ERC721(web3=None, contract_address=None, sender=None, receiver=None, token_id=None):
    contract = web3.eth.contract(address=contract_address, abi=constants.ERC721_ABI)
    print(web3.toChecksumAddress(sender))
    tx_hash = contract.functions.transferFrom(
        web3.toChecksumAddress(sender),
        web3.toChecksumAddress(receiver),
        int(token_id)
    ).transact()


def get_nft_metadata(contract_address=None, web3=None, token_id=None):
    contract = web3.eth.contract(address=contract_address, abi=constants.ERC721_ABI)
    uri = contract.functions.tokenURI(token_id).call()
    response = utility_functions.get_api_response(
        url=f"{constants.IPFS_BASE_URL}{uri.replace('ipfs://', '')}" if "ipfs://" in uri else uri
    )

    image_url = None
    for attr in response:
        if "image" in attr:
            image_url = response[attr]
            break

    image_url = format_ipfs_url(url=image_url)

    name = utility_functions.format_nft_name(
        nft_metadata=response,
        contract_name=contract.functions.name().call(),
        token_id=token_id
    )

    return {
        "name": name,
        "address": contract_address,
        "token_id": token_id,
        "image": image_url
    }


def format_ipfs_url(url=None):
    if "https://" not in url and "ipfs" in url:
        return f"{constants.IPFS_BASE_URL}{url.replace('ipfs://', '')}"
    return url


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
        )
        return utility_functions.get_api_response(url=url)["result"]


def get_coin_price_data(coin_id=None, to="usd", days=1, interval=None):
    if coin_id is not None:
        url = utility_functions.make_coingecko_coins_api_url(
            coin_id=coin_id,
            action="market_chart",
            vs_currency=to,
            days=days,
            interval=interval
        )
        print(url)
        return utility_functions.get_api_response(url=url)


def get_eth_gas_prices():
    url = utility_functions.make_etherscan_api_url(
        base_url=constants.ETHERSCAN_BASE_MAINNET_API_URL,
        module="gastracker",
        action="gasoracle",
    )
    return utility_functions.get_api_response(url=url)["result"]


def get_transaction_status(tx_hash):
    url = utility_functions.make_etherscan_api_url(
        module="transaction",
        action="gettxreceiptstatus",
        txhash=tx_hash
    )
    return "Confirmed" if utility_functions.get_api_response(url=url)['result']['status'] is '1' else "Cancelled"
