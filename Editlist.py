class Editlist:

    def __init__(self):
        self.coinlist_action = ""
        self.coinlist = []
        self.edit = 0
        self.removable = ""
        self.main_list = ['Zilliqa', 'Band Protocol', 'Algorand', 'Theta Network', 'iExec RLC', 'Cosmos',
                          'DigiByte', 'Chiliz', 'Terra', 'Theta Fuel', 'Waves', 'Nano', 'IOST', 'Tezos',
                          'VeChain', 'DOT', 'Elrond', 'NEM', 'Filecoin', 'Bitcoin', 'Ethereum', 'Dogecoin',
                          'Ripple', 'Tron', 'Binance Coin', 'Cardano', 'Bitcoin Cash', 'EOS', 'GAS', 'NEO',
                          'Litecoin', 'Chainlink', 'Tether', 'Dash', 'Aave', 'Uniswap', 'True USD', 'USD Coin',
                          'Compound', '0x', 'AdEx', 'Augur', 'Bancor', 'Basic Attention Token', 'Civic', 'Enjin Coin',
                          'Fetch.ai', 'Golem', 'Kyber Network', 'Metal', 'OmiseGO', 'Paxos Standard Token', 'Power Ledger',
                          'DIA', 'Sushi', 'Quantstamp', 'Numeraire', 'yearn.finance', 'Dai', 'Loopring', 'AirSwap',
                          'Republic Protocol', 'Maker', 'QuarkChain', 'Swipe', 'Synthetix Network Token', 'Stellar',
                          'DFI.money', 'Ripio Credit Network', 'Status', 'Storj', 'aelf', 'district0x']

    def take_input(self):
        while 1:
            c = input("\nEnter New Coin or 'N' to Proceed: ")
            if c == "n":
                break
            else:
                if c in self.main_list and c not in self.coinlist:
                    self.coinlist.append(c)
                    c = ""
                elif c not in self.main_list:
                    print("\nInvalid Input!!!   Please check the spelling and enter Case sensitive input :)")
                    continue
                elif c in self.coinlist:
                    print("\nCoin Already Present")
                    continue
        self.send_price_to_file()

    def new_list(self):
        self.coinlist = []
        self.take_input()

    def add_coin(self):
        self.take_input()

    def remove_coin(self):
        print("\nCOIN LIST =>", *self.coinlist)
        while 1:
            self.removable = input("\nEnter coin name from the list to be removed or enter 'n' if done: ")
            if self.removable == 'n':
                break
            elif self.removable in self.coinlist:
                self.coinlist.remove(self.removable)
                print("\nCOIN LIST =>", *self.coinlist)
            else:
                continue
        self.send_price_to_file()

    def edit_list(self):
        print("\nCOIN LIST =>", *self.coinlist)
        while 1:
            self.coinlist_action = input("\nEnter 1 to add coin || 2 to remove coin || 3 to proceed: ")
            if self.coinlist_action == "1":
                self.add_coin()
            elif self.coinlist_action == "2":
                self.remove_coin()
            elif self.coinlist_action == "3":
                self.coinlist_action = ""
                break
        return self.coinlist

    def get_price_from_file(self):
        self.coin_record = open("coins.txt", "r")
        ls = self.coin_record.readlines()
        for item in ls:
            self.coinlist.append(item.strip())
        self.coin_record.close()
        print("\nCOIN LIST =>", *self.coinlist)
        return self.coinlist

    def send_price_to_file(self):
        self.coin_record = open("coins.txt", "w+")
        for item in self.coinlist:
            self.coin_record.write(item + '\n')
        self.coin_record.close()
