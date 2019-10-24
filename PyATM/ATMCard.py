from datetime import date, timedelta

class ATMCard:

    def __init__(self, card_number: int, account_number: int, pin: int, name: str, date_of_issue, expiry_date,
                 address: str, phone_number: int, card_status):
        self.card_number = card_number
        self.account_number = account_number
        self.pin = pin
        self.name = name
        self.date_of_issue = date_of_issue
        self.expiry_date = expiry_date
        self.address = address
        self.phone_number = phone_number
        self.card_status = card_status

