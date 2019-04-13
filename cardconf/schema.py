import graphene

import cards.schema
import decks.schema


class Query(cards.schema, decks.schema, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
