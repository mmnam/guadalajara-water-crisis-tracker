import html
import logging
import os
from urllib.parse import urlparse
import pandas as pd
import streamlit as st
from database.db import connect
from database.seed import bootstrap
from services import records
from agent.agent import ask
from agent.presentation import source_label

st.set_page_config(page_title='Memoria Hídrica GDL', page_icon='💧', layout='wide')
logger = logging.getLogger(__name__)
bootstrap()
try:
    with connect(read_only=True) as conn:
        startup_counts = {
            'verified_events': conn.execute('SELECT count(*) FROM events WHERE verified=1').fetchone()[0],
            'attributed_material': conn.execute('SELECT count(*) FROM attributed_material').fetchone()[0],
            'reviewed_usable_material': conn.execute('SELECT count(*) FROM usable_evidence').fetchone()[0],
        }
    logger.info(
        'OPENAI_API_KEY configured: %s; OPENAI_MODEL: %s; verified events: %s; attributed material: %s; reviewed usable material: %s',
        'yes' if os.getenv('OPENAI_API_KEY') else 'no',
        os.getenv('OPENAI_MODEL', 'gpt-4.1-mini'),
        startup_counts['verified_events'],
        startup_counts['attributed_material'],
        startup_counts['reviewed_usable_material'],
    )
except Exception:
    logger.exception('Database bootstrap verification failed')
