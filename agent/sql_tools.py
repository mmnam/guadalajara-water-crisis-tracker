"""Bounded, parameterized evidence retrieval. No model-generated SQL is executed."""
import re
import sqlite3
from database.db import connect
from services.records import ATTRIBUTED_STATUS, event_status

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
    for event in events:
        event['evidence_status'] = event_status(event)
        event['evidence_tier'] = 'verified'
    attributed_where = ["am.evidence_tier='attributed_reviewed'", "am.review_status='reviewed_attributed'", "am.url IS NOT NULL", "am.url != ''"]
    attributed_params = []
    if terms:
        fields = "lower(am.title || ' ' || am.author || ' ' || coalesce(am.account,'') || ' ' || coalesce(am.professional_role,'') || ' ' || am.paraphrase || ' ' || am.exact_claim)"
        attributed_matches = []
        for raw_term in terms:
            term = '%' + raw_term.lower().replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_') + '%'
            attributed_matches.append(f"{fields} LIKE ? ESCAPE '\\'")
            attributed_params.append(term)
        attributed_where.append('(' + ' OR '.join(attributed_matches) + ')')
    if isinstance(before_date, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', before_date):
        attributed_where.append('am.publication_date < ?')
        attributed_params.append(before_date)
    elif plan.get('before_year'):
        attributed_where.append('am.publication_date < ?')
        attributed_params.append(f"{int(plan['before_year']):04d}-01-01")
    attributed = run('SELECT am.* FROM attributed_material am WHERE ' + ' AND '.join(attributed_where) + ' ORDER BY am.publication_date,am.id LIMIT 25', attributed_params)
    for material in attributed:
        material['evidence_status'] = ATTRIBUTED_STATUS.get(material['id'], 'reviewed_analysis')
    attributed_sources = [{
        'id': material['id'], 'title': material['title'], 'publisher': material['publisher'],
        'url': material['url'], 'publication_date': material['publication_date'],
        'source_type': material['source_type'], 'reliability_notes': material['review_notes'],
        'evidence_tier': 'attributed_reviewed', 'evidence_status': material['evidence_status'],
        'review_status': material['review_status'],
    } for material in attributed]
    reviewed_where = ["ue.evidence_tier='reviewed_usable'", "ue.review_status='reviewed_usable'", "ue.url IS NOT NULL", "ue.url != ''"]
    reviewed_params = []
    if terms:
        fields = "lower(ue.title || ' ' || ue.description || ' ' || ue.significance || ' ' || ue.actor_names || ' ' || ue.source_title || ' ' || coalesce(ue.source_author,''))"
        matches = []
        for raw_term in terms:
            term = '%' + raw_term.lower().replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_') + '%'
            matches.append(f"{fields} LIKE ? ESCAPE '\\'")
            reviewed_params.append(term)
        reviewed_where.append('(' + ' OR '.join(matches) + ')')
    if isinstance(before_date, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', before_date):
        reviewed_where.append('ue.event_date < ?')
        reviewed_params.append(before_date)
    elif plan.get('before_year'):
        reviewed_where.append('ue.event_date < ?')
        reviewed_params.append(f"{int(plan['before_year']):04d}-01-01")
    reviewed = run('SELECT ue.* FROM usable_evidence ue WHERE ' + ' AND '.join(reviewed_where) + ' ORDER BY ue.event_date,ue.id LIMIT 25', reviewed_params)
    reviewed_sources = [{
        'id': item['source_id'], 'title': item['source_title'], 'publisher': item['publisher'],
        'url': item['url'], 'publication_date': item['publication_date'], 'source_type': item['source_type'],
        'author': item['source_author'], 'reliability_notes': item['reliability_notes'],
        'evidence_tier': item['evidence_tier'], 'evidence_status': item['evidence_status'],
        'review_status': item['review_status'], 'key_limitation': item['key_limitation'],
    } for item in reviewed]
    evidence = {
        'events': events, 'actors': [], 'claims': [], 'responsibilities': [], 'commitments': [],
        'sources': [], 'event_sources': [], 'attributed_evidence': attributed, 'reviewed_evidence': reviewed,
    }
    if not events:
        evidence['sources'] = attributed_sources + reviewed_sources
        evidence['verified_evidence'] = {'events': [], 'actors': [], 'claims': [], 'responsibilities': [], 'commitments': [], 'sources': [], 'event_sources': []}
        evidence['scope'] = 'At most 25 verified events, 25 explicitly reviewed attributed materials, and 25 reviewed usable records. Reviewed material supports only what its author, source, interviewee, or institution reported, observed, alleged, or analyzed.'
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
        for source in evidence['sources']:
            source['evidence_tier'] = 'verified'
            source['evidence_status'] = 'verified_document'
    evidence['verified_evidence'] = {
        'events': evidence['events'], 'actors': evidence['actors'], 'claims': evidence['claims'],
        'responsibilities': evidence['responsibilities'], 'commitments': evidence['commitments'],
        'sources': list(evidence['sources']), 'event_sources': evidence['event_sources'],
    }
    evidence['sources'].extend(attributed_sources + reviewed_sources)
    evidence['scope'] = 'At most 25 verified events, 50 records per related verified entity, 25 explicitly reviewed attributed materials, and 25 reviewed usable records. Any reviewed or attributed material supports only what its author, source, interviewee, or institution reported, observed, alleged, or analyzed; it is not a factual finding of the underlying proposition.'
    return evidence, traces


def fallback_plan(question):
    words = re.findall(r'[\wáéíóúñ]+', question.lower())
    lowered = question.lower()
    chronology = any(s in lowered for s in ('quién sabía', 'quien sabia', 'qué se sabía', 'que se sabia', 'who knew'))
    # A question about whether a crisis "began" at a named time needs the dated
    # record set, not a literal occurrence of the word "crisis" in a title.
    chronology = chronology or ('crisis' in lowered and ('comenzó' in lowered or 'comenzo' in lowered or 'empezó' in lowered or 'empezo' in lowered))
    chronology = chronology or any(phrase in lowered for phrase in (
        'qué pasó entre', 'que paso entre', 'what happened between',
        'qué sabemos con certeza', 'que sabemos con certeza',
        'sigue siendo una denuncia', 'sigue siendo una interpretación',
        'diferencias existen entre las versiones', 'differences between official versions',
    ))
    before_date = '2026-10-01' if re.search(r'antes de octubre de 2026', lowered) else None
    return {'terms': [] if chronology else [w for w in words if w not in STOPWORDS and len(w)>3 and not w.isdigit()][:6], 'before_year': None, 'before_date': before_date}
