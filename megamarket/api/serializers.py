from datetime import datetime

from imports.models import TYPE_CHOICES, CategoryOrOffer
from rest_framework import serializers
from simple_history.utils import (bulk_create_with_history,
                                  bulk_update_with_history)

from .utils import Node, process_children, process_siblings

ISO_FORMAT = '%Y-%m-%dT%H:%M:%S%z'


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        value = super().to_representation(value)
        value = datetime.strptime(value, ISO_FORMAT)
        value = value.isoformat(timespec='milliseconds')
        if value.endswith('+00:00'):
            return value[:-6] + 'Z'
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
            'price', 'type', 'date', 'avg_price'
        ]

        obj_list = []
        parent_ids = []
        root_nodes = []
        ids = []
        relatives_obj_list = []
        relatives_parent_ids = []

        # set object list to update and update date
        for item in validated_data:
            parent_id = item['parent']
            ids.append(item['id'])

            if parent_id is not None:

                # parent_id in already existing object
                # or None
                parent = CategoryOrOffer.objects.filter(
                    id=parent_id
                ).first()

            else:
                parent = None

            item['parent'] = parent
            obj_list.append(CategoryOrOffer(**item))

            # change validation data dict back
            item['parent'] = parent_id

            parent_ids.append(parent_id)

            while parent is not None:
                if parent.id in ids:
                    break  # already processed this node

                ids.append(parent.id)

                # get siblings (excluding itself)
                siblings = parent.children.exclude(id=obj_list[-1].id)

                # get children of siblings
                full_siblings = process_siblings(siblings)
                full_parent_ids = [sibling.parent.id for sibling
                                   in full_siblings]

                relatives_obj_list += full_siblings
                relatives_parent_ids += full_parent_ids

                # add parent object to update list
                obj_list.append(parent)
                parent = parent.parent

                if parent is None:
                    parent_ids.append(None)
                else:
                    parent_ids.append(parent.id)

        # set a lookup dictionary
        lookup = {}
        full_obj_list = obj_list + relatives_obj_list
        full_parent_ids = parent_ids + relatives_parent_ids

        for obj, parent_id in zip(full_obj_list, full_parent_ids):
            lookup[obj.id] = (Node(obj=obj), parent_id)

        # set parents
        for _, (node, parent_id) in lookup.items():

            proposed_node_parent = Node()

            if parent_id is not None and parent_id in lookup:
                if node.obj.parent is None:
                    node.obj.parent = lookup[parent_id][0].obj
                proposed_node_parent = lookup[parent_id][0]
                proposed_node_parent.children.append(node)
                node.parent = proposed_node_parent

        # get root nodes
        root_nodes = [node[0] for (_, node) in lookup.items()
                      if node[0].parent is None]

        # set average prices
        for root_node in root_nodes:
            process_children(root_node)

        # sort for bulk updation or creation
        obj_list_to_update = []
        obj_list_to_create = []

        for obj in obj_list:
            if CategoryOrOffer.objects.filter(id=obj.id).exists():
                obj_list_to_update.append(obj)
            else:
                obj_list_to_create.append(obj)

        updated_objs = bulk_update_with_history(
            obj_list_to_update, CategoryOrOffer, fields_to_update
        )

        created_objs = bulk_create_with_history(
            obj_list_to_create, CategoryOrOffer
        )

        objs_to_return = []

        if created_objs:
            objs_to_return += created_objs

        if updated_objs:
            objs_to_return += updated_objs

        return objs_to_return


class CategoryOrOfferSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    parentId = ParentField(  # noqa
        source='parent',
        allow_null=True,
        default=None
    )
    price = serializers.IntegerField(required=False, default=None)
    type = serializers.ChoiceField(choices=TYPE_CHOICES)
    date = CustomDateTimeField()

    class Meta:
        model = CategoryOrOffer
        fields = ('id', 'name', 'parentId',
                  'price', 'type', 'date')
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


class NodeCategoryOrOfferSerializer(CategoryOrOfferSerializer):
    price = serializers.IntegerField(source='avg_price')
    children = serializers.SerializerMethodField(read_only=True)

    def get_children(self, obj):
        if obj.children.exists():
            return NodeCategoryOrOfferSerializer(
                obj.children.all(),
                many=True
            ).data
        else:
            return None

    class Meta(CategoryOrOfferSerializer.Meta):
        fields = ('id', 'name', 'parentId',
                  'price', 'type', 'date', 'children')


class SalesCategoryOrOfferSerializer(NodeCategoryOrOfferSerializer):
    children = None

    class Meta(NodeCategoryOrOfferSerializer.Meta):
        fields = ('id', 'name', 'parentId',
                  'price', 'type', 'date')


class DummySerializer(serializers.Serializer):
    pass


class ImportSerializer(serializers.Serializer):
    items = DummySerializer(many=True)
    updateDate = serializers.DateTimeField()  # noqa


class ToDateSerializer(serializers.Serializer):
    date = CustomDateTimeField()


class DateRangeSerializer(serializers.Serializer):
    dateStart = CustomDateTimeField(required=False)  # noqa
    dateEnd = CustomDateTimeField(required=False)  # noqa
