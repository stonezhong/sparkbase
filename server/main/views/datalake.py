from rest_framework import viewsets
from main.models import DataLake
from main.serializers import DataLakeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db import transaction
from rest_framework.response import Response

from main.api_input import json_to_model, CreateDataLakeInput

class DataLakeViewSet(viewsets.ModelViewSet):
    queryset = DataLake.objects.all()
    serializer_class = DataLakeSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = []
    ordering_fields = []

    @transaction.atomic
    def create(self, request):
        """
        Create a datalake
        """

        create_datalake_input = CreateDataLakeInput.from_json(request.data)

        datalake = DataLake.create(
            request.user,
            create_datalake_input.name,
            create_datalake_input.description,
            create_datalake_input.config
        )
        response = DataLakeSerializer(instance=datalake).data
        return Response(response)
