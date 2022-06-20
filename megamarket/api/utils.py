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


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {}
        response.data['code'] = response.status_code
        response.data['message'] = 'Validation failed'

    return response


def is_valid_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def process_children(data):
    prices = []
    children = data['children'] or []

    for child in children:
        if child['type'] == 'OFFER':
            prices.append(child['price'])
        else:
            prices += process_children(child)

    data['price'] = int(sum(prices) / len(prices)) if prices else None
    return prices
