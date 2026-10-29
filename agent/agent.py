import json
import os
import re
from openai import OpenAI, OpenAIError
from agent.prompts import PLANNER, ANSWER
from agent.presentation import validate_presentation
from agent.sql_tools import fallback_plan, retrieve


def asks_political_context(question):
    return bool(re.search(r'\b(partido|pol[ií]tic[oa]|administraci[oó]n|gobernaba)\b', question.lower()))


def has_explicit_political_context(evidence):
    records = evidence.get('attributed_evidence', []) + evidence.get('verified_evidence', {}).get('events', [])
    text = ' '.join(' '.join(str(value) for value in record.values() if value is not None) for record in records).lower()
    return bool(re.search(r'\b(partido|movimiento ciudadano|morena|pan|pri|prd|administraci[oó]n)\b', text))


def ask(question):
    spanish = bool(re.search(r'[¿¡áéíóúñ]|\b(qué|quién|cuando|antes|muestra|compara|sabía|agua|responsable|prometió)\b', question.lower()))
    insufficient = ('Los registros disponibles en la base de datos no son suficientes para responder de forma confiable.' if spanish else 'The available records in the database are not sufficient to answer this reliably.')
    result = {'answer': '', 'sources': [], 'traces': [], 'evidence': {}, 'notice': '', 'presentation': None}
    client = OpenAI(timeout=25, max_retries=1) if os.getenv('OPENAI_API_KEY') else None
    plan = fallback_plan(question)
    model = os.getenv('OPENAI_MODEL', 'gpt-4.1-mini')
    if client:
        try:
            response = client.chat.completions.create(model=model, messages=[{'role':'system','content':PLANNER},{'role':'user','content':question}], response_format={'type':'json_object'}, temperature=0)
            proposed = json.loads(response.choices[0].message.content)
            allows_date_cutoff = bool(re.search(r'\b(antes de|before)\b', question.lower()))
            valid_date = isinstance(proposed, dict) and (proposed.get('before_date') is None or allows_date_cutoff and isinstance(proposed.get('before_date'), str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', proposed['before_date']))
            if isinstance(proposed, dict) and isinstance(proposed.get('terms'), list) and (proposed.get('before_year') is None or isinstance(proposed.get('before_year'), int) and 1 <= proposed['before_year'] <= 9999) and valid_date:
                plan = proposed
        except (OpenAIError, ValueError, TypeError):
            result['notice'] = 'No se pudo usar el planificador; se utilizó la búsqueda local.'
    evidence, traces = retrieve(plan)
    result.update(traces=traces, evidence=evidence)
    if asks_political_context(question) and not has_explicit_political_context(evidence):
        result['answer'] = insufficient
        result['notice'] = 'No hay evidencia verificada ni reporte atribuido revisado que identifique de forma explícita el partido o la administración solicitados.'
        return result
    if not evidence['events'] and not evidence['attributed_evidence'] and not evidence.get('reviewed_evidence'):
        result['answer'] = insufficient
        return result
    if not client:
        result['answer'] = insufficient
        result['notice'] = 'Configura OPENAI_API_KEY para generar una síntesis. Puedes inspeccionar la evidencia recuperada y el SQL.'
        return result
    try:
        allowed_source_ids = sorted(source['id'] for source in evidence['sources'])
        citation_contract = (
            'Citation contract: the only permitted source IDs are '
            + ', '.join(f'[S{source_id}]' for source_id in allowed_source_ids)
            + '. Event IDs are never citations. Every number in source_ids must exactly match a cited permitted source ID.'
        )
        model_evidence = {
            'verified_evidence': evidence['verified_evidence'],
            'attributed_evidence': evidence['attributed_evidence'],
            'reviewed_evidence': evidence.get('reviewed_evidence', []),
            'scope': evidence['scope'],
        }
        response = client.chat.completions.create(model=model, messages=[{'role':'system','content':ANSWER},{'role':'system','content':citation_contract},{'role':'user','content':json.dumps({'question':question,'evidence':model_evidence},ensure_ascii=False)}], response_format={'type':'json_object'}, temperature=0)
        output = json.loads(response.choices[0].message.content)
        available = {s['id']:s for s in evidence['sources']}
        if 'summary' in output:
            presentation = validate_presentation(output, available)
            result['answer'] = presentation['summary']
            result['presentation'] = presentation
            result['sources'] = [available[source_id] for source_id in sorted(set(output['source_ids']))]
            return result
        answer = output['answer']
        ids = output['source_ids']
        cited = {int(n) for n in re.findall(r'\[S(\d+)\]', answer)}
        valid_id_list = isinstance(ids, list) and all(type(i) is int for i in ids)
        # A JSON response can name valid sources yet omit inline markers. Attach
        # those same verified source markers rather than accepting an uncited
        # synthesis or inventing a source.
        if valid_id_list and not cited and ids and set(ids).issubset(available):
            answer = answer.rstrip() + ' ' + ''.join(f'[S{source_id}]' for source_id in sorted(set(ids)))
            cited = set(ids)
        # Some models echo an event ID despite the prompt. Repair that only when
        # the retrieved event has exactly one retrieved, verified source, so the
        # displayed citation still names a source document rather than an event.
        if valid_id_list and cited and cited == set(ids) and not cited.issubset(available):
            source_by_event = {}
            for link in evidence['event_sources']:
                if link['source_id'] in available:
                    source_by_event.setdefault(link['event_id'], set()).add(link['source_id'])
            mapped = {}
            for event_id in cited:
                choices = source_by_event.get(event_id, set())
                if len(choices) != 1:
                    mapped = {}
                    break
                mapped[event_id] = next(iter(choices))
            if mapped and len(mapped) == len(cited):
                answer = re.sub(r'\[S(\d+)\]', lambda match: f"[S{mapped[int(match.group(1))]}]", answer)
                ids = sorted(set(mapped.values()))
                cited = set(ids)
        if not isinstance(answer, str) or not valid_id_list:
            raise ValueError('Invalid answer payload')
        attributed_ids = {source['id'] for source in evidence['sources'] if source.get('evidence_tier') in ('attributed_reviewed', 'reviewed_usable')}
        if cited & attributed_ids:
            lowered_answer = answer.lower()
            attribution = r'(report|señal|senal|aleg|afirm|observ|según|segun|an[aá]lis|testimonio|entrevist)'
            if not re.search(attribution, lowered_answer) or re.search(r'(está comprobado|esta comprobado|queda comprobado|se comprobó|se comprobo|proven that)', lowered_answer):
                raise ValueError('Attributed material lacks required attribution')
        if not isinstance(answer, str) or not valid_id_list or cited != set(ids) or not cited.issubset(available) or re.search(r'https?://', answer) or (not ids and answer.strip() != insufficient):
            raise ValueError('Unsupported citations or answer format')
        result['answer'] = answer
        result['sources'] = [available[i] for i in sorted(cited)]
    except (OpenAIError, ValueError, TypeError, KeyError):
        result['answer'] = insufficient
        result['notice'] = 'No se pudo generar una respuesta con citas válidas. La evidencia sigue disponible para revisión.'
    return result
