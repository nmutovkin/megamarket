from django.http import Http404
from imports.models import CategoryOrOffer
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.response import Response

from .serializers import CategoryOrOfferSerializer, ImportSerializer
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
    serializer_class = CategoryOrOfferSerializer

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
        if data['type'] == 'CATEGORY':
            process_children(data)

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
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
