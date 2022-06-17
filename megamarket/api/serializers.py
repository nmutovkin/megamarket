from imports.models import CategoryOrOffer, TYPE_CHOICES
from rest_framework import serializers


class CategoryOrOfferSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    parentId = serializers.PrimaryKeyRelatedField(
        source='parent',
        allow_null=True,
        default=None,
        queryset=CategoryOrOffer.objects.all()
    )
    price = serializers.IntegerField(required=False, default=None)
    type = serializers.ChoiceField(choices=TYPE_CHOICES)
    date = serializers.DateTimeField()

    class Meta:
        model = CategoryOrOffer
        fields = ('id', 'name', 'parentId', 'price', 'type', 'date')

    def validate(self, data):
        if data['type'] == 'OFFER' and 'price' not in data:
            raise serializers.ValidationError(
                'Price must be set for an offer.'
            )

        if 'price' in data and data['price'] and data['price'] < 0:
            raise serializers.ValidationError(
                'Price can\'t be negative'
            )

        return data

    def create(self, validated_data):
        id = validated_data.pop('id')
        obj, _ = CategoryOrOffer.objects.update_or_create(
            id=id,
            defaults=validated_data
        )
        return obj


class DummySerializer(serializers.Serializer):
    pass


class ImportSerializer(serializers.Serializer):
    items = DummySerializer(many=True)
    updateDate = serializers.DateTimeField()
