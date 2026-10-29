from database.db import connect

def query(sql, params=()):
    with connect(read_only=True) as conn:
        return [dict(row) for row in conn.execute(sql, params)]

def actors():
    return query('SELECT * FROM actors ORDER BY name')

def sources(event_id):
    return query('SELECT s.* FROM sources s JOIN event_sources es ON es.source_id=s.id WHERE es.event_id=?', (event_id,))

def timeline(year=None, category=None, actor=None, demo=False):
    sql = 'SELECT e.* FROM events e WHERE 1=1'
    params = []
    if not demo:
        sql += ' AND e.verified=1 AND EXISTS (SELECT 1 FROM event_sources es JOIN sources s ON s.id=es.source_id WHERE es.event_id=e.id AND s.verified=1 AND s.url IS NOT NULL AND s.url != "")'
    for condition, value in [("substr(e.event_date,1,4)=?", year), ('e.category=?', category), ('EXISTS (SELECT 1 FROM event_actors ea WHERE ea.event_id=e.id AND ea.actor_id=?)', actor)]:
        if value is not None:
            sql += ' AND ' + condition
            params.append(value)
    return query(sql + ' ORDER BY e.event_date,e.id', params)

def statements(actor_ids, demo=False):
    if not actor_ids:
        return []
    return query('SELECT c.*,a.name,s.title source_title,s.url,s.verified source_verified FROM claims c JOIN actors a ON a.id=c.actor_id JOIN sources s ON s.id=c.source_id WHERE c.actor_id IN (' + ','.join('?' for _ in actor_ids) + ')' + ('' if demo else ' AND c.verified=1 AND s.verified=1 AND s.url IS NOT NULL AND s.url != ""') + ' ORDER BY c.claim_date', actor_ids)

def commitments(demo=False):
    return query('SELECT c.*,a.name,s.title source_title,s.url,e.title event_title FROM commitments c JOIN actors a ON a.id=c.actor_id JOIN sources s ON s.id=c.source_id LEFT JOIN events e ON e.id=c.event_id' + ('' if demo else ' WHERE c.verified=1 AND s.verified=1 AND s.url IS NOT NULL AND s.url != ""') + ' ORDER BY c.commitment_date')