st.markdown('''<style>
.stApp {background:#f6f3ee;color:#263840}
.block-container {max-width:1180px;padding:1.25rem 1.25rem 3.5rem}
h1,h2,h3 {color:#103d4c;letter-spacing:-.035em}
h2 {margin-top:1.8rem!important}
p,li,[data-testid="stCaptionContainer"] {color:#44535b}
[data-testid="stSidebar"] {background:#103d4c;border-right:1px solid #1e6f78}
[data-testid="stSidebar"] * {color:#f6f3ee}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {color:#c8dadd}
[data-testid="stSidebar"] [data-testid="stRadio"] label {border-radius:8px;padding:.28rem .4rem}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {background:rgba(255,255,255,.1)}
[data-testid="stSidebar"] [data-testid="stRadio"] [data-checked="true"] + div {font-weight:700}
.archive-hero {position:relative;overflow:hidden;margin:.3rem 0 2rem;padding:2.2rem 2.35rem 2rem;border-radius:18px;background:linear-gradient(125deg,#103d4c 0%,#185968 58%,#1e6f78 100%);box-shadow:0 10px 28px rgba(16,61,76,.16);color:#f6f3ee}
.archive-hero:after {content:"";position:absolute;inset:-30% -10% auto 48%;height:190%;opacity:.32;background:repeating-linear-gradient(90deg,transparent 0 28px,rgba(255,255,255,.1) 29px 30px),linear-gradient(135deg,transparent 42%,rgba(75,163,195,.7) 43% 45%,transparent 46%);transform:rotate(9deg);pointer-events:none}
.archive-kicker,.sidebar-kicker {position:relative;z-index:1;color:#b7dfe7!important;font-size:.74rem;font-weight:750;letter-spacing:.11em;text-transform:uppercase}
.archive-hero h1 {position:relative;z-index:1;margin:.25rem 0 .45rem!important;color:#f6f3ee!important;font-family:Georgia,"Times New Roman",serif;font-size:clamp(2.25rem,5vw,4rem);letter-spacing:-.055em}
.archive-hero p {position:relative;z-index:1;max-width:720px;margin:.25rem 0;color:#e3eff0!important;font-size:1.05rem}
.archive-hero .archive-deck {font-size:1.22rem;line-height:1.45}
.sidebar-brand {padding:.7rem .25rem 1.1rem;border-bottom:1px solid rgba(227,232,234,.28);margin-bottom:1.2rem}
.sidebar-brand h2 {color:#f6f3ee!important;margin:.15rem 0!important;font-family:Georgia,"Times New Roman",serif}
.sidebar-note {margin-top:1.4rem;padding:.8rem .85rem;border-left:3px solid #d9a441;background:rgba(255,255,255,.08);border-radius:0 8px 8px 0;font-size:.82rem;line-height:1.42}
[data-testid="stMetric"] {background:#e3e8ea;padding:17px;border:1px solid #ccd8da;border-radius:12px}
[data-testid="stMetric"] [data-testid="stMetricValue"] {color:#103d4c}
[data-testid="stVerticalBlockBorderWrapper"] {border-color:#d3dedd!important;background:rgba(255,255,255,.5);border-radius:12px!important;box-shadow:0 2px 10px rgba(16,61,76,.045)}
[data-testid="stExpander"] {background:rgba(255,255,255,.54);border:1px solid #d3dedd;border-radius:10px}
.section-kicker {color:#1e6f78!important;font-size:.77rem;font-weight:760;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.15rem}
.section-intro {max-width:780px;font-size:1.02rem;line-height:1.5;margin-bottom:1.1rem}
.evidence-badge {display:inline-block;border-radius:999px;padding:.22rem .58rem;font-size:.75rem;font-weight:750;letter-spacing:.015em}
.badge-verified {color:#0e4c55;background:#d5e9e5;border:1px solid #8bbeb7}
.badge-attributed {color:#754115;background:#f3e4c7;border:1px solid #d9a441}
.badge-unresolved {color:#66423b;background:#f0ddd4;border:1px solid #b86a40}
.badge-neutral {color:#314951;background:#e3e8ea;border:1px solid #b9c8cb}
.finding-label {margin-bottom:.55rem}
.finding-meta {color:#52666c!important;font-weight:650;margin:.1rem 0 .35rem}
.uncertainty-box {margin:.7rem 0 0;padding:.65rem .8rem;border-left:3px solid #b86a40;background:#fbf0eb;border-radius:0 7px 7px 0;color:#66423b;font-size:.92rem}
.answer-lede {padding:.85rem 1rem;border-left:4px solid #4ba3c3;background:#e8f2f3;border-radius:0 9px 9px 0;color:#284b56;margin-bottom:1.1rem}
.timeline-marker {border-left:2px solid #4ba3c3;margin:1.05rem 0 0 .55rem;padding:0 0 .45rem 1.2rem;position:relative}
.timeline-marker:before {content:"";position:absolute;left:-.48rem;top:.25rem;width:.78rem;height:.78rem;background:#f6f3ee;border:3px solid #1e6f78;border-radius:50%}
.timeline-date {color:#1e6f78!important;font-size:.82rem;font-weight:800;letter-spacing:.055em;text-transform:uppercase}
.source-card-title {margin:.45rem 0 .12rem;color:#103d4c!important;font-weight:760}
.method-card {min-height:144px;padding:.95rem 1rem;border-top:4px solid #1e6f78;background:rgba(255,255,255,.58);border-radius:9px}
.method-card h3 {margin:.15rem 0 .35rem!important;font-size:1.03rem}
.method-card p {font-size:.9rem;line-height:1.45}
.commitment-note {padding:.7rem .9rem;border-left:3px solid #d9a441;background:#faf4e7;border-radius:0 8px 8px 0}
@media (max-width: 700px) {.archive-hero{padding:1.65rem 1.35rem}.archive-hero h1{font-size:2.35rem}.block-container{padding-left:1rem;padding-right:1rem}}
</style>''', unsafe_allow_html=True)
st.sidebar.markdown('''<div class="sidebar-brand"><div class="sidebar-kicker">Archivo público</div><h2>Memoria Hídrica</h2><div class="sidebar-kicker">Guadalajara · crisis del agua</div></div>''', unsafe_allow_html=True)
st.sidebar.markdown('#### Navegación del archivo')
page = st.sidebar.radio('Explorar el archivo', ['Línea del tiempo','Pregúntale al archivo','Comparar declaraciones','Compromisos','Fuentes y método'])
st.sidebar.markdown('#### Controles de lectura')
demo = st.sidebar.toggle('Mostrar datos de demostración', value=False)
st.sidebar.markdown('<div class="sidebar-note">La verificación es una revisión editorial de la fuente. No establece culpabilidad ni convierte una declaración en un hecho.</div>', unsafe_allow_html=True)
st.markdown('''<section class="archive-hero"><div class="archive-kicker">Zona Metropolitana de Guadalajara · Archivo público</div><h1>Memoria Hídrica GDL</h1><p class="archive-deck">Explora todo el contexto: una memoria verificable de cómo llegamos hasta aquí. Combatiendo la "memoria de pez" </p><p>Eventos, advertencias, decisiones, declaraciones y compromisos sobre la crisis del agua. Por que la historia no comienza cada que nos despertamos. Cada registro conserva su fuente, atribución y límites de evidencia.</p></section>''', unsafe_allow_html=True)
if demo:
    st.warning('MODO DEMO · Los registros marcados DEMO son ficticios. No describen hechos, instituciones ni responsabilidades reales. El agente siempre excluye estos registros.')


