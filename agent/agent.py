import json
import os
import re
from openai import OpenAI, OpenAIError
from agent.prompts import PLANNER, ANSWER
from agent.sql_tools import fallback_plan, retrieve


def ask(question):
    spanish = bool(re.search(r'[¿¡áéíóúñ]|\b(qué|quién|cuando|antes|muestra|compara|sabía|agua|responsable|prometió)\b', question.lower()))
    insufficient = ('Los registros disponibles en la base de datos no son suficientes para responder de forma confiable.' if spanish else 'The available records in the database are not sufficient to answer this reliably.')
    result = {'answer': '', 'sources': [], 'traces': [], 'evidence': {}, 'notice': ''}
    client = OpenAI(timeout=25, max_retries=1) if os.getenv('OPENAI_API_KEY') else None
    plan = fallback_plan(question)
    model = os.getenv('OPENAI_MODEL', 'gpt-4.1-mini')
    if client:
        try:
            response = client.chat.completions.create(model=model, messages=[{'role':'system','content':PLANNER},{'role':'user','content':question}], response_format={'type':'json_object'}, temperature=0)
            proposed = json.loads(response.choices[0].message.content)
            if isinstance(proposed, dict) and isinstance(proposed.get('terms'), list) and (proposed.get('before_year') is None or isinstance(proposed.get('before_year'), int) and 1 <= proposed['before_year'] <= 9999):
                plan = proposed
        except (OpenAIError, ValueError, TypeError):
            result['notice'] = 'No se pudo usar el planificador; se utilizó la búsqueda local.'
    evidence, traces = retrieve(plan)
    result.update(traces=traces, evidence=evidence)
    if not evidence['events']:
        result['answer'] = insufficient
        return result
    if not client:
        result['answer'] = insufficient
        result['notice'] = 'Configura OPENAI_API_KEY para generar una síntesis. Puedes inspeccionar la evidencia recuperada y el SQL.'
        return result
    try:
        response = client.chat.completions.create(model=model, messages=[{'role':'system','content':ANSWER},{'role':'user','content':json.dumps({'question':question,'evidence':evidence},ensure_ascii=False)}], response_format={'type':'json_object'}, temperature=0)
        output = json.loads(response.choices[0].message.content)
        answer = output['answer']
        ids = output['source_ids']
        available = {s['id']:s for s in evidence['sources']}
        cited = {int(n) for n in re.findall(r'\[S(\d+)\]', answer)}
        if not isinstance(answer, str) or not isinstance(ids, list) or any(type(i) is not int for i in ids) or cited != set(ids) or not cited.issubset(available) or re.search(r'https?://', answer) or (not ids and answer.strip() != insufficient):
            raise ValueError('Unsupported citations or answer format')
        result['answer'] = answer
        result['sources'] = [available[i] for i in sorted(cited)]
    except (OpenAIError, ValueError, TypeError, KeyError):
        result['answer'] = insufficient
        result['notice'] = 'No se pudo generar una respuesta con citas válidas. La evidencia sigue disponible para revisión.'
    return result
