import argparse
import psycopg2
import json

parser = argparse.ArgumentParser()
parser.add_argument('dir', help='Directory to write output files.',
                    type=str, default='../fixtures')
parser.add_argument('--verbose', help='Print progress messages.',
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
    json.dump(color_entries,f)
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
    json.dump(layout_entries,f)
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
    json.dump(supertype_entries,f)
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
    json.dump(type_entries,f)
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
    json.dump(subtype_entries,f)
if args.verbose:
    print(f'{len(subtype_entries)} entries generated for type.json.')

db_cursor.execute('''select deduped_cards_staging.name, max(layout), 
max(text), max(power), max(toughness), max(mana_cost), max(cmc), 
max(loyalty), array_agg(deduped_cards_color_staging.color), 
array_agg(deduped_cards_color_identity_staging.color), 
max(deduped_cards_staging.type), array_agg(deduped_cards_types_staging.type),
array_agg(subtype), array_agg(supertype), bool_or(reserved) from 
(select distinct on (name) * from cards_staging) as deduped_cards_staging 
join (select distinct on (name, color) * from cards_color_staging) as 
deduped_cards_color_staging on deduped_cards_staging.name = 
deduped_cards_color_staging.name join (select distinct on (name, color) * 
from cards_color_identity_staging) as deduped_cards_color_identity_staging on 
deduped_cards_staging.name = deduped_cards_color_identity_staging.name join 
(select distinct on (name, type) * from cards_types_staging) as 
deduped_cards_types_staging on deduped_cards_staging.name = 
deduped_cards_types_staging.name join (select distinct on (name, subtype) * 
from cards_subtypes_staging) as deduped_cards_subtypes_staging on 
deduped_cards_staging.name = deduped_cards_subtypes_staging.name join 
(select distinct on (name, supertype) * from cards_supertypes_staging) as 
deduped_cards_supertypes_staging on deduped_cards_staging.name = 
deduped_cards_supertypes_staging.name group by deduped_cards_staging.name''')
