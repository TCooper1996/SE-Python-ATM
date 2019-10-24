from datetime import date, timedelta
from random import randint


# Creates an ATM with random refill and maintenance dates
class ATM:

    def __init__(self, id, location: str):
        self.id = id
        self.current_balance = 500
        self.location = location
        self.minimum_balance = 20
        self.active = True
        self.last_refill_date = date.today() - timedelta(days=30*randint(2, 8))
        self.next_maintenance_date = date.today() + timedelta(days=30*randint(2, 8))
