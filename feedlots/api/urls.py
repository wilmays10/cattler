from django.urls import path, include
from rest_framework import routers

from feedlots.api.views import (
    AnimalViewSet,
    TropaViewSet,
    CorralViewSet,
    LoteViewSet,
    registro
)


router = routers.DefaultRouter()
router.register("animales", AnimalViewSet, basename="animal.api.animales")
router.register("tropas", TropaViewSet, basename="animal.api.tropas")
router.register("corrales", CorralViewSet, basename="animal.api.corrales")
router.register("lotes", LoteViewSet, basename="animal.api.lotes")

urlpatterns = [
    path("", include(router.urls)),
    path("registro", registro, name="registro")
]
