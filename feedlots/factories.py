import factory
from feedlots.models import Animal, Tropa, Lote, Corral


class LoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lote

    numero = factory.Sequence(lambda  n: n)

class TropaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tropa

    numero = factory.Sequence(lambda  n: n)
    lote = factory.SubFactory(LoteFactory)

class CorralFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Corral

    numero = factory.Sequence(lambda  n: n+1)
    tropa = factory.SubFactory(TropaFactory)


class AnimalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Animal

    tropa = factory.SubFactory(TropaFactory)