def source_link(source):
    url = source.get('url')
    label = source.get('title', source.get('source_title', 'Fuente'))
    if url and urlparse(url).scheme in ('https','http') and urlparse(url).netloc:
        st.markdown(f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(label)}</a>', unsafe_allow_html=True)
    else:
        st.caption(f'{label} · Sin enlace verificable; no sirve como evidencia histórica.')


def citation_labels(source_ids):
    return ' · '.join(f'[S{source_id}]' for source_id in source_ids)


def evidence_badge(label, kind):
    st.markdown(f'<span class="evidence-badge badge-{kind}">{html.escape(label)}</span>', unsafe_allow_html=True)


def category_label(category):
    labels = {
        'public_complaint': 'Queja pública',
        'institutional_warning': 'Advertencia institucional',
        'formal_notification': 'Notificación formal',
        'government_action': 'Acción gubernamental',
        'official_statement': 'Declaración oficial',
        'investigation': 'Investigación',
        'recommendation': 'Recomendación',
        'reviewed_journalism': 'Periodismo revisado',
        'reviewed_analysis': 'Análisis de especialista',
        'attributed_testimony': 'Testimonio atribuido',
        'verified_attribution': 'Declaración verificada',
    }
    return labels.get(category, category.replace('_', ' ').capitalize())


def status_label(status):
    return {
        'verified_document': 'Documento verificado',
        'verified_official_statement': 'Declaración oficial',
        'verified_attribution': 'Declaración verificada',
        'reviewed_journalism': 'Periodismo revisado',
        'reviewed_analysis': 'Análisis atribuido',
        'documented_complaint': 'Queja documentada',
        'attributed_testimony': 'Testimonio atribuido',
        'unresolved': 'No establecido',
    }.get(status, category_label(status))


def status_badge_kind(status):
    if status in ('verified_document', 'verified_official_statement', 'documented_complaint'):
        return 'verified'
    if status == 'unresolved':
        return 'unresolved'
    return 'attributed'


def render_finding(finding, label, kind, source=None):
    with st.container(border=True):
        st.markdown('<div class="finding-label">', unsafe_allow_html=True)
        evidence_badge(label, kind)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f"<div class=\"finding-meta\">{html.escape(finding['date'])}</div>", unsafe_allow_html=True)
        st.markdown(f"#### {finding['title']}")
        if finding.get('author'):
            st.write(f"**Autor / fuente:** {finding['author']}")
        st.write(finding['text'])
        st.caption('Citas: ' + citation_labels(finding['source_ids']))
        if source:
            source_link(source)
        if finding.get('limitation'):
            st.markdown(f'<div class="uncertainty-box"><strong>Límite de evidencia.</strong> {html.escape(finding["limitation"])}</div>', unsafe_allow_html=True)


