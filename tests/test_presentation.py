import unittest
from pathlib import Path

from agent.presentation import source_label, validate_presentation


SOURCES = {
    1102: {'id': 1102, 'publisher': 'CEDHJ', 'publication_date': '2026-04-30', 'source_type': 'human_rights_report', 'title': 'Recomendación', 'url': 'https://example.org/cedhj', 'verified': 1},
    2101: {'id': 2101, 'publisher': 'X', 'publication_date': '2025-09-17', 'source_type': 'technical_specialist_x_thread', 'title': 'Hilo', 'url': 'https://x.com/JSTapetillo/status/1968267797819265026', 'evidence_tier': 'attributed_reviewed'},
}


def payload(verified=True, attributed=True):
    return {
        'summary': 'Hay antecedentes documentados, con límites pendientes.',
        'verified_findings': ([{'date': '2025-09-19', 'title': 'CONAGUA → SIAPA', 'text': 'Se documentó una notificación de riesgo [S1102][S1102].', 'source_ids': [1102], 'limitation': 'El original no fue recuperado.'}] if verified else []),
        'attributed_findings': ([{'date': '2025-09-17', 'title': 'Análisis de Josué Sánchez', 'author': 'Josué Sánchez', 'text': 'Sánchez señaló factores de riesgo [S2101].', 'source_ids': [2101], 'limitation': 'No es un peritaje.'}] if attributed else []),
        'limitations': ['No se establece causalidad.'],
        'source_ids': ([1102] if verified else []) + ([2101] if attributed else []),
    }


class PresentationTest(unittest.TestCase):
    def test_tier_one_only_presentation(self):
        result = validate_presentation(payload(verified=True, attributed=False), SOURCES)
        self.assertEqual(len(result['verified_findings']), 1)
        self.assertEqual(result['attributed_findings'], [])

    def test_tier_two_only_presentation(self):
        result = validate_presentation(payload(verified=False, attributed=True), SOURCES)
        self.assertEqual(len(result['attributed_findings']), 1)
        self.assertEqual(result['attributed_findings'][0]['author'], 'Josué Sánchez')

    def test_mixed_presentation_keeps_tiers_separate(self):
        result = validate_presentation(payload(), SOURCES)
        self.assertEqual(result['verified_findings'][0]['source_ids'], [1102])
        self.assertEqual(result['attributed_findings'][0]['source_ids'], [2101])

    def test_limitations_and_duplicate_citations_are_cleaned(self):
        result = validate_presentation(payload(), SOURCES)
        self.assertEqual(result['limitations'], ['No se establece causalidad.'])
        self.assertNotIn('[S1102]', result['verified_findings'][0]['text'])
        self.assertNotIn('[S2101]', result['attributed_findings'][0]['text'])

    def test_wrong_tier_or_malformed_presentation_is_rejected(self):
        wrong_tier = payload(verified=True, attributed=False)
        wrong_tier['verified_findings'][0]['source_ids'] = [2101]
        wrong_tier['source_ids'] = [2101]
        with self.assertRaises(ValueError):
            validate_presentation(wrong_tier, SOURCES)
        malformed = payload(verified=False, attributed=True)
        del malformed['attributed_findings'][0]['author']
        with self.assertRaises(ValueError):
            validate_presentation(malformed, SOURCES)

    def test_source_cards_have_explicit_tier_labels_and_urls(self):
        self.assertEqual(source_label(SOURCES[1102]), 'Fuente verificada')
        self.assertEqual(source_label(SOURCES[2101]), 'Reporte / análisis atribuido')
        self.assertTrue(SOURCES[2101]['url'].startswith('https://x.com/'))

    def test_streamlit_structured_result_has_sections_sources_and_expandable_transparency(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py'), default_timeout=20).run()
        app.session_state['messages'] = [{
            'question': 'demo',
            'result': {
                'answer': 'Resumen', 'notice': '', 'sources': [SOURCES[1102], SOURCES[2101]],
                'traces': [], 'evidence': {}, 'presentation': validate_presentation(payload(), SOURCES),
            },
        }]
        app.sidebar.radio[0].set_value('Pregúntale al archivo').run()
        markdown = [item.value for item in app.markdown]
        for heading in ('## Lo documentado oficialmente', '## Lo reportado o analizado', '## Lo que todavía no puede establecerse', '## Conclusión', '## Fuentes utilizadas'):
            self.assertIn(heading, markdown)
        self.assertIn('**[S1102] · Fuente verificada**', markdown)
        self.assertIn('**[S2101] · Reporte / análisis atribuido**', markdown)
        self.assertIn('https://x.com/JSTapetillo/status/1968267797819265026', ''.join(markdown))
        self.assertEqual([item.label for item in app.expander], ['Ver consultas SQL · SELECT / solo lectura', 'Inspeccionar evidencia recuperada'])

    def test_streamlit_insufficient_state_is_clear(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py'), default_timeout=20).run()
        app.session_state['messages'] = [{
            'question': 'demo',
            'result': {'answer': 'Los registros disponibles en la base de datos no son suficientes para responder de forma confiable.', 'notice': '', 'sources': [], 'traces': [], 'evidence': {}, 'presentation': None},
        }]
        app.sidebar.radio[0].set_value('Pregúntale al archivo').run()
        self.assertEqual(app.error[0].value, 'Evidencia insuficiente')


if __name__ == '__main__':
    unittest.main()
