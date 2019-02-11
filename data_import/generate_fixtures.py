import argparse
import psycopg2
import json

parser = argparse.ArgumentParser()
parser.add_argument('dir', help='Directory to write output files.',
                    type=str, default='../fixtures')
parser.add_argument('-v', '--verbose', help='Print progress messages.',
                    action='store_true')
args = parser.parse_args()

DB_CONN_STRING = 'dbname=cardconf'

if args.verbose:
    print('Opening database connection.')
db_conn = psycopg2.connect(DB_CONN_STRING)
db_cursor = db_conn.cursor()

if args.verbose:
    print('Generating fixture for Color model.')
db_cursor.execute('SELECT DISTINCT(color) FROM cards_color_staging')
color_rows = db_cursor.fetchall()
color_entries = list(map(lambda c: {
    'model': 'cards.Color',
    'fields': {
        'name': c[0]
    }
}, color_rows))
with open(f'{args.dir}/color.json', 'w') as f:
    json.dump(color_entries, f)
if args.verbose:
    print(f'{len(color_entries)} entries generated for color.json.')

if args.verbose:
    print('Generating fixture for Layout model.')
db_cursor.execute('SELECT DISTINCT(layout) FROM cards_staging')
layout_rows = db_cursor.fetchall()
layout_entries = list(map(lambda l: {
    'model': 'cards.Layout',
    'fields': {
        'name': l[0]
    }
}, layout_rows))
with open(f'{args.dir}/layout.json', 'w') as f:
    json.dump(layout_entries, f)
if args.verbose:
    print(f'{len(layout_entries)} entries generated for layout.json.')

if args.verbose:
    print('Generating fixture for Supertype model.')
db_cursor.execute('SELECT DISTINCT(supertype) FROM cards_supertypes_staging')
supertype_rows = db_cursor.fetchall()
supertype_entries = list(map(lambda s: {
    'model': 'cards.Supertype',
    'fields': {
        'name': s[0]
    }
}, supertype_rows))
with open(f'{args.dir}/supertype.json', 'w') as f:
    json.dump(supertype_entries, f)
if args.verbose:
    print(f'{len(supertype_entries)} entries generated for supertype.json.')

if args.verbose:
    print('Generating fixture for Type model.')
db_cursor.execute('SELECT DISTINCT(type) FROM cards_types_staging')
type_rows = db_cursor.fetchall()
type_entries = list(map(lambda t: {
    'model': 'cards.Type',
    'fields': {
        'name': t[0]
    }
}, type_rows))
with open(f'{args.dir}/type.json', 'w') as f:
    json.dump(type_entries, f)
if args.verbose:
    print(f'{len(type_entries)} entries generated for type.json.')

if args.verbose:
    print('Generating fixture for Subtype model.')
db_cursor.execute('SELECT DISTINCT(subtype) FROM cards_subtypes_staging')
subtype_rows = db_cursor.fetchall()
subtype_entries = list(map(lambda s: {
    'model': 'cards.Subtype',
    'fields': {
        'name': s[0]
    }
}, subtype_rows))
with open(f'{args.dir}/subtype.json', 'w') as f:
    json.dump(subtype_entries, f)
if args.verbose:
    print(f'{len(subtype_entries)} entries generated for type.json.')

if args.verbose:
    print('Generating fixture for CardName model.')
db_cursor.execute('''SELECT deduped_cards_staging.name, max(layout), 
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
GROUP BY deduped_cards_staging.name''')
card_name_rows = db_cursor.fetchall()
card_name_entries = list(map(lambda c: {
    'model': 'cards.CardName',
    'fields': {
        'name': c[0],
        'layout': c[1],
        'rules_text': c[2],
        'power': c[3],
        'toughness': c[4],
        'cost': c[5],
        'cmc': c[6],
        'loyalty': c[7],
        'color': c[8],
        'color_identity': c[9],
        'type_line': c[10],
        'type': c[11],
        'subtype': c[12],
        'supertype': c[13],
        'reserved': c[14]
    }
}, card_name_rows))
with open(f'{args.dir}/card_name.json', 'w') as f:
    json.dump(card_name_entries, f)
if args.verbose:
    print(f'{len(card_name_entries)} entries generated for card_name.json.')

if args.verbose:
    print('Generating fixture for Block model.')
db_cursor.execute('SELECT DISTINCT block FROM sets_staging')
block_rows = db_cursor.fetchall()
block_entries = list(map(lambda b: {
    'model': 'cards.Block',
    'fields': {
        'name': b[0]
    }
}, block_rows))
with open(f'{args.dir}/block.json', 'w') as f:
    json.dump(block_entries, f)
if args.verbose:
    print(f'{len(block_entries)} entries generated for block.json.')

