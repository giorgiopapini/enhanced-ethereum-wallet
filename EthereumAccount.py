import time
import constants
import eth_generic_functions


class EthereumAccount:

    def __init__(self, web3=None, account=None, **kwargs):
        self.web3 = web3
        self.account = account
        self.account_path = f"App/Accounts/{self.account.address}"

    def get_balance(self, unit=None):
        return self.web3.fromWei(self.web3.eth.get_balance(self.account.address), unit)  # unit = (esempio: "ether")

    def send_ether(self, receiver_addr=None, amount_in_eth=None):
        priv_key = self.account.privateKey.hex()
        nonce = self.web3.eth.getTransactionCount(self.account.address)
        current_gas_price = eth_generic_functions.get_eth_gas_prices()["SafeGasPrice"]

        tx = {
            "nonce": nonce,
            "to": self.web3.toChecksumAddress(receiver_addr),
            "value": self.web3.toWei(amount_in_eth, "ether"),
            "gas": 21000,
            "gasPrice": self.web3.toWei(current_gas_price, 'gwei')
        }

        signed_tx = self.web3.eth.account.signTransaction(tx, priv_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    def send_erc20_token(self, erc20_address=None, receiver_addr=None, amount=None):
        priv_key = self.account.privateKey.hex()
        nonce = self.web3.eth.getTransactionCount(self.account.address)
        current_gas_price = eth_generic_functions.get_eth_gas_prices()["SafeGasPrice"]
        decimals = eth_generic_functions.get_token_decimals(token_address=erc20_address, web3=self.web3)

        contract = self.web3.eth.contract(address=erc20_address, abi=constants.ERC20_ABI)
        erc20_tx = contract.functions.transfer(
            receiver_addr,
            int(float(amount) * (10 ** decimals))
        ).buildTransaction(
            {
                "chainId": constants.GOERLI_CHAIN_ID,
                "nonce": nonce,
                "gas": 200000,  # How to dynamically regulate the gas limit?
                "gasPrice": self.web3.toWei(current_gas_price, 'gwei')
            }
        )

        signed_tx = self.web3.eth.account.signTransaction(erc20_tx, priv_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    def send_ERC721(self, contract_address=None, sender=None, receiver=None, token_id=None):
        contract = self.web3.eth.contract(address=self.web3.toChecksumAddress(contract_address), abi=constants.ERC721_ABI)
        nonce = self.web3.eth.getTransactionCount(self.account.address)
        current_gas_price = eth_generic_functions.get_eth_gas_prices()["SafeGasPrice"]

        from_address = self.web3.toChecksumAddress(sender)
        to_address = self.web3.toChecksumAddress(receiver)

        mint_txn = contract.functions.transferFrom(from_address, to_address, int(token_id)).buildTransaction(
            {
                "chainId": constants.GOERLI_CHAIN_ID,
                "nonce": nonce,
                "from": from_address,
                "gas": 1000000,
                "gasPrice": self.web3.toWei(current_gas_price, 'gwei')
            }
        )

        signed_tx = self.web3.eth.account.sign_transaction(mint_txn, private_key=self.account.privateKey.hex())
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    def swap_eth_for_token(self, amount_in_eth=None, token_address=None):
        contract = self.web3.eth.contract(address=constants.UNISWAP_V2_ROUTER_ADDRESS, abi=constants.UNISWAP_V2_ROUTER_ABI)
        nonce = self.web3.eth.getTransactionCount(self.account.address)
        current_gas_price = eth_generic_functions.get_eth_gas_prices()["SafeGasPrice"]

        weth_address_checksum = self.web3.toChecksumAddress(constants.WETH_ADDRESS)
        token_address_checksum = self.web3.toChecksumAddress(token_address)

        swap_txn = contract.functions.swapExactETHForTokens(
            0,
            [weth_address_checksum, token_address_checksum],
            self.web3.toChecksumAddress(self.account.address),
            int(time.time()) + (60 * 1000)
        ).buildTransaction(
            {
                "nonce": nonce,
                "from": self.web3.toChecksumAddress(self.account.address),
                "value": self.web3.toWei(amount_in_eth, "ether"),
                "gas": 1000000,
                "gasPrice": self.web3.toWei(current_gas_price, 'gwei')
            }
        )

        signed_tx = self.web3.eth.account.sign_transaction(swap_txn, private_key=self.account.privateKey.hex())
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    def swap_token_for_eth(self, amount, token_address=None):
        contract = self.web3.eth.contract(address=constants.UNISWAP_V2_ROUTER_ADDRESS, abi=constants.UNISWAP_V2_ROUTER_ABI)
        nonce = self.web3.eth.getTransactionCount(self.account.address)
        current_gas_price = eth_generic_functions.get_eth_gas_prices()["SafeGasPrice"]
        decimals = eth_generic_functions.get_token_decimals(token_address=token_address, web3=self.web3)

        weth_address_checksum = self.web3.toChecksumAddress(constants.WETH_ADDRESS)
        token_address_checksum = self.web3.toChecksumAddress(token_address)

        swap_txn = contract.functions.swapExactTokensForETH(
            int(float(amount) * (10 ** decimals)),
            0,
            [token_address_checksum, weth_address_checksum],
            self.web3.toChecksumAddress(self.account.address),
            int(time.time()) + (60 * 1000)
        ).buildTransaction(
            {
                "nonce": nonce,
                "from": self.web3.toChecksumAddress(self.account.address),
                "value": 0,
                "gas": 2000000,
                "gasPrice": self.web3.toWei(current_gas_price, 'gwei')
            }
        )

        signed_tx = self.web3.eth.account.sign_transaction(swap_txn, private_key=self.account.privateKey.hex())
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    def swap_token_for_token(self, amount=None, from_token_address=None, to_token_address=None):
        contract = self.web3.eth.contract(address=constants.UNISWAP_V2_ROUTER_ADDRESS, abi=constants.UNISWAP_V2_ROUTER_ABI)
        nonce = self.web3.eth.getTransactionCount(self.account.address)
        current_gas_price = eth_generic_functions.get_eth_gas_prices()["SafeGasPrice"]

        from_token_decimals = eth_generic_functions.get_token_decimals(token_address=from_token_address, web3=self.web3)

        from_address_checksum = self.web3.toChecksumAddress(from_token_address)
        to_address_checksum = self.web3.toChecksumAddress(to_token_address)

        swap_txn = contract.functions.swapExactTokensForTokens(
            int(float(amount) * (10 ** from_token_decimals)),
            0,
            [from_address_checksum, to_address_checksum],
            self.web3.toChecksumAddress(self.account.address),
            int(time.time()) + (60 * 1000)
        ).buildTransaction(
            {
                "nonce": nonce,
                "from": self.web3.toChecksumAddress(self.account.address),
                "value": 0,
                "gas": 2000000,
                "gasPrice": self.web3.toWei(current_gas_price, 'gwei')
            }
        )

        signed_tx = self.web3.eth.account.sign_transaction(swap_txn, private_key=self.account.privateKey.hex())
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    def approve_token(self, token_address=None, amount=None):
        erc20_token = self.web3.eth.contract(address=token_address, abi=constants.ERC20_ABI)
        nonce = self.web3.eth.getTransactionCount(self.account.address)
        current_gas_price = eth_generic_functions.get_eth_gas_prices()["SafeGasPrice"]
        decimals = eth_generic_functions.get_token_decimals(token_address=token_address, web3=self.web3)

        approve_txn = erc20_token.functions.approve(
            constants.UNISWAP_V2_ROUTER_ADDRESS,
            int(float(amount) * (10 ** decimals))
        ).buildTransaction(
            {
                "nonce": nonce,
                "from": self.account.address,
                "value": 0,
                "gas": 2000000,
                "gasPrice": self.web3.toWei(current_gas_price, 'gwei')
            }
        )

        signed_tx = self.web3.eth.account.sign_transaction(approve_txn, private_key=self.account.privateKey.hex())
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(tx_hash.hex())

    def token_transfer_approved(self, token_address=None, user_address=None, amount=0):
        token_allowance = eth_generic_functions.get_token_allowance(
            token_address=self.web3.toChecksumAddress(token_address),
            user_address=self.web3.toChecksumAddress(user_address),
            web3=self.web3
        )

        decimals = eth_generic_functions.get_token_decimals(
            token_address=self.web3.toChecksumAddress(token_address),
            web3=self.web3
        )

        if token_allowance >= int(float(amount) * (10 ** decimals)):
            return True
        else:
            return False

    def user_has_enough_erc20(self, erc20_address=None, amount=0):
        real_amount = eth_generic_functions.get_basic_token_amount(
            token_address=erc20_address,
            user_address=self.account.address,
            web3=self.web3
        )
        decimals = eth_generic_functions.get_token_decimals(
            token_address=self.web3.toChecksumAddress(erc20_address),
            web3=self.web3
        )

        if real_amount >= int(float(amount) * (10 ** decimals)):
            return True
        else:
            return False
