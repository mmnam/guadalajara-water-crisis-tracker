import os
import json
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from agent.agent import ask
from agent.sql_tools import fallback_plan, retrieve
from database.db import connect
from database.seed import seed
from services import records


ROOT = Path(__file__).resolve().parents[1]
APPROVED = ROOT / 'data' / 'approved_records.json'
ATTRIBUTED = ROOT / 'data' / 'attributed_reviewed_records.json'
APPROVED_IDS = {1201, 1202, 1204, 1205, 1206, 1211, 1222, 1212, 1219, 1217, 1218, 1220}


class ApprovedImportTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ, {
            'DATABASE_PATH': str(Path(self.temp.name) / 'approved.sqlite3'),
            'OPENAI_API_KEY': '',
        })
        self.env.start()
        seed()  # Deliberately keep the fictional fixtures isolated in the same DB.
        seed(APPROVED)
        seed(ATTRIBUTED)

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def test_approved_allowlist_and_idempotence(self):
        with connect(read_only=True) as conn:
            ids = {row['id'] for row in conn.execute('SELECT id FROM events WHERE id >= 1200')}
            self.assertEqual(ids, APPROVED_IDS)
            self.assertEqual(conn.execute('SELECT count(*) FROM events WHERE id >= 1200').fetchone()[0], 12)
            self.assertEqual(conn.execute('SELECT count(*) FROM sources WHERE id IN (1101,1102) AND verified=1').fetchone()[0], 2)
            self.assertEqual(conn.execute('SELECT count(*) FROM claims WHERE id IN (1301,1302,1303,1306,1309,1310) AND verified=1').fetchone()[0], 0)
        seed(APPROVED)
        with connect(read_only=True) as conn:
            self.assertEqual(conn.execute('SELECT count(*) FROM events WHERE id >= 1200').fetchone()[0], 12)

    def test_normal_mode_excludes_demo_and_unverified_claims(self):
        visible = {row['id'] for row in records.timeline()}
        self.assertEqual(visible, APPROVED_IDS)
        self.assertNotIn(1, visible)
        self.assertEqual(records.statements([1001]), [])

    def test_every_approved_event_has_a_verified_source_link(self):
        with connect(read_only=True) as conn:
            rows = conn.execute('''
                SELECT e.id
                FROM events e
                JOIN event_sources es ON es.event_id=e.id
                JOIN sources s ON s.id=es.source_id
                WHERE e.id >= 1200 AND e.verified=1 AND s.verified=1 AND s.url <> ''
            ''').fetchall()
        self.assertEqual({row['id'] for row in rows}, APPROVED_IDS)

    def test_provenance_and_separate_april_march_events_are_preserved(self):
        with connect(read_only=True) as conn:
            e1222 = conn.execute('SELECT description,significance FROM events WHERE id=1222').fetchone()
            e1219 = conn.execute('SELECT event_date,description,significance FROM events WHERE id=1219').fetchone()
            e1217 = conn.execute('SELECT event_date,description FROM events WHERE id=1217').fetchone()
            e1218 = conn.execute('SELECT event_date,description FROM events WHERE id=1218').fetchone()
        self.assertIn('BOO.812.01625', e1222['description'])
        self.assertIn('original autónomo', e1222['significance'])
        self.assertIn('octubre de 2026', e1222['significance'])
        self.assertEqual(e1219['event_date'], '2026-03-05')
        self.assertIn('distinto', e1219['significance'])
        self.assertEqual(e1217['event_date'], e1218['event_date'])
        self.assertNotEqual(e1217['description'], e1218['description'])

    def test_six_historical_questions_retrieve_bounded_citable_evidence(self):
        questions = {
            '¿Qué se sabía sobre problemas de calidad del agua antes de octubre de 2026?': {1201, 1202, 1204, 1205, 1206, 1211, 1222, 1212, 1219, 1217, 1218, 1220},
            '¿Quién sabía qué y cuándo?': {1201},
            '¿La crisis del agua comenzó en octubre de 2026?': {1201},
            '¿Qué sabía SIAPA antes de octubre de 2026?': {1202},
            '¿Qué ocurrió entre CONAGUA y SIAPA en septiembre de 2025?': {1222},
            '¿SIAPA y Tlajomulco dieron la misma explicación del problema en abril de 2026?': {1217, 1218},
        }
        for question, expected in questions.items():
            evidence, _ = retrieve(fallback_plan(question))
            ids = {row['id'] for row in evidence['events']}
            self.assertTrue(expected.issubset(ids), question)
            self.assertTrue(evidence['sources'], question)
            self.assertTrue(all(
                source['url'] and (
                    source.get('evidence_tier') == 'attributed_reviewed'
                    or source.get('verified') == 1
                )
                for source in evidence['sources']
            ), question)

    def test_month_cutoff_includes_2026_records_before_october(self):
        evidence, _ = retrieve(fallback_plan('¿Qué sabía SIAPA antes de octubre de 2026?'))
        self.assertEqual({row['id'] for row in evidence['events']}, {1201, 1202, 1204, 1206, 1211, 1222, 1212, 1219, 1217, 1218, 1220})

    def test_event_id_citation_is_normalized_only_to_its_retrieved_source(self):
        def response(payload):
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))])
        client = MagicMock()
        client.chat.completions.create.side_effect = [
            response({'terms': ['conagua'], 'before_year': None, 'before_date': None}),
            response({'answer': 'La notificación está documentada [S1222]', 'source_ids': [1222]}),
        ]
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}), patch('agent.agent.OpenAI', return_value=client):
            result = ask('¿Qué ocurrió entre CONAGUA y SIAPA en septiembre de 2025?')
        self.assertEqual([source['id'] for source in result['sources']], [1102])
        self.assertIn('[S1102]', result['answer'])

    def test_declared_valid_sources_are_attached_when_inline_markers_are_missing(self):
        def response(payload):
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))])
        client = MagicMock()
        client.chat.completions.create.side_effect = [
            response({'terms': ['conagua'], 'before_year': None, 'before_date': None}),
            response({'answer': 'La notificación está documentada.', 'source_ids': [1102]}),
        ]
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}), patch('agent.agent.OpenAI', return_value=client):
            result = ask('¿Qué ocurrió entre CONAGUA y SIAPA en septiembre de 2025?')
        self.assertEqual([source['id'] for source in result['sources']], [1102])
        self.assertTrue(result['answer'].endswith('[S1102]'))

    def test_attributed_reviewed_material_is_retrieved_separately_and_labeled(self):
        evidence, _ = retrieve({'terms': ['nixticuil'], 'before_year': None, 'before_date': None})
        self.assertEqual(evidence['verified_evidence']['events'], [])
        self.assertEqual([row['id'] for row in evidence['attributed_evidence']], [2102])
        row = evidence['attributed_evidence'][0]
        self.assertEqual(row['evidence_tier'], 'attributed_reviewed')
        self.assertEqual(row['review_status'], 'reviewed_attributed')
        self.assertEqual(evidence['sources'][0]['evidence_tier'], 'attributed_reviewed')

    def test_arbitrary_unverified_record_is_not_promoted_to_attributed_evidence(self):
        with connect() as conn:
            conn.execute("INSERT INTO sources (id,title,url,verified) VALUES (2998,'unreviewed','https://example.org/unreviewed',0)")
            conn.execute("INSERT INTO events (id,event_date,title,description,category,verified) VALUES (2998,'2026-01-01','unreviewed lead','arbitrary research lead','other',0)")
            conn.execute('INSERT INTO event_sources (event_id,source_id) VALUES (2998,2998)')
        evidence, _ = retrieve({'terms': ['arbitrary'], 'before_year': None, 'before_date': None})
        self.assertEqual(evidence['verified_evidence']['events'], [])
        self.assertEqual(evidence['attributed_evidence'], [])

    def test_mixed_tiers_remain_separate_and_cited(self):
        def response(payload):
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))])
        client = MagicMock()
        client.chat.completions.create.side_effect = [
            response({'terms': ['siapa'], 'before_year': None, 'before_date': None}),
            response({'answer': 'Lo documentado: respuesta institucional [S1101]. Reportado o señalado: trabajadores entrevistados afirmaron problemas [S2103].', 'source_ids': [1101, 2103]}),
        ]
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}), patch('agent.agent.OpenAI', return_value=client):
            result = ask('¿Qué se documentó y qué reportaron trabajadores sobre SIAPA?')
        self.assertEqual({source['id'] for source in result['sources']}, {1101, 2103})
        self.assertEqual(result['evidence']['verified_evidence']['events'][0]['verified'], 1)
        self.assertTrue(result['evidence']['attributed_evidence'])
        self.assertIn('Reportado o señalado', result['answer'])
        model_payload = json.loads(client.chat.completions.create.call_args_list[1].kwargs['messages'][2]['content'])
        self.assertIn('verified_evidence', model_payload['evidence'])
        self.assertIn('attributed_evidence', model_payload['evidence'])
        self.assertIn(2103, {row['id'] for row in model_payload['evidence']['attributed_evidence']})

    def test_journalist_material_cannot_be_rendered_as_a_factual_finding(self):
        def response(payload):
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))])
        client = MagicMock()
        client.chat.completions.create.side_effect = [
            response({'terms': ['nixticuil'], 'before_year': None, 'before_date': None}),
            response({'answer': 'Está comprobado que el origen de la descarga fue identificado [S2102].', 'source_ids': [2102]}),
        ]
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}), patch('agent.agent.OpenAI', return_value=client):
            result = ask('¿Qué observó el periodista en El Nixticuil?')
        self.assertIn('no son suficientes', result['answer'])
        self.assertEqual(result['sources'], [])

    def test_unsupported_political_conclusion_fails_safely(self):
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            result = ask('¿Qué partido político gobernaba cuando estas quejas estaban siendo externadas?')
        self.assertIn('no son suficientes', result['answer'])
        self.assertIn('partido o la administración', result['notice'])

    def test_original_x_url_is_preserved(self):
        evidence, _ = retrieve({'terms': ['nuevo pico'], 'before_year': None, 'before_date': None})
        row = next(item for item in evidence['attributed_evidence'] if item['id'] == 2105)
        self.assertEqual(row['url'], 'https://x.com/JSTapetillo/status/2106757575630872957')

    def test_direct_date_question_keeps_date_as_a_search_target(self):
        evidence, _ = retrieve(fallback_plan('¿Qué señaló Josué Sánchez sobre Arroyo Seco el 17 de septiembre de 2025?'))
        self.assertIn(2101, {row['id'] for row in evidence['attributed_evidence']})

    def test_structured_model_output_drives_presentation_and_source_cards(self):
        def response(payload):
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))])
        client = MagicMock()
        client.chat.completions.create.side_effect = [
            response({'terms': ['nixticuil'], 'before_year': None, 'before_date': None}),
            response({
                'summary': 'El reportaje conserva una observación atribuida, no una conclusión técnica.',
                'verified_findings': [],
                'attributed_findings': [{
                    'date': '2026-04-13', 'title': 'Recorrido periodístico', 'author': 'Pepe Toral',
                    'text': 'Toral observó aguas negras y recogió testimonios de residentes.',
                    'source_ids': [2102], 'limitation': 'No hay análisis de laboratorio recuperado.',
                }],
                'limitations': ['No se establece el origen de la descarga.'],
                'source_ids': [2102],
            }),
        ]
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}), patch('agent.agent.OpenAI', return_value=client):
            result = ask('¿Qué observó el periodista en El Nixticuil?')
        self.assertEqual(result['sources'][0]['evidence_tier'], 'attributed_reviewed')
        self.assertEqual(result['presentation']['attributed_findings'][0]['source_ids'], [2102])

    def test_malformed_structured_model_output_falls_back_safely(self):
        def response(payload):
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))])
        client = MagicMock()
        client.chat.completions.create.side_effect = [
            response({'terms': ['nixticuil'], 'before_year': None, 'before_date': None}),
            response({'summary': 'Incompleto', 'verified_findings': [], 'attributed_findings': [], 'limitations': []}),
        ]
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}), patch('agent.agent.OpenAI', return_value=client):
            result = ask('¿Qué observó el periodista en El Nixticuil?')
        self.assertIn('no son suficientes', result['answer'])
        self.assertIsNone(result['presentation'])


if __name__ == '__main__':
    unittest.main()
