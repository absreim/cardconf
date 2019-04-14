import graphene

from graphene_django.types import DjangoObjectType

from cards.models import (
    Color, Layout, Supertype, Type, Subtype, CardName, Block, Expansion,
    Rarity, Artist, Watermark, Border, Edition, Format, LegalityType,
    Legality, Language, ForeignVersion, Ruling, FlipCardPair,
    SplitCardPair, MeldCardTriplet
)


class ColorType(DjangoObjectType):
    class Meta:
        model = Color


class LayoutType(DjangoObjectType):
    class Meta:
        model = Layout


class SupertypeType(DjangoObjectType):
    class Meta:
        model = Supertype


class TypeType(DjangoObjectType):
    class Meta:
        model = Type


class SubtypeType(DjangoObjectType):
    class Meta:
        model = Subtype


class CardNameType(DjangoObjectType):
    class Meta:
        model = CardName


class BlockType(DjangoObjectType):
    class Meta:
        model = Block


class ExpansionType(DjangoObjectType):
    class Meta:
        model = Expansion


class RarityType(DjangoObjectType):
    class Meta:
        model = Rarity


class ArtistType(DjangoObjectType):
    class Meta:
        model = Artist


class WatermarkType(DjangoObjectType):
    class Meta:
        model = Watermark


class BorderType(DjangoObjectType):
    class Meta:
        model = Border


class EditionType(DjangoObjectType):
    class Meta:
        model = Edition


class FormatType(DjangoObjectType):
    class Meta:
        model = Format


class LegalityTypeType(DjangoObjectType):
    class Meta:
        model = LegalityType


class LegalityGrapheneType(DjangoObjectType):
    class Meta:
        model = Legality


class LanguageType(DjangoObjectType):
    class Meta:
        model = Language


class ForeignVersionType(DjangoObjectType):
    class Meta:
        model = ForeignVersion


class RulingType(DjangoObjectType):
    class Meta:
        model = Ruling


class FlipCardPairType(DjangoObjectType):
    class Meta:
        model = FlipCardPair


class SplitCardPairType(DjangoObjectType):
    class Meta:
        model = SplitCardPair


class MeldCardTripletType(DjangoObjectType):
    class Meta:
        model = MeldCardTriplet


class Query(object):
    all_colors = graphene.List(ColorType)
    all_layouts = graphene.List(LayoutType)
    all_supertypes = graphene.List(SupertypeType)
    all_types = graphene.List(TypeType)
    all_subtypes = graphene.List(SubtypeType)
    all_cardnames = graphene.List(CardNameType)
    all_blocks = graphene.List(BlockType)
    all_expansions = graphene.List(ExpansionType)
    all_rarities = graphene.List(RarityType)
    all_artists = graphene.List(ArtistType)
    all_watermarks = graphene.List(WatermarkType)
    all_borders = graphene.List(BorderType)
    all_editions = graphene.List(EditionType)
    all_formats = graphene.List(FormatType)
    all_legality_types = graphene.List(LegalityTypeType)
    all_legalities = graphene.List(LegalityGrapheneType)
    all_languages = graphene.List(LanguageType)
    all_foreign_versions = graphene.List(ForeignVersionType)
    all_rulings = graphene.List(RulingType)
    all_flip_card_pairs = graphene.List(FlipCardPairType)
    all_split_card_pairs = graphene.List(SplitCardPairType)
    all_meld_card_triplets = graphene.List(MeldCardTripletType)

    def resolve_all_colors(self, info, **kwargs):
        return Color.objects.all()

    def resolve_all_layouts(self, info, **kwargs):
        return Layout.objects.all()

    def resolve_all_supertypes(self, info, **kwargs):
        return Supertype.objects.all()

    def resolve_all_types(self, info, **kwargs):
        return Type.objects.all()

    def resolve_all_subtypes(self, info, **kwargs):
        return Subtype.objects.all()

    def resolve_all_cardnames(self, info, **kwargs):
        return CardName.objects.all()

    def resolve_all_blocks(self, info, **kwargs):
        return Block.objects.all()

    def resolve_all_expansions(self, info, **kwargs):
        return Expansion.objects.all()

    def resolve_all_rarities(self, info, **kwargs):
        return Rarity.objects.all()

    def resolve_all_artists(self, info, **kwargs):
        return Artist.objects.all()

    def resolve_all_watermarks(self, info, **kwargs):
        return Watermark.objects.all()

    def resolve_all_borders(self, info, **kwargs):
        return Border.objects.all()

    def resolve_all_editions(self, info, **kwargs):
        return Edition.objects.all()

    def resolve_all_formats(self, info, **kwargs):
        return Format.objects.all()

    def resolve_all_legality_types(self, info, **kwargs):
        return LegalityType.objects.all()

    def resolve_all_legalities(self, info, **kwargs):
        return Legality.objects.all()

    def resolve_all_languages(self, info, **kwargs):
        return Language.objects.all()

    def resolve_all_foreign_versions(self, info, **kwargs):
        return ForeignVersion.objects.all()

    def resolve_all_rulings(self, info, **kwargs):
        return Ruling.objects.all()

    def resolve_all_flip_card_pairs(self, info, **kwargs):
        return FlipCardPair.objects.all()

    def resolve_all_split_card_pairs(self, info, **kwargs):
        return SplitCardPair.objects.all()

    def resolve_all_meld_card_triplets(self, info, **kwargs):
        return MeldCardTriplet.objects.all()
