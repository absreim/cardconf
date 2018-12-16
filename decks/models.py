from django.db import models
from django.conf import settings
from cards.models import Edition


class Deck(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together: ("name", "user")


class CardsInDeck(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    edition = models.ForeignKey(Edition, on_delete=models.PROTECT)
    quantity = models.IntegerField()