def render_result(result):
    presentation = result.get('presentation')
    if presentation:
        source_by_id = {source['id']: source for source in result['sources']}
        if presentation.get('fallback'):
            st.markdown('## Evidencia recuperada')
            st.info('No fue posible generar la síntesis automática, pero la evidencia recuperada sí está disponible.')
        else:
            st.markdown('<div class="answer-lede"><strong>Lectura guiada del archivo.</strong> La respuesta conserva separadas la documentación institucional y el material atribuido revisado; las citas permiten volver a cada fuente.</div>', unsafe_allow_html=True)
        if presentation['verified_findings']:
            st.markdown('### Lo documentado oficialmente' if presentation.get('fallback') else '## Lo documentado oficialmente')
            for finding in presentation['verified_findings']:
                source = source_by_id.get(finding['source_ids'][0])
                render_finding(finding, source_label(source) if source else 'Fuente verificada', 'verified', source)
        if presentation['attributed_findings']:
            st.markdown('### Lo reportado o analizado' if presentation.get('fallback') else '## Lo reportado o analizado')
            for finding in presentation['attributed_findings']:
                source = source_by_id.get(finding['source_ids'][0])
                render_finding(finding, source_label(source) if source else 'Reporte / análisis atribuido', 'attributed', source)
        if presentation['limitations']:
            st.markdown('### Lo que todavía no puede establecerse' if presentation.get('fallback') else '## Lo que todavía no puede establecerse')
            for limitation in presentation['limitations']:
                st.markdown(f'<div class="uncertainty-box">{html.escape(limitation)}</div>', unsafe_allow_html=True)
        if not presentation.get('fallback'):
            st.markdown('## Conclusión')
            st.write(presentation['summary'])
    elif not result['sources'] and 'no son suficientes' in result['answer'].lower():
        st.error('Evidencia insuficiente')
        st.write('El corpus actual no contiene información suficiente para responder esta pregunta de forma confiable.')
    else:
        # Legacy safe fallback for older model output.
        st.write(result['answer'])
    if result['notice']:
        st.info(result['notice'])
    st.markdown('## Fuentes utilizadas')
    if not result['sources']:
        st.caption('No hay fuentes citadas en esta respuesta.')
    for s in result['sources']:
        with st.container(border=True):
            evidence_badge(source_label(s), 'verified' if s.get('evidence_tier') == 'verified' or s.get('verified') else status_badge_kind(s.get('evidence_status')))
            st.markdown(f"**[S{s['id']}] · {source_label(s)}**")
            st.caption(f"{s['publisher']} · {s['publication_date']} · {s['source_type']}")
            source_link(s)
            if s.get('reliability_notes'):
                st.caption(s['reliability_notes'])
    diagnostics = result.get('diagnostics', {})
    if diagnostics.get('failure_category'):
        with st.expander('Diagnóstico técnico'):
            st.write({
                'categoría de fallo': diagnostics['failure_category'],
                'modelo': diagnostics.get('model'),
                'filas de evidencia recuperadas': diagnostics.get('evidence_rows', {}),
                'IDs de fuente permitidos': diagnostics.get('allowed_source_ids', []),
            })
    with st.expander('Ver consultas SQL · SELECT / solo lectura'):
        for trace in result['traces']:
            st.code(trace['sql'], language='sql')
            st.write({'parámetros':trace['parameters'],'filas':trace['rows']})
    with st.expander('Inspeccionar evidencia recuperada'):
        if result['evidence'].get('verified_evidence', {}).get('events'):
            st.caption('Evidencia verificada')
            st.dataframe(pd.DataFrame(result['evidence']['verified_evidence']['events']), hide_index=True, use_container_width=True)
        if result['evidence'].get('attributed_evidence'):
            st.caption('Reporte / análisis atribuido')
            st.dataframe(pd.DataFrame(result['evidence']['attributed_evidence']), hide_index=True, use_container_width=True)
        st.json(result['evidence'])


