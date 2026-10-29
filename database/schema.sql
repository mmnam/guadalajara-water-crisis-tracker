CREATE TABLE IF NOT EXISTS actors (
 id INTEGER PRIMARY KEY, name TEXT NOT NULL, actor_type TEXT NOT NULL,
 institution TEXT, role TEXT, start_date TEXT, end_date TEXT, notes TEXT,
 verified INTEGER NOT NULL DEFAULT 0 CHECK(verified IN (0,1)));
CREATE TABLE IF NOT EXISTS events (
 id INTEGER PRIMARY KEY, event_date TEXT NOT NULL, title TEXT NOT NULL,
 description TEXT NOT NULL, category TEXT NOT NULL, location TEXT, significance TEXT,
 verified INTEGER NOT NULL DEFAULT 0 CHECK(verified IN (0,1)));
CREATE TABLE IF NOT EXISTS sources (
 id INTEGER PRIMARY KEY, title TEXT NOT NULL, publisher TEXT, url TEXT,
 publication_date TEXT, source_type TEXT, reliability_notes TEXT,
 verified INTEGER NOT NULL DEFAULT 0 CHECK(verified IN (0,1)));
CREATE TABLE IF NOT EXISTS attributed_material (
 id INTEGER PRIMARY KEY, publication_date TEXT NOT NULL, publication_time TEXT,
 title TEXT NOT NULL, author TEXT NOT NULL, account TEXT, professional_role TEXT,
 publisher TEXT, url TEXT NOT NULL, source_type TEXT NOT NULL,
 paraphrase TEXT NOT NULL, exact_claim TEXT NOT NULL, evidence_type TEXT NOT NULL,
 supporting_documents TEXT, underlying_documents_retrieved INTEGER NOT NULL DEFAULT 0 CHECK(underlying_documents_retrieved IN (0,1)),
 corroboration_status TEXT NOT NULL, review_status TEXT NOT NULL CHECK(review_status='reviewed_attributed'),
 evidence_tier TEXT NOT NULL CHECK(evidence_tier='attributed_reviewed'), review_notes TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS usable_evidence (
 id INTEGER PRIMARY KEY, candidate_id INTEGER UNIQUE,
 event_date TEXT NOT NULL, title TEXT NOT NULL, description TEXT NOT NULL,
 category TEXT NOT NULL, location TEXT, significance TEXT NOT NULL,
 evidence_status TEXT NOT NULL CHECK(evidence_status IN ('verified_document','verified_official_statement','verified_attribution','reviewed_journalism','reviewed_analysis','documented_complaint','attributed_testimony')),
 evidence_tier TEXT NOT NULL CHECK(evidence_tier='reviewed_usable'),
 review_status TEXT NOT NULL CHECK(review_status='reviewed_usable'),
 source_id INTEGER NOT NULL, source_title TEXT NOT NULL, source_author TEXT,
 publisher TEXT, url TEXT NOT NULL, publication_date TEXT, source_type TEXT,
 reliability_notes TEXT NOT NULL, key_limitation TEXT NOT NULL, actor_names TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS event_sources (
 event_id INTEGER REFERENCES events(id), source_id INTEGER REFERENCES sources(id),
 PRIMARY KEY(event_id,source_id));
CREATE TABLE IF NOT EXISTS event_actors (
 event_id INTEGER REFERENCES events(id), actor_id INTEGER REFERENCES actors(id),
 PRIMARY KEY(event_id,actor_id));
CREATE TABLE IF NOT EXISTS claims (
 id INTEGER PRIMARY KEY, actor_id INTEGER NOT NULL REFERENCES actors(id),
 event_id INTEGER REFERENCES events(id), claim_date TEXT NOT NULL,
 claim_text TEXT NOT NULL, source_id INTEGER NOT NULL REFERENCES sources(id),
 verified INTEGER NOT NULL DEFAULT 0 CHECK(verified IN (0,1)));
CREATE TABLE IF NOT EXISTS responsibilities (
 id INTEGER PRIMARY KEY, actor_id INTEGER NOT NULL REFERENCES actors(id),
 responsibility TEXT NOT NULL, start_date TEXT, end_date TEXT,
 legal_or_institutional_basis TEXT, source_id INTEGER NOT NULL REFERENCES sources(id),
 verified INTEGER NOT NULL DEFAULT 0 CHECK(verified IN (0,1)));
CREATE TABLE IF NOT EXISTS commitments (
 id INTEGER PRIMARY KEY, actor_id INTEGER NOT NULL REFERENCES actors(id),
 event_id INTEGER REFERENCES events(id), commitment_date TEXT NOT NULL,
 commitment TEXT NOT NULL, deadline TEXT,
 status TEXT NOT NULL CHECK(status IN ('announced','in_progress','completed','delayed','unfulfilled','unknown')),
 source_id INTEGER NOT NULL REFERENCES sources(id),
 verified INTEGER NOT NULL DEFAULT 0 CHECK(verified IN (0,1)));
