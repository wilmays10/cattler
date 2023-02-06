from django.core.exceptions import ValidationError
from django.test import TestCase
from random import randint
from rest_framework.test import APIClient
from rest_framework import status
import json

from feedlots.factories import AnimalFactory, TropaFactory, LoteFactory, CorralFactory


class FeedlotTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.lote = LoteFactory()
        self.tropa = TropaFactory(lote=self.lote)
        self.corral = CorralFactory(tropa=self.tropa)

    def test_animal(self):
        """
        Comprueba el método GET y POST del API de Animales
        :return:None
        """
        # Creo un objeto animal
        response = self.client.post(
            "/feedlots/api/animales/", {
                "tropa": self.tropa.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Creo un objeto animal
        response = self.client.post(
            "/feedlots/api/animales/", {
                "tropa": self.tropa.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Compruebo que se hayan creado los 2 objetos anteriores
        response = self.client.get("/feedlots/api/animales/")
        result = json.loads(response.content)
        self.assertEqual(len(result), 2)

    def test_tropa(self):
        """
        Comprueba los métodos GET y POST del API de Tropa
        :return: None
        """
        # Creo un objeto tropa
        response = self.client.post(
            "/feedlots/api/tropas/", {
                "numero": randint(100, 150),
                "lote": self.lote.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Creo un objeto tropa
        response = self.client.post(
            "/feedlots/api/tropas/", {
                "numero": randint(150, 200),
                "lote": self.lote.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get("/feedlots/api/tropas/")
        result = json.loads(response.content)

        # Existe una tropa creada en el setUp
        self.assertEqual(len(result), 3)

    def test_fail_tropa(self):
        """
        Comprueba que el número de una tropa debe ser único dentro de su lote
        :return: None
        """
        # Creo un objeto tropa con el numero de un obj tropa existente pero distinto lote
        response = self.client.post(
            "/feedlots/api/tropas/", {
                "numero": self.tropa.numero,
                "lote": LoteFactory().id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Creo un objeto tropa con un numero nuevo pero mismo lote
        response = self.client.post(
            "/feedlots/api/tropas/", {
                "numero": randint(100, 200),
                "lote": LoteFactory().id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with self.assertRaises(ValidationError) as context:
            # Creo un objeto tropa con numero existente en el lote
            response = self.client.post(
                "/feedlots/api/tropas/", {
                    "numero": self.tropa.numero,
                    "lote": self.lote.id
                }
            )
        self.assertTrue("numero de tropa ya existe en el lote" in str(context.exception))

    def test_lote(self):
        """
        Comprueba los métodos GET y POST del API de Lote
        :return: None
        """
        # Creo un objeto Lote
        response = self.client.post(
            "/feedlots/api/lotes/", {
                "numero": randint(10, 100),
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get("/feedlots/api/lotes/")
        result = json.loads(response.content)

        # Existe un lote creado en el setUp
        self.assertEqual(len(result), 2)

    def test_corral(self):
        """
        Comprueba los métodos GET y POST del API de Corral
        :return: None
        """
        # Creo un objeto Lote
        response = self.client.post(
            "/feedlots/api/corrales/", {
                "numero": randint(10, 100),
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get("/feedlots/api/corrales/")
        result = json.loads(response.content)

        # Existe un corral creado en el setUp
        self.assertEqual(len(result), 2)

    def test_registro(self):
        """
        Comprueba el funcionamiento del API de registro
        :return: None
        """
        corral_1 = CorralFactory(tropa=None)
        corral_2 = CorralFactory(tropa=None)
        lote = LoteFactory()
        lote_1 = LoteFactory()
        response = self.client.post(
            "/feedlots/api/registro", {
                "lote": self.lote.numero,
                "ingresos":[
                    {
                        "corral": corral_1.numero,
                        "cantidad": 50
                    },
                    {
                        "corral": corral_2.numero,
                        "cantidad": 30
                    }
                ]
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ingreso datos a un corral inexistente
        response = self.client.post(
            "/feedlots/api/registro", {
                "lote": lote.numero,
                "ingresos":[
                    {
                        "corral": randint(100, 110),
                        "cantidad": 10
                    },
                ]
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get("/feedlots/api/animales/")

        # Ingreso datos a un corral no vacío
        response = self.client.post(
            "/feedlots/api/registro", {
                "lote": lote_1.numero,
                "ingresos":[
                    {
                        "corral": self.corral.numero,
                        "cantidad": 10
                    },
                ]
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
