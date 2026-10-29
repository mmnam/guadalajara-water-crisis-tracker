import json
import logging
import os
import re

from openai import OpenAI, OpenAIError

from agent.presentation import evidence_class, validate_presentation
from agent.prompts import ANSWER, PLANNER
from agent.sql_tools import fallback_plan, retrieve


logger = logging.getLogger(__name__)


def asks_political_context(question):
    return bool(re.search(r'\b(partido|pol[ií]tic[oa]|administraci[oó]n|gobernaba)\b', question.lower()))


def has_explicit_political_context(evidence):
    records = evidence.get('attributed_evidence', []) + evidence.get('verified_evidence', {}).get('events', [])
    text = ' '.join(' '.join(str(value) for value in record.values() if value is not None) for record in records).lower()
    return bool(re.search(r'\b(partido|movimiento ciudadano|morena|pan|pri|prd|administraci[oó]n)\b', text))


def _evidence_counts(evidence):
    return {
        'verified_events': len(evidence.get('verified_evidence', {}).get('events', [])),
        'attributed_material': len(evidence.get('attributed_evidence', [])),
        'reviewed_usable_material': len(evidence.get('reviewed_evidence', [])),
        'sources': len(evidence.get('sources', [])),
    }


def _diagnostics(evidence, model, failure_category=None):
    sources = evidence.get('sources', [])
    return {
        'failure_category': failure_category,
        'model': model,
        'evidence_rows': _evidence_counts(evidence),
        'allowed_source_ids': sorted({source['id'] for source in sources}),
        'source_classes': {
            source['id']: {
                'evidence_class': evidence_class(source),
                'evidence_tier': source.get('evidence_tier'),
                'evidence_status': source.get('evidence_status'),
            }
            for source in sources
        },
    }


def _set_presentation(result, presentation, available):
    result['answer'] = presentation['summary']
    result['presentation'] = presentation
    result['sources'] = [available[source_id] for source_id in presentation['source_ids']]
    return result


def _validation_failure_category(errors):
    text = ' '.join(errors).lower()
    if any(term in text for term in ('source id', 'source_ids', 'citation', 'evidence classes')):
        return 'citation_validation_error'
    return 'presentation_validation_error'


def _deterministic_fallback(evidence, available):
    """Render retrieved records safely when automatic synthesis is unavailable."""
    findings = []
    event_sources = {}
    for link in evidence.get('event_sources', []):
        if link['source_id'] in available:
            event_sources.setdefault(link['event_id'], []).append(link['source_id'])

    for event in evidence.get('verified_evidence', {}).get('events', []):
        source_ids = sorted(set(event_sources.get(event['id'], [])))
        if source_ids:
            findings.append(('documented', {
                'date': event['event_date'],
                'title': event['title'],
                'text': event['description'],
                'source_ids': source_ids[:1],
                'limitation': event.get('significance') or '',
            }))
    for item in evidence.get('attributed_evidence', []):
        if item['id'] in available:
            findings.append(('attributed', {
                'date': item['publication_date'],
                'title': item['title'],
                'author': item['author'],
                'text': item['paraphrase'],
                'source_ids': [item['id']],
                'limitation': item.get('review_notes') or '',
            }))
    for item in evidence.get('reviewed_evidence', []):
        source_id = item['source_id']
        if source_id not in available:
            continue
        kind = evidence_class(available[source_id])
        finding = {
            'date': item['event_date'],
            'title': item['title'],
            'text': item['description'],
            'source_ids': [source_id],
            'limitation': item.get('key_limitation') or item.get('significance') or '',
        }
        if kind == 'attributed':
            finding['author'] = item.get('source_author') or item.get('publisher') or 'Fuente revisada'
        findings.append((kind, finding))

    presentation = {
        'summary': 'No fue posible generar la síntesis automática, pero la evidencia recuperada sí está disponible.',
        'verified_findings': [],
        'attributed_findings': [],
        'limitations': ['Cada registro conserva el alcance y los límites de su fuente; el material atribuido no prueba por sí solo su afirmación subyacente.'],
        'source_ids': [],
        'fallback': True,
    }
    for kind, finding in findings[:8]:
        presentation['verified_findings' if kind == 'documented' else 'attributed_findings'].append(finding)
        presentation['source_ids'].extend(finding['source_ids'])
    presentation['source_ids'] = sorted(set(presentation['source_ids']))
    return presentation


