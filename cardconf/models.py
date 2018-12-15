from django.db import models
from django.conf import settings


class Color(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class SubType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    type = models.ManyToManyField(Type, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class CardName(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    rules_text = models.TextField(blank=True)
    power = models.CharField(max_length=10, blank=True)
    toughness = models.CharField(max_length=10, blank=True)
    cost = models.CharField(max_length=50)
    cmc = models.IntegerField()
    color = models.ManyToManyField(Color, on_delete=models.PROTECT, blank=True)
    type = models.ManyToManyField(Type, on_delete=models.PROTECT)
    subtype = models.ManyToManyField(SubType, on_delete=models.PROTECT, blank=True)

    def __str__(self):
        return self.name


class Block(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class Expansion(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    block = models.ForeignKey(Block, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.name


class Rarity(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name


class Edition(models.Model):
    card_name = models.ForeignKey(CardName, on_delete=models.PROTECT)
    expansion_name = models.ForeignKey(Expansion, on_delete=models.PROTECT)
    flavor_text = models.TextField(blank=True)
    rarity = models.ForeignKey(Rarity, on_delete=models.PROTECT)
    multiverse_id = models.IntegerField()

    def __str__(self):
        return "{0} - {1}".format(self.card_name, self.expansion_name)

    class Meta:
        unique_together = ("card_name", "expansion_name")


class Format(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class LegalityType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class CardLegality(models.Model):
    format = models.ForeignKey(Format, on_delete=models.PROTECT)
    card_name = models.ForeignKey(CardName, on_delete=models.PROTECT)
    legality = models.ForeignKey(LegalityType, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("card_name", "format")


class Deck(models.Model):
    name = models.CharField(max_length=200, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class CardsInDeck(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    edition = models.ForeignKey(Edition, on_delete=models.PROTECT)
    quantity = models.IntegerField()