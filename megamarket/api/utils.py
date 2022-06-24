import uuid

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

VALIDATION_FAIL_RESPONSE = Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                'code': 400,
                'message': 'Validation failed'
            }
        )


class Node:
    def __init__(self, parent=None, obj=None):
        self.parent = parent
        self.obj = obj
        self.children = []

    @property
    def type(self):
        return self.obj.type

    @property
    def price(self):
        return self.obj.price

    @property
    def avg_price(self):
        return self.obj.avg_price

    @avg_price.setter
    def avg_price(self, value):
        self.obj.avg_price = value

    @property
    def date(self):
        return self.obj.date

    @date.setter
    def date(self, value):
        self.obj.date = value


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {}
        response.data['code'] = response.status_code
        if response.data['code'] == 404:
            message = 'Item not found'
        else:
            message = 'Validation failed'
        response.data['message'] = message

    return response


def is_valid_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def process_children(node, is_model_obj=False):
    prices = []
    latest_date = None

    if is_model_obj:
        children = node.children.all()
    else:
        children = node.children

    for child in children:
        if child.type == 'OFFER':
            prices.append(child.price)
            if not latest_date or child.date > latest_date:
                latest_date = child.date

            child.avg_price = child.price
        else:
            new_prices, new_date = process_children(child, is_model_obj)
            prices += new_prices

            if not latest_date or new_date > latest_date:
                latest_date = new_date

    node.avg_price = int(sum(prices) / len(prices)) if prices else None

    if latest_date is None:
        latest_date = node.date

    node.date = latest_date

    if is_model_obj:
        node.save()

    return prices, latest_date


def process_siblings(siblings):
    added_siblings = list(siblings)  # children of siblings

    for sibling in siblings:
        added_siblings += list(process_siblings(sibling.children.all()))

    return added_siblings
