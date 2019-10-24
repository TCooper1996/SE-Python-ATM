import datetime
from .ATMCard import ATMCard
from .AccountExtension import AccountExtension
from .ATM import ATM


class Administrator:
    def __init__(self):
        self.transactions = []
        self.accounts = {}
        self.atm_cards = {}
        self.atms = {}

    def register_atm(self, id: int, location: str):
       self.atms[id] = ATM(id, location)

    def register_card(self, card_number: int, account_number: int, pin: int, account_name: str,
                      date_of_issue: datetime.datetime, expiry_date: datetime.datetime, address: str,
                      balance: float, phone_number: int, card_status):

        # Create new account if it doesn't already exist
        if account_number not in self.accounts.values():
            account = AccountExtension(card_number, account_name, phone_number, balance)
            self.accounts[account_number] = account

        card = ATMCard(card_number, account_number, pin, account_name, date_of_issue, expiry_date, address,
                       phone_number, card_status)

        self.atm_cards[card_number] = card

