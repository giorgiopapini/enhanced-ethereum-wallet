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
            int(int(amount) * (10 ** decimals))
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