def _validate_legacy_answer(output, available, insufficient, event_sources):
    answer = output['answer']
    ids = output['source_ids']
    cited = {int(number) for number in re.findall(r'\[S(\d+)\]', answer)}
    valid_id_list = isinstance(ids, list) and all(type(item) is int for item in ids)
    if valid_id_list and not cited and ids and set(ids).issubset(available):
        answer = answer.rstrip() + ' ' + ''.join(f'[S{source_id}]' for source_id in sorted(set(ids)))
        cited = set(ids)
    # Older model outputs occasionally cite an event ID despite the prompt. Map
    # it only when that retrieved event has one retrieved source, so no source
    # is invented or selected ambiguously.
    if valid_id_list and cited and cited == set(ids) and not cited.issubset(available):
        sources_by_event = {}
        for link in event_sources:
            if link['source_id'] in available:
                sources_by_event.setdefault(link['event_id'], set()).add(link['source_id'])
        mapped = {}
        for event_id in cited:
            choices = sources_by_event.get(event_id, set())
            if len(choices) != 1:
                mapped = {}
                break
            mapped[event_id] = next(iter(choices))
        if mapped and len(mapped) == len(cited):
            answer = re.sub(r'\[S(\d+)\]', lambda match: f"[S{mapped[int(match.group(1))]}]", answer)
            cited = set(mapped.values())
            ids = sorted(cited)
    if not isinstance(answer, str) or not valid_id_list:
        raise ValueError('Invalid answer payload')
    attributed_ids = {source_id for source_id, source in available.items() if evidence_class(source) == 'attributed'}
    if cited & attributed_ids:
        lowered_answer = answer.lower()
        attribution = r'(report|señal|senal|aleg|afirm|observ|según|segun|an[aá]lis|testimonio|entrevist)'
        if not re.search(attribution, lowered_answer) or re.search(r'(está comprobado|esta comprobado|queda comprobado|se comprobó|se comprobo|proven that)', lowered_answer):
            raise ValueError('Attributed material lacks required attribution')
    if cited != set(ids) or not cited.issubset(available) or re.search(r'https?://', answer) or (not ids and answer.strip() != insufficient):
        raise ValueError('Unsupported citations or answer format')
    return answer, sorted(cited)


def _repair_presentation(client, model, raw_output, errors, diagnostics):
    repair_contract = {
        'instruction': 'Repair formatting and citation attribution only. Do not add new factual claims.',
        'validation_errors': errors,
        'allowed_source_ids': diagnostics['allowed_source_ids'],
        'source_classes': diagnostics['source_classes'],
        'required_schema': {
            'summary': 'short conclusion without citations',
            'verified_findings': '[{date,title,text,source_ids,limitation?}]',
            'attributed_findings': '[{date,title,author,text,source_ids,limitation?}]',
            'limitations': '[text]',
            'source_ids': '[integer]',
        },
        'previous_model_json': raw_output,
    }
    response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': ANSWER},
            {'role': 'user', 'content': json.dumps(repair_contract, ensure_ascii=False)},
        ],
        response_format={'type': 'json_object'},
    )
    content = response.choices[0].message.content
    return json.loads(content), content