if args.verbose:
    print('Generating fixture for Expansion model.')
db_cursor.execute('SELECT DISTINCT name, block FROM sets_staging')
expansion_rows = db_cursor.fetchall()
expansion_entries = list(map(lambda e: {
    'model': 'cards.Expansion',
    'fields': {
        'name': e[0],
        'block': e[1]
    }
}, expansion_rows))
with open(f'{args.dir}/expansion.json', 'w') as f:
    json.dump(expansion_entries, f)
if args.verbose:
    print(f'{len(expansion_entries)} entries generated for expansion.json.')

if args.verbose:
    print('Generating fixture for Rarity model.')
db_cursor.execute('SELECT DISTINCT rarity FROM cards_staging')
rarity_rows = db_cursor.fetchall()
rarity_entries = list(map(lambda r: {
    'model': 'cards.Rarity',
    'fields': {
        'name': r[0]
    }
}, rarity_rows))
with open(f'{args.dir}/rarity.json', 'w') as f:
    json.dump(rarity_entries, f)
if args.verbose:
    print(f'{len(rarity_entries)} entries generated for rarity.json.')

if args.verbose:
    print('Generating fixture for Artist model.')
db_cursor.execute('SELECT DISTINCT artist FROM cards_staging')
artist_rows = db_cursor.fetchall()
artist_entries = list(map(lambda a: {
    'model': 'cards.Artist',
    'fields': {
        'name': a[0]
    }
}, artist_rows))
with open(f'{args.dir}/artist.json', 'w') as f:
    json.dump(artist_entries, f)
if args.verbose:
    print(f'{len(artist_entries)} entries generated for artist.json.')

if args.verbose:
    print('Generating fixture for Watermark model.')
db_cursor.execute('SELECT DISTINCT watermark FROM cards_staging')
watermark_rows = db_cursor.fetchall()
watermark_entries = list(map(lambda w: {
    'model': 'cards.Watermark',
    'fields': {
        'name': w[0]
    }
}, watermark_rows))
with open(f'{args.dir}/watermark.json', 'w') as f:
    json.dump(watermark_entries, f)
if args.verbose:
    print(f'{len(watermark_entries)} entries generated for watermark.json.')

if args.verbose:
    print('Generating fixture for Border model.')
db_cursor.execute('SELECT DISTINCT border FROM cards_staging')
border_rows = db_cursor.fetchall()
border_entries = list(map(lambda b: {
    'model': 'cards.Border',
    'fields': {
        'name': b[0]
    }
}, border_rows))
with open(f'{args.dir}/border.json', 'w') as f:
    json.dump(border_entries, f)
if args.verbose:
    print(f'{len(border_entries)} entries generated for border.json.')

if args.verbose:
    print('Generating fixture for Edition model.')
db_cursor.execute('''SELECT DISTINCT name, set_name, artist, number, image_url,
flavor, rarity, multiverse_id, watermark, border, source, release_date
FROM cards_staging''')
edition_rows = db_cursor.fetchall()
edition_entries = list(map(lambda e: {
    'model': 'cards.Edition',
    'fields': {
        'card_name': e[0],
        'expansion_name': e[1],
        'artist': e[2],
        'number': e[3],
        'image_url': e[4],
        'flavor_text': e[5],
        'rarity': e[6],
        'multiverse_id': e[7],
        'watermark': e[8],
        'border': e[9],
        'source': e[10],
        'promo_release_date': e[11]
    }
}, edition_rows))
with open(f'{args.dir}/edition.json', 'w') as f:
    json.dump(edition_entries, f)
if args.verbose:
    print(f'{len(edition_entries)} entries generated for edition.json.')

if args.verbose:
    print('Generating fixture for Format model.')
db_cursor.execute('''SELECT DISTINCT name FROM formats_staging''')
format_rows = db_cursor.fetchall()
format_entries = list(map(lambda f: {
    'model': 'cards.Format',
    'fields': {
        'name': f[0]
    }
}, format_rows))
with open(f'{args.dir}/format.json', 'w') as f:
    json.dump(format_entries, f)
if args.verbose:
    print(f'{len(format_entries)} entries generated for format.json.')

if args.verbose:
    print('Generating fixture for LegalityType model.')
db_cursor.execute('''SELECT DISTINCT legality FROM cards_legalities_staging''')
legality_type_rows = db_cursor.fetchall()
legality_type_entries = list(map(lambda l: {
    'model': 'cards.LegalityType',
    'fields': {
        'name': l[0]
    }
}, legality_type_rows))
with open(f'{args.dir}/legality_type.json'):
    json.dump(legality_type_entries, f)
if args.verbose:
    print(f'{len(legality_type_entries)} entries generated for legality_type.json.')

