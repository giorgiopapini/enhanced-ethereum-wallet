import constants
import config

import utility_functions


def get_nft_owner(nft_address=None, nft_id=None, user_address=None, web3=None):
    contract = web3.eth.contract(address=web3.toChecksumAddress(nft_address), abi=constants.ERC721_ABI)
    nft_owner = web3.toChecksumAddress(contract.functions.ownerOf(int(nft_id)).call())
    if web3.toChecksumAddress(user_address) == web3.toChecksumAddress(nft_owner):
        return True
    return False


def get_nft_metadata(contract_address=None, web3=None, token_id=None):
    contract = web3.eth.contract(address=web3.toChecksumAddress(contract_address), abi=constants.ERC721_ABI)
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
    contract = web3.eth.contract(address=web3.toChecksumAddress(contract_address), abi=constants.ERC20_ABI)
    return contract.functions.name().call()


def get_token_symbol(token_address=None, web3=None):
    contract = web3.eth.contract(address=web3.toChecksumAddress(token_address), abi=constants.ERC20_ABI)
    return contract.functions.symbol().call()


def get_token_decimals(token_address=None, web3=None):
    contract = web3.eth.contract(address=web3.toChecksumAddress(token_address), abi=constants.ERC20_ABI)
    return contract.functions.decimals().call()


def get_basic_token_amount(token_address=None, user_address=None, web3=None):
    token = web3.eth.contract(address=web3.toChecksumAddress(token_address), abi=constants.ERC20_ABI)
    token_amount = token.functions.balanceOf(user_address).call()
    return token_amount


def get_token_amount(token_address=None, user_address=None, web3=None):
    token_amount = get_basic_token_amount(token_address=token_address, user_address=user_address, web3=web3)
    decimals = get_token_decimals(token_address=token_address, web3=web3)
    token_amount = utility_functions.format_balance(amount=token_amount, decimals=decimals)
    return token_amount


def get_token_allowance(token_address=None, user_address=None, web3=None):
    token = web3.eth.contract(address=web3.toChecksumAddress(token_address), abi=constants.ERC20_ABI)
    token_allowance = token.functions.allowance(user_address, constants.UNISWAP_V2_ROUTER_ADDRESS).call()
    return token_allowance


def uniswap_get_min_amount_in(path=None, web3=None):
    uniswap_router = web3.eth.contract(
        address=web3.toChecksumAddress(constants.UNISWAP_V2_ROUTER_ADDRESS),
        abi=constants.UNISWAP_V2_ROUTER_ABI
    )
    amounts_in = uniswap_router.functions.getAmountsIn(int(1), path).call()

    return amounts_in[0]


def uniswap_get_amounts_out(path=None, amount_in=None, web3=None):
    uniswap_router = web3.eth.contract(
        address=web3.toChecksumAddress(constants.UNISWAP_V2_ROUTER_ADDRESS),
        abi=constants.UNISWAP_V2_ROUTER_ABI
    )
    amounts_out = uniswap_router.functions.getAmountsOut(int(amount_in), path).call()

    return amounts_out


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
