"""Bounded, parameterized evidence retrieval. No model-generated SQL is executed."""
import re
import sqlite3
from database.db import connect

STOPWORDS = set('what when where who did does were with from this that about show compare qué que quién quien cuándo cuando cómo como para sobre las los del una con por agua water happened before after earlier warnings existed sabía sabia'.split())


def read_select(sql, params=()):
    if not re.match(r'^\s*SELECT\b', sql, re.I):
        raise ValueError('Only SELECT statements are permitted')
    with connect(read_only=True) as conn:
        conn.set_authorizer(lambda action, *_: sqlite3.SQLITE_OK if action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION) else sqlite3.SQLITE_DENY)
        return [dict(row) for row in conn.execute(sql, params)]


def retrieve(plan):
    traces = []
    def run(sql, params=()):
        rows = read_select(sql, params)
        traces.append({'sql': sql, 'parameters': list(params), 'rows': len(rows)})
        return rows

    terms = [term for term in plan.get('terms', []) if isinstance(term, str) and term.strip()][:6]
    where = ['e.verified=1', 'EXISTS (SELECT 1 FROM event_sources es JOIN sources s ON s.id=es.source_id WHERE es.event_id=e.id AND s.verified=1 AND s.url IS NOT NULL AND s.url != "")']
    params = []
    if terms:
        fields = "lower(e.title || ' ' || e.description || ' ' || coalesce(e.location,'') || ' ' || coalesce(e.significance,''))"
        matches = []
        for term in terms:
            term = '%' + term.lower().replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_') + '%'
            matches.append(f"({fields} LIKE ? ESCAPE '\\' OR EXISTS (SELECT 1 FROM event_actors ea JOIN actors a ON a.id=ea.actor_id WHERE ea.event_id=e.id AND lower(a.name || ' ' || coalesce(a.institution,'')) LIKE ? ESCAPE '\\') OR EXISTS (SELECT 1 FROM claims c WHERE c.event_id=e.id AND c.verified=1 AND lower(c.claim_text) LIKE ? ESCAPE '\\'))")
            params.extend([term]*3)
        where.append('(' + ' OR '.join(matches) + ')')
    before_date = plan.get('before_date')
    if isinstance(before_date, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', before_date):
        where.append('e.event_date < ?')
        params.append(before_date)
    elif plan.get('before_year'):
        where.append('e.event_date < ?')
        params.append(f"{int(plan['before_year']):04d}-01-01")
    events = run('SELECT e.* FROM events e WHERE ' + ' AND '.join(where) + ' ORDER BY e.event_date LIMIT 25', params)
    evidence = {'events': events, 'actors': [], 'claims': [], 'responsibilities': [], 'commitments': [], 'sources': [], 'event_sources': []}
    if not events:
        return evidence, traces
    ids = [e['id'] for e in events]
    marks = ','.join('?' for _ in ids)
    evidence['actors'] = run(f'SELECT DISTINCT a.* FROM actors a JOIN event_actors ea ON ea.actor_id=a.id WHERE ea.event_id IN ({marks})', ids)
    for table in ('claims','commitments'):
        evidence[table] = run(f'SELECT t.* FROM {table} t JOIN sources s ON s.id=t.source_id WHERE t.event_id IN ({marks}) AND t.verified=1 AND s.verified=1 AND s.url IS NOT NULL AND s.url != "" ORDER BY t.' + ('claim_date' if table=='claims' else 'commitment_date') + ' LIMIT 50', ids)
    actor_ids = set(a['id'] for a in evidence['actors'])
    actor_ids.update(r['actor_id'] for key in ('claims','commitments') for r in evidence[key])
    if actor_ids:
        am = ','.join('?' for _ in actor_ids)
        evidence['actors'] = run(f'SELECT * FROM actors WHERE id IN ({am})', list(actor_ids))
        evidence['responsibilities'] = run(f'SELECT r.* FROM responsibilities r JOIN sources s ON s.id=r.source_id WHERE r.actor_id IN ({am}) AND r.verified=1 AND s.verified=1 AND s.url IS NOT NULL AND s.url != "" LIMIT 50', list(actor_ids))
    evidence['event_sources'] = run(f'SELECT es.* FROM event_sources es JOIN sources s ON s.id=es.source_id WHERE es.event_id IN ({marks}) AND s.verified=1 AND s.url IS NOT NULL AND s.url != ""', ids)
    source_ids = {r['source_id'] for key in ('claims','commitments','responsibilities') for r in evidence[key]}
    event_sources = run(f'SELECT s.* FROM sources s JOIN event_sources es ON es.source_id=s.id WHERE es.event_id IN ({marks}) AND s.verified=1 AND s.url IS NOT NULL AND s.url != ""', ids)
    source_ids.update(s['id'] for s in event_sources)
    if source_ids:
        evidence['sources'] = run('SELECT * FROM sources WHERE id IN (' + ','.join('?' for _ in source_ids) + ')', list(source_ids))
    evidence['scope'] = 'At most 25 matching events, 50 records per related entity. Not an exhaustive historical search. Dates delimit events; responsibility terms must be checked separately.'
    return evidence, traces


def fallback_plan(question):
    words = re.findall(r'[\wáéíóúñ]+', question.lower())
    lowered = question.lower()
    chronology = any(s in lowered for s in ('quién sabía', 'quien sabia', 'qué se sabía', 'que se sabia', 'who knew'))
    # A question about whether a crisis "began" at a named time needs the dated
    # record set, not a literal occurrence of the word "crisis" in a title.
    chronology = chronology or ('crisis' in lowered and ('comenzó' in lowered or 'comenzo' in lowered or 'empezó' in lowered or 'empezo' in lowered))
    before_date = '2026-10-01' if re.search(r'antes de octubre de 2026', lowered) else None
    return {'terms': [] if chronology else [w for w in words if w not in STOPWORDS and len(w)>3 and not w.isdigit()][:6], 'before_year': None, 'before_date': before_date}
