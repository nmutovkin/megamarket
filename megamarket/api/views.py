from datetime import timedelta

from django.http import Http404
from imports.models import CategoryOrOffer
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (CategoryOrOfferSerializer, DateRangeSerializer,
                          ImportSerializer, NodeCategoryOrOfferSerializer,
                          SalesCategoryOrOfferSerializer, ToDateSerializer)
from .utils import VALIDATION_FAIL_RESPONSE, is_valid_uuid, process_children


class ImportViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CategoryOrOffer.objects.all()
    serializer_class = CategoryOrOfferSerializer

    def create(self, request, *args, **kwargs):

        # validate import serializer
        import_serializer = ImportSerializer(data=request.data)
        import_serializer.is_valid(raise_exception=True)

        # extract date
        date = request.data['updateDate']

        # update date
        for item in request.data['items']:
            item['date'] = date

        serializer = self.get_serializer(
            data=request.data['items'],
            many=True
        )

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return VALIDATION_FAIL_RESPONSE

        self.perform_create(serializer)
        return Response(status=status.HTTP_200_OK)


class NodeViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CategoryOrOffer.objects.all()
    serializer_class = NodeCategoryOrOfferSerializer

    def retrieve(self, request, *args, **kwargs):
        if not is_valid_uuid(self.kwargs['pk']):
            return VALIDATION_FAIL_RESPONSE

        try:
            instance = self.get_object()
        except Http404:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'code': 404,
                    'message': "Item not found"
                }
            )
        serializer = self.get_serializer(instance)

        data = serializer.data
        return Response(data)


class DeleteViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = CategoryOrOffer.objects.all()
    serializer_class = CategoryOrOfferSerializer

    def destroy(self, request, *args, **kwargs):
        if not is_valid_uuid(self.kwargs['pk']):
            return VALIDATION_FAIL_RESPONSE

        try:
            instance = self.get_object()
        except Http404:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'code': 404,
                    'message': "Item not found"
                }
            )

        root = instance
        parent = instance.parent

        # delete instance and its children
        self.perform_destroy(instance)

        # update average prices for parents and grandparents

        # get to the root
        while parent is not None:
            root = root.parent
            parent = parent.parent

        # update prices and date
        process_children(root, True)

        return Response(status=status.HTTP_200_OK)


class SalesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = CategoryOrOffer.objects.all()
    serializer_class = SalesCategoryOrOfferSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        to_date = self.to_date
        from_date = to_date - timedelta(days=1)

        return queryset.filter(
            date__gte=from_date,
            date__lte=to_date,
            type='OFFER'
        )

    def list(self, request, *args, **kwargs):
        query = ToDateSerializer(data=self.request.query_params)

        try:
            query.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return VALIDATION_FAIL_RESPONSE

        self.to_date = query.validated_data.get('date')

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({'items': serializer.data})


class StatisticsViewSet(viewsets.ModelViewSet):
    queryset = CategoryOrOffer.objects.all()
    serializer_class = SalesCategoryOrOfferSerializer

    @action(detail=True, methods=['get'])
    def statistic(self, request, pk=None):
        query = DateRangeSerializer(data=self.request.query_params)

        try:
            query.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return VALIDATION_FAIL_RESPONSE

        from_date = query.validated_data.get('dateStart', None)
        to_date = query.validated_data.get('dateEnd', None)

        entity = self.get_object()
        history = entity.history.all()

        if from_date:
            history = history.filter(
                date__gte=from_date
            )

        if to_date:
            history = history.filter(
                date__lte=to_date
            )

        history = history.distinct()

        serializer = self.get_serializer(history, many=True)

        return Response({'items': serializer.data})
