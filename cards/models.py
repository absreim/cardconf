from django.db import models

class Color(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name


class Layout(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class SuperType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class SubType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class CardName(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    layout = models.ForeignKey(Layout, on_delete=models.PROTECT)
    rules_text = models.TextField(blank=True)
    power = models.CharField(max_length=10, blank=True)
    toughness = models.CharField(max_length=10, blank=True)
    cost = models.CharField(max_length=50)
    cmc = models.IntegerField()
    loyalty = models.CharField(max_length=10)
    color = models.ManyToManyField(Color, blank=True)
    color_identity = models.ManyToManyField(Color, blank=True)
    type_line = models.CharField(max_length=200)
    type = models.ManyToManyField(Type)
    subtype = models.ManyToManyField(SubType, blank=True)
    supertype = models.ManyToManyField(SuperType, blank=True)
    reserved = models.BooleanField()

    def __str__(self):
        return self.name


class Block(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class Expansion(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    block = models.ForeignKey(Block, on_delete=models.PROTECT,
                              blank=True, null=True)

    def __str__(self):
        return self.name


class Rarity(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class Watermark(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Border(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Edition(models.Model):
    card_name = models.ForeignKey(CardName, on_delete=models.PROTECT)
    expansion_name = models.ForeignKey(Expansion, on_delete=models.PROTECT)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)
    number = models.CharField(max_length=10)
    image_url = models.CharField(max_length=200)
    flavor_text = models.TextField(blank=True)
    rarity = models.ForeignKey(Rarity, on_delete=models.PROTECT)
    multiverse_id = models.IntegerField()
    watermark = models.ForeignKey(Watermark, on_delete=models.PROTECT,
                                  blank=True, null=True)
    border = models.ForeignKey(Border, on_delete=models.PROTECT)
    source = models.TextField(blank=True)
    promo_release_date = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return "{0} - {1}".format(self.card_name, self.expansion_name)

    class Meta:
        unique_together = ("card_name", "expansion_name", "number")


class Format(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class LegalityType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class LegalityExceptions(models.Model):
    format = models.ForeignKey(Format, on_delete=models.PROTECT)
    card_name = models.ForeignKey(CardName, on_delete=models.PROTECT)
    legality = models.ForeignKey(LegalityType, on_delete=models.PROTECT)

    def __str__(self):
        return "{0} - {1} - {2}".format(self.card_name, self.format,
                                        self.legality)

    class Meta:
        unique_together = ("card_name", "format")


class Language(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class ForeignName(models.Model):
    english_name = models.ForeignKey(CardName, on_delete=models.PROTECT)
    foreign_name = models.CharField(max_length=400)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    multiverse_id = models.IntegerField()

    def __str__(self):
        return "{0} - {1} - {2}".format(self.english_name, self.foreign_name,
                                        self.language)


class Ruling(models.Model):
    card_name = models.ForeignKey(CardName, on_delete=models.PROTECT)
    date = models.DateField()
    text = models.TextField()

    def __str__(self):
        return "Ruling: {0} - {1}".format(self.card_name, self.date)


class FlipCardPair(models.Model):
    day_side_card = models.ForeignKey(CardName, on_delete=models.PROTECT)
    night_side_card = models.ForeignKey(CardName, on_delete=models.PROTECT)

    def __str__(self):
        return "Day: {0} - Night: {1}".format(self.day_side_card,
                                              self.night_side_card)


class MeldCardTriplet(models.Model):
    top_card = models.ForeignKey(CardName, on_delete=models.PROTECT)
    bottom_card = models.ForeignKey(CardName, on_delete=models.PROTECT)
    meld_card = models.ForeignKey(CardName, on_delete=models.PROTECT)

    def __str__(self):
        if __name__ == '__main__':
            return "Top: {0} - Bottom: {1} - Meld: {2}".format(
                self.top_card, self.bottom_card, self.meld_card
            )
