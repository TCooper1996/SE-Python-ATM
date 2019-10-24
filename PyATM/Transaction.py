from .ATMCard import ATMCard
from .ATM import ATM
from .AccountExtension import AccountExtension
from datetime import date


class Transaction:

    def __init__(self, card_number: int, atm: ATM):
        self.card_number = card_number
        self.atm = atm
        self.date = date.today()

    def get_date(self):
        return self.date.strftime("%d/%m/%Y")


class CashTransfer(Transaction):
    def __init__(self, card_number: int, atm: ATM, receiving_account_number: int, receiving_name: str, amount_transferred: int):
        super(CashTransfer, self).__init__(card_number, atm)
        self.receiving_account_number = receiving_account_number
        self.receiving_account_name = receiving_name
        self.amount_transferred = amount_transferred


class BalanceEnquiry(Transaction):
    def __init__(self, card_number: int, atm: ATM):
        super(BalanceEnquiry, self).__init__(card_number, atm)


class CashWithdrawal(Transaction):
    def __init__(self, card_number: int, atm: ATM, amount_transferred: int, denomination: int, current_balance: float):
        super(CashWithdrawal, self).__init__(card_number, atm)
        self.amount_transferred = amount_transferred
        self.denomination = denomination
        self.current_balance = current_balance


class PinChange(Transaction):
    def __init__(self, card_number: int, atm: ATM, previous_pin: int, next_pin: int):
        super(PinChange, self).__init__(card_number, atm)
        self.previous_pin = previous_pin
        self.next_pin = next_pin


class PhoneNumber(Transaction):
    def __init__(self, card_number: int, atm: ATM, phone_number: int):
        super(PhoneNumber, self).__init__(card_number, atm)
        self.phone_number = phone_number
