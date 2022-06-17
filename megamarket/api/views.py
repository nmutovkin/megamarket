from imports.models import CategoryOrOffer
from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import CategoryOrOfferSerializer, ImportSerializer


class ImportViewSet(viewsets.ModelViewSet):
    queryset = CategoryOrOffer.objects.all()
    serializer_class = CategoryOrOfferSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):

        # validate import serializer
        import_serializer = ImportSerializer(data=request.data)
        import_serializer.is_valid(raise_exception=True)

        # extract date
        date = request.data['updateDate']

        for item in request.data['items']:
            item['date'] = date

            # create or update data
            serializer = self.get_serializer(data=item)

            if serializer.is_valid():
                self.perform_create(serializer)
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(status=status.HTTP_200_OK)
