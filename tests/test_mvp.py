import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace

from database.db import connect
from database.seed import seed
from agent.sql_tools import read_select, retrieve
from agent.agent import ask
from services import records


class MVPTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ, {'DATABASE_PATH':str(Path(self.temp.name)/'test.sqlite3'), 'OPENAI_API_KEY':''})
        self.env.start()
        seed()

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def verified_fixture(self):
        with connect() as conn:
            conn.execute("UPDATE events SET verified=1 WHERE id=1")
            conn.execute("UPDATE sources SET verified=1,url='https://example.org/fixture' WHERE id=1")
            conn.execute('UPDATE claims SET verified=1 WHERE id=1')
            conn.execute('UPDATE responsibilities SET verified=1 WHERE id=1')
            conn.execute('UPDATE commitments SET verified=1 WHERE id=1')

    def test_seed_idempotent_and_demo_isolation(self):
        seed()
        self.assertEqual(len(records.timeline(demo=True)),5)
        self.assertEqual(records.timeline(),[])
        evidence,traces=retrieve({'terms':[]})
        self.assertFalse(evidence['events'])
        self.assertTrue(traces)
        self.assertIn('not sufficient',ask('What happened?')['answer'])

    def test_filters(self):
        self.assertEqual(len(records.timeline(year='2023',actor=1,demo=True)),1)
        self.assertEqual(records.timeline(category='protest',demo=True),[])
        self.assertEqual(len(records.statements([1],True)),5)
        self.assertEqual(len(records.commitments(True)),5)

    def test_read_only(self):
        for sql in ('DELETE FROM events','PRAGMA user_version=5','SELECT 1; DROP TABLE events','SELECT load_extension("x")'):
            with self.assertRaises(Exception):
                read_select(sql)
        self.assertEqual(read_select('SELECT count(*) n FROM events')[0]['n'],5)

    def test_evidence_relationships_and_parameterization(self):
        self.verified_fixture()
        evidence,traces=retrieve({'terms':[], 'before_year':2023})
        self.assertEqual(len(evidence['events']),1)
        for table in ('claims','responsibilities','commitments','sources','event_sources','actors'):
            self.assertTrue(evidence[table],table)
        evidence,_=retrieve({'terms':["' OR 1=1 --"]})
        self.assertEqual(evidence['events'],[])
        self.assertEqual(records.timeline()[0]['id'],1)

    def test_foreign_keys_and_import_transaction(self):
        bad=Path(self.temp.name)/'bad.json'
        bad.write_text(json.dumps({'events':[{'id':99,'event_date':'2026-01-01','title':'x','description':'x','category':'other'}],'event_sources':[{'event_id':99,'source_id':999}]}))
        with self.assertRaises(Exception):
            seed(bad)
        self.assertEqual(read_select('SELECT * FROM events WHERE id=99'),[])

    def test_citation_validation(self):
        self.verified_fixture()
        def response(payload):
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))])
        for source_id, valid in [(1,True),(999,False)]:
            client = MagicMock()
            client.chat.completions.create.side_effect = [
                response({'terms':[], 'before_year':None}),
                response({'answer':f'Documented statement [S{source_id}]', 'source_ids':[source_id]})]
            with patch.dict(os.environ, {'OPENAI_API_KEY':'test-key'}), patch('agent.agent.OpenAI', return_value=client):
                result=ask('What happened?')
            self.assertTrue(result['sources'])
            if not valid:
                self.assertTrue(result['presentation']['fallback'])
                self.assertNotIn(999, {source['id'] for source in result['sources']})

    def test_streamlit_pages(self):
        from streamlit.testing.v1 import AppTest
        app=AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py'), default_timeout=20).run()
        self.assertFalse(app.exception)
        app.sidebar.toggle[0].set_value(True).run()
        for page in ('Línea del tiempo','Comparar declaraciones','Compromisos','Fuentes y método','Pregúntale al archivo'):
            app.sidebar.radio[0].set_value(page).run()
            self.assertFalse(app.exception, page)
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.session_state['messages']),1)

if __name__ == '__main__':
    unittest.main()
