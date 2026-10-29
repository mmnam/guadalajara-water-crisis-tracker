from database.db import connect


ATTRIBUTED_STATUS = {
    2101: 'reviewed_analysis', 2102: 'verified_attribution',
    2103: 'attributed_testimony', 2104: 'reviewed_journalism',
    2105: 'reviewed_analysis', 2106: 'verified_attribution',
}


def event_status(event):
    """Editorial status of a verified event, not a finding about every claim in it."""
    return {
        'public_complaint': 'documented_complaint',
        'official_statement': 'verified_official_statement',
        'government_action': 'verified_official_statement',
        'institutional_warning': 'verified_official_statement',
        'recommendation': 'verified_document',
        'investigation': 'verified_document',
        'formal_notification': 'verified_document',
    }.get(event.get('category'), 'verified_document')

def query(sql, params=()):
    with connect(read_only=True) as conn:
        return [dict(row) for row in conn.execute(sql, params)]

def actors():
    return query('SELECT * FROM actors ORDER BY name')

def sources(event_id):
    return query('SELECT s.* FROM sources s JOIN event_sources es ON es.source_id=s.id WHERE es.event_id=?', (event_id,))

def attributed_material():
    rows = query("SELECT * FROM attributed_material WHERE evidence_tier='attributed_reviewed' AND review_status='reviewed_attributed' ORDER BY publication_date,id")
    for row in rows:
        row['evidence_status'] = ATTRIBUTED_STATUS.get(row['id'], 'reviewed_analysis')
    return rows


def usable_sources():
    verified = query("SELECT * FROM sources WHERE verified=1 AND url IS NOT NULL AND url != '' ORDER BY publication_date,id")
    for source in verified:
        source.update(evidence_tier='verified', evidence_status='verified_document', review_status='reviewed_primary')
    reviewed = query("SELECT source_id id, source_title title, publisher, url, publication_date, source_type, source_author author, reliability_notes, evidence_status, evidence_tier, review_status, key_limitation FROM usable_evidence ORDER BY publication_date,id")
    attributed = [{
        'id': row['id'], 'title': row['title'], 'publisher': row['publisher'], 'url': row['url'],
        'publication_date': row['publication_date'], 'source_type': row['source_type'],
        'author': row['author'], 'reliability_notes': row['review_notes'],
        'evidence_status': row['evidence_status'], 'evidence_tier': row['evidence_tier'],
        'review_status': row['review_status'], 'key_limitation': row['review_notes'],
    } for row in attributed_material()]
    return verified + reviewed + attributed

def timeline(year=None, category=None, actor=None, demo=False, evidence_status=None, source_type=None):
    sql = '''SELECT e.*, GROUP_CONCAT(a.name, ' | ') actor_names, GROUP_CONCAT(a.id, ',') actor_ids
             FROM events e
             LEFT JOIN event_actors ea ON ea.event_id=e.id
             LEFT JOIN actors a ON a.id=ea.actor_id
             WHERE 1=1'''
    params = []
    if not demo:
        sql += ' AND e.verified=1 AND EXISTS (SELECT 1 FROM event_sources es JOIN sources s ON s.id=es.source_id WHERE es.event_id=e.id AND s.verified=1 AND s.url IS NOT NULL AND s.url != "")'
    for condition, value in [("substr(e.event_date,1,4)=?", year), ('e.category=?', category)]:
        if value is not None:
            sql += ' AND ' + condition
            params.append(value)
    verified = query(sql + ' GROUP BY e.id ORDER BY e.event_date,e.id', params)
    for row in verified:
        row.update(record_kind='verified', evidence_status=event_status(row), evidence_tier='verified')
        row['source_type'] = 'primary_document'
    reviewed_sql = "SELECT * FROM usable_evidence WHERE 1=1"
    reviewed_params = []
    if year is not None:
        reviewed_sql += ' AND substr(event_date,1,4)=?'
        reviewed_params.append(year)
    if category is not None:
        reviewed_sql += ' AND category=?'
        reviewed_params.append(category)
    if evidence_status is not None:
        reviewed_sql += ' AND evidence_status=?'
        reviewed_params.append(evidence_status)
    if source_type is not None:
        reviewed_sql += ' AND source_type=?'
        reviewed_params.append(source_type)
    reviewed = query(reviewed_sql + ' ORDER BY event_date,id', reviewed_params)
    for row in reviewed:
        row.update(record_kind='reviewed', verified=0, actor_names=row['actor_names'], actor_ids='')
    materials = []
    if category is None or category in ('reviewed_analysis', 'attributed_testimony', 'verified_attribution', 'reviewed_journalism'):
        for material in attributed_material():
            if (year is not None and not material['publication_date'].startswith(year)) or (evidence_status is not None and material['evidence_status'] != evidence_status) or (source_type is not None and material['source_type'] != source_type):
                continue
            materials.append({
                'id': material['id'], 'event_date': material['publication_date'], 'title': material['title'],
                'description': material['paraphrase'], 'category': material['evidence_status'],
                'location': None, 'significance': material['review_notes'], 'verified': 0,
                'record_kind': 'attributed', 'evidence_status': material['evidence_status'],
                'evidence_tier': material['evidence_tier'], 'source_id': material['id'],
                'source_title': material['title'], 'source_author': material['author'],
                'publisher': material['publisher'], 'url': material['url'],
                'publication_date': material['publication_date'], 'source_type': material['source_type'],
                'reliability_notes': material['review_notes'], 'key_limitation': material['review_notes'],
                'actor_names': material['author'], 'actor_ids': '',
            })
    records = verified + reviewed + materials
    if evidence_status is not None:
        records = [row for row in records if row['evidence_status'] == evidence_status]
    if source_type is not None:
        records = [row for row in records if row.get('source_type') == source_type]
    if actor is not None:
        if isinstance(actor, int):
            records = [row for row in records if str(actor) in (row.get('actor_ids') or '').split(',')]
        else:
            records = [row for row in records if actor in (row.get('actor_names') or '')]
    return sorted(records, key=lambda row: (row['event_date'], row['record_kind'], row['id']))

def statements(actor_ids, demo=False):
    if not actor_ids:
        return []
    return query('SELECT c.*,a.name,s.title source_title,s.url,s.verified source_verified FROM claims c JOIN actors a ON a.id=c.actor_id JOIN sources s ON s.id=c.source_id WHERE c.actor_id IN (' + ','.join('?' for _ in actor_ids) + ')' + ('' if demo else ' AND c.verified=1 AND s.verified=1 AND s.url IS NOT NULL AND s.url != ""') + ' ORDER BY c.claim_date', actor_ids)

def commitments(demo=False):
    return query('SELECT c.*,a.name,s.title source_title,s.url,e.title event_title FROM commitments c JOIN actors a ON a.id=c.actor_id JOIN sources s ON s.id=c.source_id LEFT JOIN events e ON e.id=c.event_id' + ('' if demo else ' WHERE c.verified=1 AND s.verified=1 AND s.url IS NOT NULL AND s.url != ""') + ' ORDER BY c.commitment_date')
