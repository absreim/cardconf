import argparse
import psycopg2
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument('dir', help='Directory to write output files.',
                    type=str, default='../cards/fixtures', nargs='?')
parser.add_argument('-v', '--verbose', help='Print progress messages.',
                    action='store_true')
args = parser.parse_args()

DB_CONN_STRING = 'dbname=cardconf'

if args.verbose:
    print('Opening database connection.')
db_conn = psycopg2.connect(DB_CONN_STRING)
db_cursor = db_conn.cursor()


def generate_fixture_for_model(model_name, file_name, db_query,
                               entry_generator):
    if args.verbose:
        print(f'Generating fixture for {model_name} model.')
    db_cursor.execute(db_query)
    rows = db_cursor.fetchall()
    entries = list(map(entry_generator, rows))
    with open(f'{args.dir}/{file_name}.json', 'w') as f:
        json.dump(entries, f)
    if args.verbose:
        print(f'{len(entries)} entries generated for {file_name}.json.')


color_query = 'SELECT DISTINCT(color) FROM cards_color_staging'


def color_generator(row):
    return {
        'model': 'cards.Color',
        'fields': {
            'name': row[0]
        }
    }


generate_fixture_for_model('Color', 'color', color_query, color_generator)

layout_query = 'SELECT DISTINCT(layout) FROM cards_staging'


def layout_generator(row):
    return {
        'model': 'cards.Layout',
        'fields': {
            'name': row[0]
        }
    }


generate_fixture_for_model('Layout', 'layout', layout_query, layout_generator)

supertype_query = 'SELECT DISTINCT(supertype) FROM cards_supertypes_staging'


def supertype_generator(row):
    return {
        'model': 'cards.Supertype',
        'fields': {
            'name': row[0]
        }
    }
    

generate_fixture_for_model('Supertype', 'supertype', supertype_query,
                           supertype_generator)

type_query = 'SELECT DISTINCT(type) FROM cards_types_staging'


def type_generator(row):
    return {
        'model': 'cards.Type',
        'fields': {
            'name': row[0]
        }
    }


generate_fixture_for_model('Type', 'type', type_query, type_generator)

subtype_query = 'SELECT DISTINCT(subtype) FROM cards_subtypes_staging'


def subtype_generator(row):
    return {
        'model': 'cards.Subtype',
        'fields': {
            'name': row[0]
        }
    }


generate_fixture_for_model('Subtype', 'subtype', subtype_query, subtype_generator)

card_name_query = '''SELECT deduped_cards_staging.name, max(layout), 
max(text), max(power), max(toughness), max(mana_cost), max(cmc), 
max(loyalty), array_agg(deduped_cards_color_staging.color), 
array_agg(deduped_cards_color_identity_staging.color), 
max(deduped_cards_staging.type), array_agg(deduped_cards_types_staging.type),
array_agg(subtype), array_agg(supertype), bool_or(reserved) 
FROM (SELECT DISTINCT ON (name) * FROM cards_staging) AS 
    deduped_cards_staging
LEFT JOIN (SELECT DISTINCT ON (name, color) * from cards_color_staging) AS 
    deduped_cards_color_staging ON deduped_cards_staging.name = 
    deduped_cards_color_staging.name 
LEFT JOIN (SELECT DISTINCT ON (name, color) * FROM 
    cards_color_identity_staging) AS deduped_cards_color_identity_staging 
    ON deduped_cards_staging.name = 
    deduped_cards_color_identity_staging.name 
JOIN (SELECT DISTINCT ON (name, type) * FROM cards_types_staging) AS 
    deduped_cards_types_staging on deduped_cards_staging.name = 
    deduped_cards_types_staging.name 
LEFT JOIN (SELECT DISTINCT ON (name, subtype) * FROM cards_subtypes_staging) AS
    deduped_cards_subtypes_staging ON 
    deduped_cards_staging.name = deduped_cards_subtypes_staging.name 
LEFT JOIN (SELECT DISTINCT ON (name, supertype) * FROM 
    cards_supertypes_staging) AS deduped_cards_supertypes_staging ON 
    deduped_cards_staging.name = deduped_cards_supertypes_staging.name 
GROUP BY deduped_cards_staging.name'''


