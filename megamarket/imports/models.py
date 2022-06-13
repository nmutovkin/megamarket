import uuid
from django.db import models


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Name', max_length=50)
    date = models.DateTimeField('Update date')


class Offer(Category):
    price = models.IntegerField('Price')