all_actors = records.actors()
actor_names = {a['id']:a['name'] for a in all_actors}
if page == 'Línea del tiempo':
    st.markdown('<div class="section-kicker">Rastro histórico</div>', unsafe_allow_html=True)
    st.header('El presente tiene una historia')
    st.markdown('<p class="section-intro">Una cronología para situar qué se documentó, qué se dijo y qué quedó pendiente antes y durante la crisis. Cada ficha conserva la fuente y sus límites.</p>', unsafe_allow_html=True)
    base = records.timeline(demo=demo)
    timeline_actor_names = sorted({name.strip() for event in base for name in (event.get('actor_names') or '').split('|') if name.strip()})
    status_options = ['Todos'] + sorted({event['evidence_status'] for event in base})
    source_type_options = ['Todos'] + sorted({event.get('source_type') for event in base if event.get('source_type')})
    with st.container(border=True):
        st.markdown('<div class="section-kicker">Filtrar la cronología</div>', unsafe_allow_html=True)
        cols = st.columns(5)
        year = cols[0].selectbox('Año', ['Todos'] + sorted({e['event_date'][:4] for e in base}))
        category = cols[1].selectbox('Categoría', ['Todas'] + sorted({e['category'] for e in base}), format_func=lambda value: 'Todas' if value == 'Todas' else category_label(value))
        evidence_status = cols[2].selectbox('Tipo de evidencia', status_options, format_func=lambda value: 'Todos' if value == 'Todos' else status_label(value))
        actor = cols[3].selectbox('Actor / institución', ['Todos'] + timeline_actor_names)
        source_type = cols[4].selectbox('Tipo de fuente', source_type_options, format_func=lambda value: 'Todos' if value == 'Todos' else value.replace('_', ' '))
    events = records.timeline(
        None if year=='Todos' else year, None if category=='Todas' else category,
        None if actor=='Todos' else actor, demo,
        None if evidence_status=='Todos' else evidence_status,
        None if source_type=='Todos' else source_type,
    )
    c = st.columns(4)
    c[0].metric('Registros en esta selección',len(events))
    c[1].metric('Años representados',len({e['event_date'][:4] for e in events}))
    c[2].metric('Documentos / actuaciones verificadas',sum(e['evidence_tier'] == 'verified' for e in events))
    c[3].metric('Reportes, análisis y testimonios revisados',sum(e['evidence_tier'] != 'verified' for e in events))
    if not events:
        st.info('No hay eventos para esta selección. Ejecuta python seed_db.py y activa la demostración para explorar el MVP, o importa registros verificados.')
    for e in events:
        st.markdown(f'<div class="timeline-marker"><div class="timeline-date">{html.escape(e["event_date"])} · {html.escape(status_label(e["evidence_status"]))}</div></div>', unsafe_allow_html=True)
        with st.container(border=True):
            evidence_badge(status_label(e['evidence_status']), status_badge_kind(e['evidence_status']))
            demo_marker = ' · DEMO' if e['record_kind'] == 'verified' and not e['verified'] else ''
            st.caption(e['event_date'] + ' · ' + category_label(e['category']) + (demo_marker or ' · ' + e['evidence_tier']))
            st.markdown('### ' + e['title'])
            st.write(e['description'])
            st.caption(e['location'] or '')
            if e.get('actor_names'):
                st.write('Actores: ' + e['actor_names'].replace(' | ', ', '))
            with st.expander('Contexto y fuentes'):
                st.write(e['significance'])
                if e['record_kind'] == 'verified':
                    for s in records.sources(e['id']):
                        source_link(s)
                        st.caption(s['reliability_notes'])
                else:
                    source_link({'title': e['source_title'], 'url': e['url']})
                    st.caption(e['reliability_notes'])
                    st.markdown(f'<div class="uncertainty-box"><strong>Límite de evidencia.</strong> {html.escape(e["key_limitation"])}</div>', unsafe_allow_html=True)
elif page == 'Pregúntale al archivo':
    st.markdown('<div class="section-kicker">Consulta documental</div>', unsafe_allow_html=True)
    st.header('Preguntas al archivo, respuestas con evidencia')
    st.markdown('<p class="section-intro">El agente separa evidencia verificada de reportes y análisis atribuidos revisados. La segunda capa no prueba por sí sola su afirmación subyacente. La búsqueda es acotada: no demuestra por sí misma el primer aviso de toda la historia ni la ausencia de antecedentes.</p>', unsafe_allow_html=True)
    suggestions = ['¿Quién sabía qué y cuándo?','Muéstrame eventos relacionados con Las Pintas.','¿Qué se sabía sobre problemas en Arroyo Seco antes de la crisis de octubre de 2026, tanto en documentos oficiales como en análisis de especialistas?']
    selected = None
    for i,q in enumerate(suggestions):
        if st.button(q, type='primary' if i==0 else 'secondary'):
            selected = q
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message('user'):
            st.write(message['question'])
        with st.chat_message('assistant'):
            render_result(message['result'])
    question = st.chat_input('Pregunta por un evento, una institución o un compromiso…') or selected
    if question:
        with st.chat_message('user'):
            st.write(question)
        with st.chat_message('assistant'):
            with st.spinner('Consultando el archivo…'):
                result = ask(question)
            render_result(result)
        st.session_state.messages.append({'question':question,'result':result})
