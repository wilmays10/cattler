from django.core.exceptions import ValidationError
from django.db import models


class Lote(models.Model):
    numero = models.IntegerField()

    def __str__(self):
        return f'id {self.pk} - lote {self.numero}'


class Corral(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    tropa = models.OneToOneField(
        "Tropa", null=True, blank=True, on_delete=models.SET_NULL
    )

    def es_vacio(self):
        return not isinstance(self.tropa, Tropa)

    def __str__(self):
        return f'id {self.pk} - corral {self.numero}'


class Tropa(models.Model):
    numero = models.IntegerField()
    lote = models.ForeignKey("Lote", on_delete=models.CASCADE)

    def validate_unique(self, *args, **kwargs):
        super(Tropa, self).validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(
            numero=self.numero,
            lote__numero=self.lote.numero,
        ).exists():
            raise ValidationError(
                message=f"{self.numero} como numero de tropa ya existe en el lote {self.lote.numero}.",
                code="unique_together",
            )

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Tropa, self).save(*args, **kwargs)

    def __str__(self):
        return f'Tropa {self.numero} - Lote {self.lote.numero}'


class Animal(models.Model):
    numero_caravana = models.IntegerField(unique=True, null=True, blank=True)
    rfid = models.IntegerField(null=True, blank=True)
    tropa = models.ForeignKey("Tropa", on_delete=models.CASCADE)

    def __str__(self):
        return f'Animal {self.pk} - Tropa {self.tropa.numero}'
