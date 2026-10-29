import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from database.db import connect
from database.seed import bootstrap
from services import records


class BootstrapTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.database = Path(self.temp.name) / 'fresh.sqlite3'
        self.env = patch.dict(os.environ, {'DATABASE_PATH': str(self.database)})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def counts(self):
        with connect(read_only=True) as conn:
            return {
                'demo_events': conn.execute('SELECT count(*) FROM events WHERE id < 1000').fetchone()[0],
                'approved_events': conn.execute('SELECT count(*) FROM events WHERE id >= 1200').fetchone()[0],
                'attributed_material': conn.execute('SELECT count(*) FROM attributed_material').fetchone()[0],
                'usable_evidence': conn.execute('SELECT count(*) FROM usable_evidence').fetchone()[0],
            }

    def test_bootstrap_creates_missing_database_and_imports_committed_corpus(self):
        self.assertFalse(self.database.exists())

        bootstrap()

        self.assertTrue(self.database.exists())
        self.assertEqual(self.counts(), {
            'demo_events': 5,
            'approved_events': 12,
            'attributed_material': 6,
            'usable_evidence': 12,
        })

    def test_bootstrap_is_idempotent_and_keeps_demo_records_out_of_normal_mode(self):
        bootstrap()
        first_counts = self.counts()

        bootstrap()

        self.assertEqual(self.counts(), first_counts)
        self.assertNotIn(1, {row['id'] for row in records.timeline()})
        self.assertTrue({1, 2, 3, 4, 5}.issubset({row['id'] for row in records.timeline(demo=True)}))


if __name__ == '__main__':
    unittest.main()