elif page == 'Comparar declaraciones':
    st.markdown('<div class="section-kicker">Registro de posiciones</div>', unsafe_allow_html=True)
    st.header('Lo que se dijo, a través del tiempo')
    st.markdown('<p class="section-intro">Una declaración es una atribución documentada. Su contenido no se considera verdadero por haber sido expresado por una autoridad.</p>', unsafe_allow_html=True)
    chosen = st.multiselect('Actores / instituciones', list(actor_names), format_func=lambda a: actor_names[a])
    rows = records.statements(chosen,demo)
    if not rows:
        st.info('Selecciona actores con declaraciones disponibles en este modo.')
    for row in rows:
        with st.container(border=True):
            evidence_badge('Atribución documentada' if row['verified'] else 'No establecido / DEMO', 'verified' if row['verified'] else 'unresolved')
            st.caption(row['claim_date'] + (' · DEMO' if not row['verified'] else ' · Atribución verificada'))
            st.markdown('**' + row['name'] + '**')
            st.write(row['claim_text'])
            source_link(row)
elif page == 'Compromisos':
    st.markdown('<div class="section-kicker">Seguimiento público</div>', unsafe_allow_html=True)
    st.header('De lo anunciado al seguimiento')
    rows = records.commitments(demo)
    groups = {'Cumplidos':['completed'],'Pendientes':['announced','in_progress'],'Retrasados / incumplidos':['delayed','unfulfilled'],'Estado desconocido':['unknown']}
    for col,(label,statuses) in zip(st.columns(4),groups.items()):
        col.metric(label,sum(r['status'] in statuses for r in rows))
    st.markdown('<div class="commitment-note">El estado es editorial y requiere evidencia. Una fecha vencida no determina automáticamente un incumplimiento.</div>', unsafe_allow_html=True)
    status = st.selectbox('Filtrar estado',['Todos','announced','in_progress','completed','delayed','unfulfilled','unknown'])
    shown = [r for r in rows if status=='Todos' or r['status']==status]
    if not shown:
        st.info('No hay compromisos disponibles para esta selección.')
    for row in shown:
        with st.expander(f"{row['commitment_date']} · {row['name']} · {row['status']}" + (' · DEMO' if not row['verified'] else '')):
            st.write(row['commitment'])
            st.write('Plazo: ' + (row['deadline'] or 'No documentado'))
            st.write('Evento relacionado: ' + (row['event_title'] or 'No vinculado'))
            source_link(row)
else:
    st.markdown('<div class="section-kicker">Método y trazabilidad</div>', unsafe_allow_html=True)
    st.header('Evidencia que puedes inspeccionar')
    st.markdown('<p class="section-intro">El archivo separa hechos documentados, declaraciones atribuidas, responsabilidades institucionales y compromisos. No transforma una afirmación en un hecho por estar publicada o por venir de una autoridad.</p>', unsafe_allow_html=True)
    method_columns = st.columns(3)
    method_cards = [
        ('Fuente verificada', 'badge-verified', 'Documento o registro revisado editorialmente. Puede respaldar lo que el documento establece, no conclusiones que no contiene.'),
        ('Reporte / análisis atribuido', 'badge-attributed', 'Periodismo o análisis técnico revisado y citado. Se presenta como lo que sus autores o entrevistados reportaron, no como hecho probado.'),
        ('No establecido', 'badge-unresolved', 'Hipótesis, vacíos, conflictos y datos de demostración. No entran como evidencia del agente ni se presentan como antecedentes comprobados.'),
    ]
    for col, (title, badge_class, text) in zip(method_columns, method_cards):
        with col:
            st.markdown(f'<div class="method-card"><span class="evidence-badge {badge_class}">{title}</span><h3>{title}</h3><p>{text}</p></div>', unsafe_allow_html=True)
    st.markdown('### Criterio editorial')
    st.write('Para incorporar historia real, conserva la URL original, la fecha, la atribución y las notas de revisión. Marca verified=1 solo después de revisar el documento. Una fuente que documenta una declaración no demuestra que esa declaración sea cierta.')
    st.info('La búsqueda del agente usa como máximo 25 eventos y 50 registros por entidad relacionada. El SQL se construye con plantillas y parámetros; el modelo no ejecuta SQL libre.')
    for source in records.usable_sources():
        with st.container(border=True):
            evidence_badge(source_label(source), status_badge_kind(source.get('evidence_status')))
            st.caption(f"S{source['id']} · {source['source_type']} · {source_label(source)}")
            st.markdown(f"**{source['title']}**")
            if source.get('author'):
                st.caption(f"{source['author']} · {source.get('publisher', '')} · {source.get('publication_date', '')}")
            source_link(source)
            st.write(source['reliability_notes'])
            if source.get('key_limitation'):
                st.caption('Límite: ' + source['key_limitation'])
