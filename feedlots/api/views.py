from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from feedlots.api.serializers import (
    AnimalSerializer,
    TropaSerializer,
    CorralSerializer,
    LoteSerializer,
    RegistroSerializer
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


@api_view(['POST'])
def registro(request):
    """
    Servicio de ingreso de animales. El lote ya debe existir en la base de datos.
    El corral al cuál se ingresan los animales debe existir y estar vacío.
    :return: response(msg, status)
    """
    serializer = RegistroSerializer(data=request.data)
    message = "Datos cargados correctamente. "
    status_num = status.HTTP_201_CREATED
    if serializer.is_valid():
        try:
            num_lote = serializer.validated_data['lote']
            lote = Lote.objects.get(numero=num_lote)

        except ObjectDoesNotExist:
            return Response({"message": f'Lote numero {num_lote} inexistente.'},
                            status=status.HTTP_400_BAD_REQUEST)

        ingresos = serializer.validated_data['ingresos']
        try:
            for index, ingreso in enumerate(ingresos, 1):
                num_corral = ingreso['corral']
                corral = Corral.objects.get(numero=num_corral)
                if corral.es_vacio():
                    tropa = Tropa.objects.create(numero=index, lote=lote)
                    corral.tropa = tropa
                    corral.save()
                    for i in range(ingreso['cantidad']):
                        animal = Animal.objects.create(tropa=tropa)
                else:
                    message = f"Corral {num_corral} no vacío. No se cargaron sus datos. "
                    status_num = status.HTTP_200_OK

        except ObjectDoesNotExist:
            message = f"Corral numero {num_corral} inexistente."
            status_num = status.HTTP_200_OK

    else:
        message = serializer.errors
        status_num = status.HTTP_400_BAD_REQUEST

    return Response({"message": message}, status_num)