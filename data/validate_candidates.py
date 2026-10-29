"""Validate the review corpus without opening or modifying the application database.

This checks structure and references, not whether a source actually supports a claim.
"""
import json
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

PATH = Path(__file__).with_name('candidate_records.json')
TABLES = ('actors', 'sources', 'events', 'event_sources', 'event_actors', 'claims', 'responsibilities', 'commitments')
REVIEW_STATUSES = {'needs_review', 'strong_candidate', 'uncertain', 'primary_source_found', 'needs_additional_source'}


def main():
    data = json.loads(PATH.read_text(encoding='utf-8'))
    errors, warnings = [], []
    def check(condition, message):
        if not condition:
            errors.append(message)
    def check_date(value, label):
        if value is not None:
            try:
                check(date.fromisoformat(value).isoformat() == value, f'{label}: not ISO date')
            except (ValueError, TypeError):
                errors.append(f'{label}: invalid date {value!r}')
    for table in TABLES:
        check(isinstance(data.get(table), list), f'{table} must be an array')
    if errors:
        raise SystemExit('\n'.join(errors))
    ids = {}
    for table in ('actors', 'sources', 'events', 'claims', 'responsibilities', 'commitments'):
        values = [row.get('id') for row in data[table]]
        check(len(set(values)) == len(values) and None not in values, f'{table}: duplicate/missing IDs')
        ids[table] = set(values)
    for table in TABLES:
        for row in data[table]:
            label = f"{table}:{row.get('id', (row.get('event_id'),row.get('source_id', row.get('actor_id'))))}"
            check(row.get('verified') == 0, f'{label}: must remain unverified')
            review = row.get('review', {})
            check(review.get('status') in REVIEW_STATUSES and bool(review.get('reason')) and bool(review.get('notes')), f'{label}: incomplete review')
            for column in ('event_date','publication_date','claim_date','commitment_date','deadline','start_date','end_date'):
                check_date(row.get(column), f'{label}.{column}')
            if table in ('claims','responsibilities','commitments'):
                check(row.get('actor_id') in ids['actors'], f'{label}: actor missing')
                check(row.get('source_id') in ids['sources'], f'{label}: source missing')
                if table != 'responsibilities' and row.get('event_id') is not None:
                    check(row['event_id'] in ids['events'], f'{label}: event missing')
            if table == 'commitments':
                check(row.get('status') == 'unknown', f'{label}: completion not supported by a separate status source')
            if table == 'event_sources':
                check(row.get('source_id') in ids['sources'] and row.get('event_id') in ids['events'], f'{label}: missing reference')
            if table == 'event_actors':
                check(row.get('actor_id') in ids['actors'] and row.get('event_id') in ids['events'], f'{label}: missing reference')
    for table, cols in [('event_sources', ('event_id', 'source_id')), ('event_actors', ('event_id', 'actor_id'))]:
        pairs = [tuple(row.get(k) for k in cols) for row in data[table]]
        check(len(set(pairs)) == len(pairs), f'{table}: duplicate relationships')
    urls = [s.get('url') for s in data['sources']]
    check(len(urls) == len(set(urls)), 'duplicate source URL')
    for s in data['sources']:
        parts = urlparse(s.get('url') or '')
        check(parts.scheme in ('http','https') and bool(parts.netloc), f"source {s['id']}: invalid URL")
        check(bool(s.get('title')) and bool(s.get('publisher')) and bool(s.get('reliability_notes')), f"source {s['id']}: missing details")
        check(s.get('source_kind') in ('primary','secondary'), f"source {s['id']}: invalid source priority")
        check(s.get('access') in ('read','snippet_only','link_only'), f"source {s['id']}: invalid access flag")
        if s['access'] != 'read':
            warnings.append(f"S{s['id']}: {s['access']}, human must examine full document")
        if s.get('author') is None and s['source_type'] in ('news','investigation','interview','analysis','opinion'):
            warnings.append(f"S{s['id']}: author not established")
    titles = [e['title'].casefold().strip() for e in data['events']]
    check(len(set(titles)) == len(titles), 'duplicate event titles')
    linked_events = {r['event_id'] for r in data['event_sources']}
    linked_actors = {r['event_id'] for r in data['event_actors']}
    for e in data['events']:
        label = f"E{e['id']}"
        check(e['id'] in linked_events, f'{label}: no source')
        check(e['id'] in linked_actors, f'{label}: no actor')
        check(all(e.get(x) for x in ('event_date','title','description','category','location','significance')), f'{label}: missing event information')
        check(e.get('date_precision') == 'day', f'{label}: unexpected date precision')
    for row in data['claims']:
        if row.get('event_id') is not None and row.get('claim_date') != next(e['event_date'] for e in data['events'] if e['id'] == row['event_id']):
            warnings.append(f"claim {row['id']}: date differs from linked event; inspect context")
    same_day = Counter(e['event_date'] for e in data['events'])
    for day,count in same_day.items():
        if count > 1:
            warnings.append(f'{day}: {count} events; check they describe distinct actions')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f"OK: {len(data['events'])} events, {len(data['sources'])} sources, {len(data['claims'])} claims, {len(data['responsibilities'])} responsibilities, {len(data['commitments'])} commitments; all candidates unverified.")
    print('Manual checks remain essential: source accessibility, URL provenance, attribution, independent corroboration, and editorial accuracy.')
    for warning in warnings:
        print('REVIEW:', warning)

if __name__ == '__main__':
    main()
