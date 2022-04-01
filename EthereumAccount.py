
class EthereumAccount:

    def __init__(self, web3=None, account=None, **kwargs):
        self.web3 = web3
        self.account = account
        self.balance = self.web3.eth.get_balance(self.account.address)

    def get_balance(self, unit=None):
        return self.web3.fromWei(self.balance, unit)  # unit = (esempio: "ether")
