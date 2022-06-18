from datetime import datetime
from imports.models import CategoryOrOffer, TYPE_CHOICES
from rest_framework import serializers


ISO_FORMAT = '%Y-%m-%dT%H:%M:%S%z'


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        value = super().to_representation(value)
        value = datetime.strptime(value, ISO_FORMAT)
        value = value.isoformat(timespec='milliseconds')
        if value.endswith('+00:00'):
            value = value[:-6] + 'Z'
        return value


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
    date = CustomDateTimeField()
    children = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CategoryOrOffer
        fields = ('id', 'name', 'parentId',
                  'price', 'type', 'date', 'children')

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

        # update date of parents
        parent = validated_data['parent']
        while parent is not None:
            parent.date = validated_data['date']
            parent.save(update_fields=['date'])
            parent = parent.parent

        obj, _ = CategoryOrOffer.objects.update_or_create(
            id=id,
            defaults=validated_data
        )
        return obj

    def get_children(self, obj):
        if obj.children.exists():
            return CategoryOrOfferSerializer(
                obj.children.all(),
                many=True
            ).data
        else:
            return None


class DummySerializer(serializers.Serializer):
    pass


class ImportSerializer(serializers.Serializer):
    items = DummySerializer(many=True)
    updateDate = serializers.DateTimeField()
