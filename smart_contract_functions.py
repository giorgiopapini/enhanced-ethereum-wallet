import constants


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
