from django import template


register = template.Library()


@register.filter
def add_variables(value, value2):
    """Allows to update existing variable in template"""
    return value+value2


@register.filter
def sum_of_elements(value):
    sum_q = 0
    print(value.storage_items.all())
    for i in value.storage_items.all():
        sum_q += i.item_quantity
        # print(i.item_quantity)
    return sum_q


@register.filter
def is_item_deleted(value):
    print(value.storage_to)
    if str(value.storage_to) == "DELETED":
        print("true")
        return True
    else:
        return False


