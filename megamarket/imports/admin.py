from django.contrib import admin

from .models import CategoryOrOffer


class CategoryOrOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'price', 'date', 'type')
    list_filter = ('type', )


admin.site.register(CategoryOrOffer, CategoryOrOfferAdmin)
