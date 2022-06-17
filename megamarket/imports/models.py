import uuid
from django.db import models


TYPE_CHOICES = [
    ('OFFER', 'Offer'),
    ('CATEGORY', 'Category')
]


class CategoryOrOffer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Name', max_length=50)
    date = models.DateTimeField('Update date')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    price = models.IntegerField('Price', null=True)
    type = models.CharField('Type', choices=TYPE_CHOICES, max_length=50)
