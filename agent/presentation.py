"""Validation and display metadata for structured agent answers."""
import re


CITATION_RE = re.compile(r'\s*\[S\d+\]')
DOCUMENTED_STATUSES = {'verified_document', 'documented_complaint', 'verified_official_statement'}
ATTRIBUTED_STATUSES = {
    'reviewed_journalism', 'reviewed_analysis', 'attributed_testimony',
    'verified_attribution',
}


def source_label(source):
    labels = {
        'verified_document': 'Documento verificado',
        'verified_official_statement': 'Declaración oficial verificada',
        'verified_attribution': 'Declaración verificada',
        'reviewed_journalism': 'Periodismo revisado',
        'reviewed_analysis': 'Análisis atribuido',
        'documented_complaint': 'Queja documentada',
        'attributed_testimony': 'Testimonio atribuido',
    }
    if source.get('evidence_status') in labels:
        return labels[source['evidence_status']]
    if source.get('evidence_tier') == 'attributed_reviewed':
        return 'Reporte / análisis atribuido'
    return 'Fuente verificada' if source.get('evidence_tier') == 'verified' or source.get('verified') == 1 else 'Material revisado atribuido'


def evidence_class(source):
    """Classify epistemic treatment from semantic status, not storage table."""
    status = source.get('evidence_status')
    if status in DOCUMENTED_STATUSES:
        return 'documented'
    if status in ATTRIBUTED_STATUSES:
        return 'attributed'
    # Compatibility for older records that predate evidence_status.
    if source.get('evidence_tier') == 'attributed_reviewed':
        return 'attributed'
    return 'documented' if source.get('evidence_tier') == 'verified' or source.get('verified') == 1 else 'attributed'


def is_attributed_or_reviewed(source):
    return evidence_class(source) == 'attributed'


def _clean_text(value):
    return CITATION_RE.sub('', value).strip()


def _finding_error(section, index, message):
    return f'{section}[{index}]: {message}'


def _validate_finding(row, section, index, expected_class, available):
    if not isinstance(row, dict):
        raise ValueError(_finding_error(section, index, 'must be an object'))
    required = ('date', 'title', 'text')
    if any(not isinstance(row.get(field), str) or not _clean_text(row[field]) for field in required):
        raise ValueError(_finding_error(section, index, 'missing required text'))
    source_ids = row.get('source_ids')
    if not isinstance(source_ids, list) or not source_ids or any(type(source_id) is not int for source_id in source_ids):
        raise ValueError(_finding_error(section, index, 'has invalid source IDs'))
    source_ids = sorted(set(source_ids))
    if any(source_id not in available for source_id in source_ids):
        raise ValueError(_finding_error(section, index, 'uses an unknown source ID'))
    if any(evidence_class(available[source_id]) != expected_class for source_id in source_ids):
        raise ValueError(_finding_error(section, index, 'mixes incompatible evidence classes'))
    limitation = row.get('limitation', '')
    if limitation is not None and not isinstance(limitation, str):
        raise ValueError(_finding_error(section, index, 'has an invalid limitation'))
    cleaned = {
        'date': _clean_text(row['date']),
        'title': _clean_text(row['title']),
        'text': _clean_text(row['text']),
        'source_ids': source_ids,
        'limitation': _clean_text(limitation) if limitation else '',
    }
    if expected_class == 'attributed':
        author = row.get('author')
        if not isinstance(author, str) or not _clean_text(author):
            raise ValueError(_finding_error(section, index, 'is missing attribution'))
        cleaned['author'] = _clean_text(author)
    return cleaned


def validate_presentation(output, available):
    """Return the safe subset of a structured response.

    Unsupported findings are omitted individually. The returned source set is
    authoritative: it is derived from the findings that passed validation,
    never from the model's top-level source list.
    """
    if not isinstance(output, dict):
        raise ValueError('Structured response must be an object')

    errors = []
    summary = output.get('summary')
    if not isinstance(summary, str) or not _clean_text(summary):
        errors.append('summary: missing or invalid')
        summary = 'La evidencia recuperada se presenta a continuación.'

    result = {
        'summary': _clean_text(summary),
        'verified_findings': [],
        'attributed_findings': [],
        'limitations': [],
        'validation_errors': errors,
    }
    used_ids = set()
    for section, expected_class, result_key in (
        ('verified_findings', 'documented', 'verified_findings'),
        ('attributed_findings', 'attributed', 'attributed_findings'),
    ):
        rows = output.get(section, [])
        if not isinstance(rows, list):
            errors.append(f'{section}: must be a list')
            continue
        for index, row in enumerate(rows):
            try:
                finding = _validate_finding(row, section, index, expected_class, available)
            except ValueError as error:
                errors.append(str(error))
                continue
            result[result_key].append(finding)
            used_ids.update(finding['source_ids'])

    limitations = output.get('limitations', [])
    if not isinstance(limitations, list):
        errors.append('limitations: must be a list')
    else:
        for index, limitation in enumerate(limitations):
            if not isinstance(limitation, str):
                errors.append(f'limitations[{index}]: must be text')
            elif _clean_text(limitation):
                result['limitations'].append(_clean_text(limitation))

    declared = output.get('source_ids', [])
    if declared is not None:
        if not isinstance(declared, list) or any(type(source_id) is not int for source_id in declared):
            errors.append('source_ids: must be an integer list')
        elif any(source_id not in available for source_id in declared):
            errors.append('source_ids: includes an unknown source ID')

    if errors and (result['verified_findings'] or result['attributed_findings']):
        result['limitations'].append('Algunas afirmaciones generadas se omitieron porque no pudieron validarse contra las fuentes recuperadas.')
    result['source_ids'] = sorted(used_ids)
    result['validation_errors'] = errors
    if not result['source_ids']:
        raise ValueError('; '.join(errors) or 'No supported findings')
    return result
