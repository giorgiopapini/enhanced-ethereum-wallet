import constants
import config

import utility_functions


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
    print(token.functions.balanceOf(user_address).call())
    return token.functions.balanceOf(user_address).call()


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