def card_name_generator(row):
    card_name_dict = {
        'model': 'cards.CardName',
        'fields': {
            'name': row[0],
            'layout': row[1],
            'rules_text': row[2],
            'power': row[3],
            'toughness': row[4],
            'cost': row[5],
            'cmc': row[6],
            'loyalty': row[7],
            'type_line': row[10],
            'reserved': row[14]
        }
    }
    if row[8] is not None:
        card_name_dict['color'] = row[8]
    if row[9] is not None:
        card_name_dict['color_identity'] = row[9]
    if row[11] is not None:
        card_name_dict['type'] = row[11]
    if row[12] is not None:
        card_name_dict['subtype'] = row[12]
    if row[13] is not None:
        card_name_dict['supertype'] = row[13]
    return card_name_dict


generate_fixture_for_model('CardName', 'card_name', card_name_query,
                           card_name_generator)

block_query = 'SELECT DISTINCT block FROM sets_staging'


def block_generator(row):
    return {
        'model': 'cards.Block',
        'fields': {
            'name': row[0]
        }
    }


generate_fixture_for_model('Block', 'block', block_query, block_generator)

expansion_query = 'SELECT DISTINCT name, block FROM sets_staging'


def expansion_generator(row):
    return {
        'model': 'cards.Expansion',
        'fields': {
            'name': row[0],
            'block': row[1]
        }
    }


generate_fixture_for_model('Expansion', 'expansion', expansion_query,
                           expansion_generator)

addtl_expansion_query = '''SELECT DISTINCT set_name from cards_staging WHERE
set_name NOT IN (SELECT DISTINCT name FROM sets_staging)'''

child_set_name_matcher = re.compile('^(.+) (Planes|Schemes)$')


def addtl_expansion_generator(row):
    name = row[0]
    match_obj = child_set_name_matcher.match(name)
    return {
        'model': 'cards.Expansion',
        'fields': {
            'name': name,
            'block': '',
            'parent': match_obj.group(1) if match_obj else None
        }
    }


generate_fixture_for_model('Expansion', 'addtl_expansion',
                           addtl_expansion_query, addtl_expansion_generator)

rarity_query = 'SELECT DISTINCT rarity FROM cards_staging'


def rarity_generator(row):
    return {
        'model': 'cards.Rarity',
        'fields': {
            'name': row[0]
        }
    }


generate_fixture_for_model('Rarity', 'rarity', rarity_query, rarity_generator)

artist_query = 'SELECT DISTINCT artist FROM cards_staging'


def artist_generator(row):
    return {
    'model': 'cards.Artist',
    'fields': {
        'name': row[0]
    }
}


generate_fixture_for_model('Artist', 'artist', artist_query, artist_generator)

watermark_query = 'SELECT DISTINCT watermark FROM cards_staging'


def watermark_generator(row):
    return {
    'model': 'cards.Watermark',
    'fields': {
        'name': row[0]
    }
}


generate_fixture_for_model('Watermark', 'watermark', watermark_query,
                           watermark_generator)


border_query = 'SELECT DISTINCT border FROM cards_staging'


def border_generator(row):
    return {
        'model': 'cards.Border',
        'fields': {
            'name': row[0]
        }
    }


generate_fixture_for_model('Border', 'border', border_query, border_generator)

edition_query = '''SELECT DISTINCT name, set_name, artist, number, image_url,
flavor, rarity, multiverse_id, watermark, border, source, release_date, id
FROM cards_staging'''


def edition_generator(row):
    return {
        'model': 'cards.Edition',
        'fields': {
            'card_name': row[0],
            'expansion_name': row[1],
            'artist': row[2],
            'number': row[3],
            'image_url': row[4],
            'flavor_text': row[5],
            'rarity': row[6],
            'multiverse_id': row[7],
            'watermark': row[8],
            'border': row[9],
            'source': row[10],
            'promo_release_date': row[11],
            'id': row[12]
        }
    }


generate_fixture_for_model('Edition', 'edition', edition_query,
                           edition_generator)

format_query = 'SELECT DISTINCT name FROM formats_staging'


def format_generator(row):
    return {
        'model': 'cards.Format',
        'fields': {
            'name': row[0]
        }
    }


generate_fixture_for_model('Format', 'format', format_query,
                           format_generator)

