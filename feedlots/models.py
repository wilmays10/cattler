from django.db import models


class Lote(models.Model):
    numero_lote = models.IntegerField()

    def __str__(self):
        return self.numero_lote


class Corral(models.Model):
    numero_corral = models.PositiveIntegerField()

    def __str__(self):
        return self.numero_corral


class Tropa(models.Model):
    numero_tropa = models.IntegerField()
    lote = models.ForeignKey("Lote", on_delete=models.CASCADE)
    corral = models.ForeignKey(
        "Corral", null=True, blank=True, on_delete=models.SET_NULL
    )

    def validate_unique(self, *args, **kwargs):
        super().validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(
            numero_tropa=self.numero_tropa,
            lote__numero_lote=self.lote.numero_lote,
        ).exists():
            raise ValidationError(
                message="Tropa con (numero_tropa, numero_lote) ya existe.",
                code="unique_together",
            )

    def __str__(self):
        return f'Tropa {self.numero_tropa} - Lote {self.lote.numero_lote}'


class Animal(models.Model):
    numero_caravana = models.IntegerField(unique=True, null=True, blank=True)
    rfid = models.IntegerField(null=True, blank=True)
    tropa = models.ForeignKey("Tropa", on_delete=models.CASCADE)

    def __str__(self):
        return f'Animal {self.pk} - Tropa {self.tropa.numero_tropa}'
