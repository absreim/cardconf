import graphene

import cards.schema
import decks.schema


class Query(cards.schema.Query, decks.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