legality_type_query = 'SELECT DISTINCT legality FROM cards_legalities_staging'


def legality_type_generator(row):
    return {
        'model': 'cards.LegalityType',
        'fields': {
            'name': row[0]
        }
    }


generate_fixture_for_model('LegalityType', 'legality_type',
                           legality_type_query, legality_type_generator)


legality_query = '''SELECT DISTINCT name, format, legality 
FROM cards_legalities_staging '''


def legality_generator(row):
    return {
        'model': 'cards.Legality',
        'fields': {
            'card_name': row[0],
            'format': row[1],
            'legality': row[2]
        }
    }


generate_fixture_for_model('Legality', 'legality', legality_query,
                           legality_generator)

language_query = 'SELECT DISTINCT language FROM cards_foreign_names_staging'


def language_generator(row):
    return {
        'model': 'cards.Language',
        'fields': {
            'name': row[0]
        }
    }


generate_fixture_for_model('Language', 'language', language_query,
                           language_generator)

foreign_version_query = '''SELECT DISTINCT id, foreign_name, language,
multiverse_id, text, flavor, image_url FROM 
cards_foreign_names_staging'''


def foreign_version_generator(row):
    return {
        'model': 'cards.ForeignVersion',
        'fields': {
            'edition': row[0],
            'foreign_name': row[1],
            'language': row[2],
            'multiverse_id': row[3],
            'rules_text': row[4],
            'flavor_text': row[5],
            'image_url': row[6]
        }
    }


generate_fixture_for_model('ForeignVersion', 'foreign_version',
                           foreign_version_query, foreign_version_generator)

ruling_query = 'SELECT DISTINCT name, date, text FROM cards_rulings_staging'


def ruling_generator(row):
    return {
        'model': 'cards.Ruling',
        'fields': {
            'card_name': row[0],
            'date': row[1],
            'text': row[2]
        }
    }


generate_fixture_for_model('Ruling', 'ruling', ruling_query, ruling_generator)

flip_card_pair_query = '''SELECT DISTINCT name AS first_card_name,
second_card_name FROM cards_staging JOIN (SELECT DISTINCT first_card_name,
second_card_name FROM cards_pairs_staging) AS deduped_cards_pairs_staging ON
cards_staging.name = deduped_cards_pairs_staging.first_card_name WHERE
cards_staging.layout = \'transform\''''


def flip_card_pair_generator(row):
    return {
        'model': 'cards.FlipCardPair',
        'fields': {
            'day_side_card': row[0],
            'night_side_card': row[1]
        }
    }


generate_fixture_for_model('FlipCardPair', 'flip_card_pair',
                           flip_card_pair_query, flip_card_pair_generator)

split_card_pair_query = '''SELECT DISTINCT name AS first_card_name,
second_card_name FROM cards_staging JOIN (SELECT DISTINCT first_card_name,
second_card_name FROM cards_pairs_staging) AS deduped_cards_pairs_staging ON
cards_staging.name = deduped_cards_pairs_staging.first_card_name WHERE
cards_staging.layout = \'split\''''


def split_card_pair_generator(row):
    return {
        'model': 'cards.SplitCardPair',
        'fields': {
            'left_side_card': row[0],
            'right_side_card': row[1]
        }
    }


generate_fixture_for_model('SplitCardPair', 'split_card_pair',
                           split_card_pair_query, split_card_pair_generator)

meld_card_triplet_query = '''SELECT DISTINCT name AS first_card_name,
second_card_name, third_card_name FROM cards_staging JOIN (SELECT DISTINCT
first_card_name, second_card_name, third_card_name FROM
cards_triplets_staging) as deduped_cards_triplets_staging ON
cards_staging.name = deduped_cards_triplets_staging.first_card_name WHERE
cards_staging.layout = \'meld\''''


def meld_card_triplet_generator(row):
    return {
        'model': 'cards.MeldCardTriplet',
        'fields': {
            'bottom_card': row[0],
            'meld_card': row[1],
            'top_card': row[2]
        }
    }


generate_fixture_for_model('MeldCardTriplet', 'meld_card_triplet',
                           meld_card_triplet_query,
                           meld_card_triplet_generator)

db_conn.commit()
db_cursor.close()
db_conn.close()
