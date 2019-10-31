from django.db.models.signals import pre_save
from django.dispatch import receiver
import hashlib

from .models import Account


@receiver(pre_save, sender=Account)
def set_hash(sender, **kwargs):
    print("Calling")
    kwargs['instance'].account_hash = hashlib.sha3_256(bytes(kwargs['instance'].username, 'utf-8')).hexdigest()
