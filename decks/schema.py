import graphene

from graphene_django.types import DjangoObjectType

from decks.models import Deck


class DeckType(DjangoObjectType):
    class Meta:
        model = Deck


class Query(object):
    all_decks = graphene.List(DeckType)

    def resolve_all_decks(self, info, **kwargs):
        if info.context.user.is_authenticated():
            return Deck.objects.filter(user=info.context.user)
        else:
            return Deck.objects.none()
