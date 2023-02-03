from rest_framework import serializers

from feedlots.models import Animal, Tropa, Corral, Lote


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = "__all__"


class TropaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tropa
        fields = "__all__"


class CorralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corral
        fields = "__all__"


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = "__all__"
