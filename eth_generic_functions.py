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
    url = (f"{constants.ETHERSCAN_BASE_API_URL}"
           f"module=account&"
           f"action=txlist&"
           f"address={user_address}&"
           f"startblock=0&"
           f"endblock=latest&"
           f"sort=desc&"
           f"apikey={config.ETHERSCAN_API_KEY}")
    return utility_functions.get_api_response(url=url)


def get_token_transactions(token_address=None, user_address=None):
    if token_address is None:
        return get_eth_transactions(user_address=user_address)
    else:
        url = (f"{constants.ETHERSCAN_BASE_API_URL}"
               f"module=account&"
               f"action=tokentx&"
               f"contractaddress={token_address}&"
               f"address={user_address}&"
               f"startblock=0&"
               f"endblock=latest&"
               f"sort=desc&"
               f"apikey={config.ETHERSCAN_API_KEY}")
        return utility_functions.get_api_response(url=url)
