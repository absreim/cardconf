import graphene

from graphene_django.types import DjangoObjectType

from cardconf.cards.models import (
    Color, Layout, Supertype, Type, Subtype, CardName, Block, Expansion,
    Rarity, Artist, Watermark
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


class Watermark(DjangoObjectType):
    class Meta:
        model = Watermark


class Query(object):
    all_colors = graphene.List(ColorType)
    all_layouts = graphene.List(LayoutType)
    all_supertypes = graphene.List(SupertypeType)
    all_types = graphene.List(TypeType)
    all_subtypes = graphene.List(SubtypeType)

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
