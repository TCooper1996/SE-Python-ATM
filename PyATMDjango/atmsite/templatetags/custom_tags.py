from django import template
from ..models import Card

register = template.Library()


# Returns "checked" if the card is active, empty string otherwise.
# Used to generate a checkbox as active or not in manage_cards.html
@register.simple_tag
def sub_active(card_number):
    card_number = int(card_number)
    if Card.objects.get(card_number__exact=card_number).active:
        return "checked"
    else:
        return ""
