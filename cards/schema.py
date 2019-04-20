import graphene

from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from cards.models import (
    Color, Layout, Supertype, Type, Subtype, CardName, Block, Expansion,
    Rarity, Artist, Watermark, Border, Edition, Format, LegalityType,
    Legality, Language, ForeignVersion, Ruling, FlipCardPair,
    SplitCardPair, MeldCardTriplet
)


class ColorNode(DjangoObjectType):
    class Meta:
        model = Color
        filter_fields = ['name']
        interfaces = (relay.Node,)


class LayoutNode(DjangoObjectType):
    class Meta:
        model = Layout
        filter_fields = ['name']
        interfaces = (relay.Node,)


class SupertypeNode(DjangoObjectType):
    class Meta:
        model = Supertype
        filter_fields = ['name']
        interfaces = (relay.Node,)


class TypeNode(DjangoObjectType):
    class Meta:
        model = Type
        filter_fields = ['name']
        interfaces = (relay.Node,)


class SubtypeNode(DjangoObjectType):
    class Meta:
        model = Subtype
        filter_fields = ['name']
        interfaces = (relay.Node,)


class CardNameNode(DjangoObjectType):
    class Meta:
        model = CardName
        filter_fields = ['name']
        interfaces = (relay.Node,)


class BlockNode(DjangoObjectType):
    class Meta:
        model = Block
        filter_fields = ['name']
        interfaces = (relay.Node,)


class ExpansionNode(DjangoObjectType):
    class Meta:
        model = Expansion
        filter_fields = ['name']
        interfaces = (relay.Node,)


class RarityNode(DjangoObjectType):
    class Meta:
        model = Rarity
        filter_fields = ['name']
        interfaces = (relay.Node,)


class ArtistNode(DjangoObjectType):
    class Meta:
        model = Artist
        filter_fields = ['name']
        interfaces = (relay.Node,)


class WatermarkNode(DjangoObjectType):
    class Meta:
        model = Watermark
        filter_fields = ['name']
        interfaces = (relay.Node,)


class BorderNode(DjangoObjectType):
    class Meta:
        model = Border
        filter_fields = ['name']
        interfaces = (relay.Node,)


class EditionNode(DjangoObjectType):
    class Meta:
        model = Edition
        filter_fields = ['card_name']
        interfaces = (relay.Node,)


class FormatNode(DjangoObjectType):
    class Meta:
        model = Format
        filter_fields = ['name']
        interfaces = (relay.Node,)


class LegalityTypeNode(DjangoObjectType):
    class Meta:
        model = LegalityType
        filter_fields = ['name']
        interfaces = (relay.Node,)


class LegalityNode(DjangoObjectType):
    class Meta:
        model = Legality
        filter_fields = ['card_name']
        interfaces = (relay.Node,)


class LanguageNode(DjangoObjectType):
    class Meta:
        model = Language
        filter_fields = ['name']
        interfaces = (relay.Node,)


class ForeignVersionNode(DjangoObjectType):
    class Meta:
        model = ForeignVersion
        filter_fields = ['edition']
        interfaces = (relay.Node,)


class RulingNode(DjangoObjectType):
    class Meta:
        model = Ruling
        filter_fields = ['card_name']
        interfaces = (relay.Node,)


class FlipCardPairNode(DjangoObjectType):
    class Meta:
        model = FlipCardPair
        filter_fields = []
        interfaces = (relay.Node,)


class SplitCardPairNode(DjangoObjectType):
    class Meta:
        model = SplitCardPair
        filter_fields = []
        interfaces = (relay.Node,)


class MeldCardTripletNode(DjangoObjectType):
    class Meta:
        model = MeldCardTriplet
        filter_fields = []
        interfaces = (relay.Node,)


class Query(object):
    color = relay.Node.Field(ColorNode)
    layout = relay.Node.Field(LayoutNode)
    supertype = relay.Node.Field(SupertypeNode)
    type = relay.Node.Field(TypeNode)
    subtypes = relay.Node.Field(SubtypeNode)
    card_name = relay.Node.Field(CardNameNode)
    block = relay.Node.Field(BlockNode)
    expansion = relay.Node.Field(ExpansionNode)
    rarity = relay.Node.Field(RarityNode)
    artist = relay.Node.Field(ArtistNode)
    watermark = relay.Node.Field(WatermarkNode)
    border = relay.Node.Field(BorderNode)
    edition = relay.Node.Field(EditionNode)
    format = relay.Node.Field(FormatNode)
    legality_type = relay.Node.Field(LegalityTypeNode)
    legality = relay.Node.Field(LegalityNode)
    language = relay.Node.Field(LanguageNode)
    foreign_version = relay.Node.Field(ForeignVersionNode)
    ruling = relay.Node.Field(RulingNode)
    flip_card_pair = relay.Node.Field(FlipCardPairNode)
    split_card_pair = relay.Node.Field(SplitCardPairNode)
    meld_card_triplet = relay.Node.Field(MeldCardTripletNode)

    all_colors = DjangoFilterConnectionField(ColorNode)
    all_layouts = DjangoFilterConnectionField(LayoutNode)
    all_supertypes = DjangoFilterConnectionField(SupertypeNode)
    all_types = DjangoFilterConnectionField(TypeNode)
    all_subtypes = DjangoFilterConnectionField(SubtypeNode)
    all_card_names = DjangoFilterConnectionField(CardNameNode)
    all_blocks = DjangoFilterConnectionField(BlockNode)
    all_expansions = DjangoFilterConnectionField(ExpansionNode)
    all_rarities = DjangoFilterConnectionField(RarityNode)
    all_artists = DjangoFilterConnectionField(ArtistNode)
    all_watermarks = DjangoFilterConnectionField(WatermarkNode)
    all_borders = DjangoFilterConnectionField(BorderNode)
    all_editions = DjangoFilterConnectionField(EditionNode)
    all_formats = DjangoFilterConnectionField(FormatNode)
    all_legality_types = DjangoFilterConnectionField(LegalityTypeNode)
    all_legalities = DjangoFilterConnectionField(LegalityNode)
    all_languages = DjangoFilterConnectionField(LanguageNode)
    all_foreign_versions = DjangoFilterConnectionField(ForeignVersionNode)
    all_rulings = DjangoFilterConnectionField(RulingNode)
    all_flip_card_pairs = DjangoFilterConnectionField(FlipCardPairNode)
    all_split_card_pairs = DjangoFilterConnectionField(SplitCardPairNode)
    all_meld_card_triplets = DjangoFilterConnectionField(MeldCardTripletNode)
