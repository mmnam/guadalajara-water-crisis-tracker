"""Validation and display metadata for structured agent answers."""
import re


CITATION_RE = re.compile(r'\s*\[S\d+\]')


def source_label(source):
    return 'Reporte / análisis atribuido' if source.get('evidence_tier') == 'attributed_reviewed' else 'Fuente verificada'


def _clean_text(value):
    return CITATION_RE.sub('', value).strip()


def validate_presentation(output, available):
    """Return a safe, citation-clean presentation object or raise ValueError."""
    if not isinstance(output, dict) or 'summary' not in output:
        raise ValueError('No structured presentation')
    summary = output['summary']
    if not isinstance(summary, str) or not summary.strip():
        raise ValueError('Invalid summary')
    tier_specs = (
        ('verified_findings', False),
        ('attributed_findings', True),
    )
    result = {'summary': _clean_text(summary), 'verified_findings': [], 'attributed_findings': [], 'limitations': []}
    used_ids = set()
    for key, attributed in tier_specs:
        rows = output.get(key, [])
        if not isinstance(rows, list):
            raise ValueError(f'Invalid {key}')
        for row in rows:
            if not isinstance(row, dict):
                raise ValueError(f'Invalid {key} row')
            source_ids = row.get('source_ids')
            required = ('date', 'title', 'text')
            if any(not isinstance(row.get(field), str) or not row[field].strip() for field in required):
                raise ValueError(f'Missing {key} field')
            if not isinstance(source_ids, list) or not source_ids or any(type(source_id) is not int for source_id in source_ids):
                raise ValueError(f'Invalid {key} citations')
            if any(source_id not in available for source_id in source_ids):
                raise ValueError(f'Unknown {key} citation')
            if any((available[source_id].get('evidence_tier') == 'attributed_reviewed') != attributed for source_id in source_ids):
                raise ValueError(f'Wrong evidence tier in {key}')
            limitation = row.get('limitation')
            if limitation is not None and not isinstance(limitation, str):
                raise ValueError(f'Invalid {key} limitation')
            cleaned = {
                'date': _clean_text(row['date']), 'title': _clean_text(row['title']),
                'text': _clean_text(row['text']), 'source_ids': sorted(set(source_ids)),
                'limitation': _clean_text(limitation) if limitation else '',
            }
            if attributed:
                author = row.get('author')
                if not isinstance(author, str) or not author.strip():
                    raise ValueError('Attributed finding missing author')
                cleaned['author'] = _clean_text(author)
            result[key].append(cleaned)
            used_ids.update(source_ids)
    limitations = output.get('limitations', [])
    if not isinstance(limitations, list) or any(not isinstance(item, str) or not item.strip() for item in limitations):
        raise ValueError('Invalid limitations')
    result['limitations'] = [_clean_text(item) for item in limitations]
    declared = output.get('source_ids')
    if not isinstance(declared, list) or any(type(source_id) is not int for source_id in declared) or set(declared) != used_ids:
        raise ValueError('Structured citation set does not match findings')
    return result
