import json
from database.db import ROOT, connect, initialize

TABLES = ('actors', 'events', 'sources', 'attributed_material', 'usable_evidence', 'event_sources', 'event_actors', 'claims', 'responsibilities', 'commitments')

def seed(path=None):
    """Import records transactionally. Existing IDs are preserved, never overwritten."""
    payload = json.loads((path or ROOT / 'data/seed_data.json').read_text())
    initialize()
    with connect() as conn:
        for table in TABLES:
            allowed = {row['name'] for row in conn.execute(f'PRAGMA table_info({table})')}
            for row in payload.get(table, []):
                if not row or not set(row).issubset(allowed):
                    raise ValueError(f'Invalid columns in {table}')
                columns = list(row)
                conn.execute(f'INSERT INTO {table} ({",".join(columns)}) VALUES ({",".join("?" for _ in columns)}) ON CONFLICT DO NOTHING', list(row.values()))
