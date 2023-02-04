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
    serializer = RegistroSerializer(data=request.data)
    message = ""
    if serializer.is_valid():
        try:
            num_lote = serializer.validated_data['lote']
            lote = Lote.objects.get(numero=num_lote)

        except ObjectDoesNotExist:
            return Response({"message": f'Lote numero {num_lote} inexistente.'},
                            status=status.HTTP_404_NOT_FOUND)

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
                    message += f"Corral {num_corral} no vacío. No se cargaron sus datos. "

        except ObjectDoesNotExist:
            return Response({"message": f"Corral numero {num_corral} inexistente."})

    else:
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    if not message:
        message = "Datos cargados correctamente."
    return Response({"message": message})