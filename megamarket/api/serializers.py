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


class ParentField(serializers.UUIDField):
    def to_representation(self, value):
        if self.uuid_format == 'hex_verbose':
            return value.id
        else:
            return getattr(value, self.uuid_format)


class CategoryOrOfferListSerializer(serializers.ListSerializer):
    def validate(self, data):
        ids = [item['id'] for item in data]
        parent_ids = [item['parent'] for item in data
                      if item['parent'] is not None]

        for parent_id in parent_ids:
            if not CategoryOrOffer.objects.filter(
                id=parent_id
            ).exists() and parent_id not in ids:
                raise serializers.ValidationError(
                    "Parent id must correspond to an object"
                )

        return data

    def create(self, validated_data):
        fields_to_update = [
            'name', 'parent',
            'price', 'type', 'date'
        ]

        obj_list = []

        for item in validated_data:
            parent_id = item['parent']

            if parent_id is not None:

                # parent_id in already existing objects
                parent = CategoryOrOffer.objects.filter(
                    id=parent_id
                ).first()

                # suppose that parent is in current list
                if parent is None:
                    # find object in list
                    parent = [
                        obj for obj in obj_list if obj.id == parent_id
                    ][0]

            else:
                parent = None

            is_initial_object = True

            while parent is not None:
                parent.date = item['date']
                if is_initial_object:  # update dict
                    is_initial_object = False
                    item['parent'] = parent

                # add parent object to update list
                obj_list.append(parent)
                parent = parent.parent

            obj_list.append(
                CategoryOrOffer(**item)
            )

            # change validation data dict back
            item['parent'] = parent_id

        return CategoryOrOffer.objects.bulk_update_or_create(
            obj_list, fields_to_update, match_field='id'
        )


class CategoryOrOfferSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    parentId = ParentField(
        source='parent',
        allow_null=True,
        default=None
    )
    price = serializers.IntegerField(required=False, default=None)
    type = serializers.ChoiceField(choices=TYPE_CHOICES)
    date = CustomDateTimeField()
    children = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CategoryOrOffer
        fields = ('id', 'name', 'parentId',
                  'price', 'type', 'date', 'children')
        list_serializer_class = CategoryOrOfferListSerializer

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
