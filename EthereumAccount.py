
class EthereumAccount:

    def __init__(self, web3=None, account=None, **kwargs):
        self.web3 = web3
        self.account = account

    def get_balance(self, unit=None):
        return self.web3.fromWei(self.web3.eth.get_balance(self.account.address), unit)  # unit = (esempio: "ether")