def ask(question):
    spanish = bool(re.search(r'[¿¡áéíóúñ]|\b(qué|quién|cuando|antes|muestra|compara|sabía|agua|responsable|prometió)\b', question.lower()))
    insufficient = ('Los registros disponibles en la base de datos no son suficientes para responder de forma confiable.' if spanish else 'The available records in the database are not sufficient to answer this reliably.')
    model = os.getenv('OPENAI_MODEL', 'gpt-4.1-mini')
    result = {
        'answer': '', 'sources': [], 'traces': [], 'evidence': {}, 'notice': '',
        'presentation': None, 'diagnostics': {
            'failure_category': None, 'model': model, 'evidence_rows': {},
            'allowed_source_ids': [], 'source_classes': {},
        },
    }
    client = None
    if os.getenv('OPENAI_API_KEY'):
        try:
            client = OpenAI(timeout=25, max_retries=1)
        except (OpenAIError, ValueError, TypeError) as error:
            logger.exception('OpenAI client initialization failed: %s', error)
            result['notice'] = 'No se pudo completar la llamada al modelo. Revisa la configuración de OpenAI o los registros del despliegue.'
            result['diagnostics']['failure_category'] = 'openai_api_error'

    plan = fallback_plan(question)
    if client:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{'role': 'system', 'content': PLANNER}, {'role': 'user', 'content': question}],
                response_format={'type': 'json_object'},
            )
            proposed = json.loads(response.choices[0].message.content)
            allows_date_cutoff = bool(re.search(r'\b(antes de|before)\b', question.lower()))
            valid_date = isinstance(proposed, dict) and (
                proposed.get('before_date') is None or allows_date_cutoff
                and isinstance(proposed.get('before_date'), str)
                and re.fullmatch(r'\d{4}-\d{2}-\d{2}', proposed['before_date'])
            )
            if isinstance(proposed, dict) and isinstance(proposed.get('terms'), list) and (
                proposed.get('before_year') is None or isinstance(proposed.get('before_year'), int)
                and 1 <= proposed['before_year'] <= 9999
            ) and valid_date:
                plan = proposed
        except OpenAIError as error:
            logger.exception('OpenAI planner call failed: %s', error)
            result['notice'] = 'No se pudo completar la llamada al modelo. Revisa la configuración de OpenAI o los registros del despliegue.'
            result['diagnostics']['planner_failure'] = 'openai_api_error'
        except (json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
            logger.warning('Planner response was invalid; using local search: %s', error)
            result['notice'] = 'No se pudo usar el planificador; se utilizó la búsqueda local.'
            result['diagnostics']['planner_failure'] = 'invalid_model_json'

    evidence, traces = retrieve(plan)
    result.update(traces=traces, evidence=evidence)
    result['diagnostics'] = {
        **_diagnostics(evidence, model, result['diagnostics'].get('failure_category')),
        **({'planner_failure': result['diagnostics']['planner_failure']} if result['diagnostics'].get('planner_failure') else {}),
    }
    if asks_political_context(question) and not has_explicit_political_context(evidence):
        result['answer'] = insufficient
        result['notice'] = 'No hay evidencia verificada ni reporte atribuido revisado que identifique de forma explícita el partido o la administración solicitados.'
        result['diagnostics']['failure_category'] = 'insufficient_evidence'
        return result
    if not evidence['events'] and not evidence['attributed_evidence'] and not evidence.get('reviewed_evidence'):
        result['answer'] = insufficient
        result['diagnostics']['failure_category'] = 'insufficient_evidence'
        return result

    available = {source['id']: source for source in evidence['sources']}
    if not client:
        result['presentation'] = _deterministic_fallback(evidence, available)
        result['answer'] = result['presentation']['summary']
        result['sources'] = [available[source_id] for source_id in result['presentation']['source_ids']]
        result['notice'] = result['notice'] or 'Configura OPENAI_API_KEY para generar una síntesis. La evidencia recuperada sigue disponible.'
        result['diagnostics']['failure_category'] = result['diagnostics']['failure_category'] or 'openai_api_error'
        return result

    citation_contract = (
        'Citation contract: the only permitted source IDs are '
        + ', '.join(f'[S{source_id}]' for source_id in result['diagnostics']['allowed_source_ids'])
        + '. Event IDs are never citations. Each finding must use sources from one evidence class only.'
    )
    model_evidence = {
        'verified_evidence': evidence['verified_evidence'],
        'attributed_evidence': evidence['attributed_evidence'],
        'reviewed_evidence': evidence.get('reviewed_evidence', []),
        'scope': evidence['scope'],
    }
    raw_content = None
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': ANSWER},
                {'role': 'system', 'content': citation_contract},
                {'role': 'user', 'content': json.dumps({'question': question, 'evidence': model_evidence}, ensure_ascii=False)},
            ],
            response_format={'type': 'json_object'},
        )
        raw_content = response.choices[0].message.content
        output = json.loads(raw_content)
    except OpenAIError as error:
        logger.exception('OpenAI answer call failed: %s', error)
        result['notice'] = 'No se pudo completar la llamada al modelo. Revisa la configuración de OpenAI o los registros del despliegue.'
        result['diagnostics']['failure_category'] = 'openai_api_error'
    except (json.JSONDecodeError, TypeError, KeyError) as error:
        logger.warning('Invalid model JSON: %s; response=%r', error, raw_content)
        result['notice'] = 'La respuesta automática no tuvo un formato válido; se muestra la evidencia recuperada.'
        result['diagnostics']['failure_category'] = 'invalid_model_json'
    else:
        if isinstance(output, dict) and 'answer' in output and 'summary' not in output:
            try:
                answer, source_ids = _validate_legacy_answer(
                    output, available, insufficient, evidence['event_sources'],
                )
                result['answer'] = answer
                result['sources'] = [available[source_id] for source_id in source_ids]
                return result
            except (ValueError, TypeError, KeyError) as error:
                validation_errors = [str(error)]
                presentation = None
        else:
            try:
                presentation = validate_presentation(output, available)
                validation_errors = presentation['validation_errors']
                if not validation_errors:
                    return _set_presentation(result, presentation, available)
            except (ValueError, TypeError, KeyError) as error:
                presentation = None
                validation_errors = [str(error)]

        logger.warning(
            'Presentation validation failed: errors=%s response=%s permitted_source_ids=%s source_classes=%s',
            validation_errors, raw_content, result['diagnostics']['allowed_source_ids'], result['diagnostics']['source_classes'],
        )
        validation_category = _validation_failure_category(validation_errors)
        try:
            repaired_output, repaired_raw = _repair_presentation(
                client, model, output, validation_errors, result['diagnostics'],
            )
            repaired = validate_presentation(repaired_output, available)
            if not repaired['validation_errors']:
                return _set_presentation(result, repaired, available)
            logger.warning(
                'Presentation repair remained partial: errors=%s response=%s',
                repaired['validation_errors'], repaired_raw,
            )
            if presentation is None:
                presentation = repaired
        except OpenAIError as error:
            logger.exception('OpenAI presentation repair failed: %s', error)
            result['notice'] = 'No se pudo completar la llamada al modelo. Revisa la configuración de OpenAI o los registros del despliegue.'
            result['diagnostics']['failure_category'] = 'openai_api_error'
        except (json.JSONDecodeError, ValueError, TypeError, KeyError, StopIteration) as error:
            logger.warning('Presentation repair failed: %s', error)
            result['diagnostics']['failure_category'] = validation_category

        if presentation is not None:
            return _set_presentation(result, presentation, available)
        result['notice'] = result['notice'] or 'La respuesta automática no pudo validarse; se muestra la evidencia recuperada.'
        result['diagnostics']['failure_category'] = result['diagnostics']['failure_category'] or validation_category

    fallback = _deterministic_fallback(evidence, available)
    return _set_presentation(result, fallback, available)
