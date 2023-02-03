from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from feedlots.api.serializers import (
    AnimalSerializer,
    TropaSerializer,
    CorralSerializer,
    LoteSerializer,
)
from feedlots.models import Animal, Tropa, Corral, Lote


class AnimalViewSet(viewsets.ModelViewSet):
    """
    Animales dentro de un feedlot. Se puede agregar, borrar o modificar
    dependiendo del método http usado. No se necesita autenticación.
    """

    serializer_class = AnimalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["tropa__numero"]
    queryset = Animal.objects.all()


class TropaViewSet(viewsets.ModelViewSet):
    """
    Tropas dentro de un feedlot. Se puede agregar, borrar o modificar
    dependiendo del método http usado. No se necesita autenticación.
    """

    serializer_class = TropaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["lote__numero"]
    queryset = Tropa.objects.all()


class CorralViewSet(viewsets.ModelViewSet):
    """
    Corrales de un feedlot. Se puede agregar, borrar o modificar
    dependiendo del método http usado. No se necesita autenticación.
    """

    serializer_class = CorralSerializer
    queryset = Corral.objects.all()


class LoteViewSet(viewsets.ModelViewSet):
    """
    Lotes en un feedlot. Se puede agregar, borrar o modificar
    dependiendo del método http usado. No se necesita autenticación.
    """

    serializer_class = LoteSerializer
    queryset = Lote.objects.all()
