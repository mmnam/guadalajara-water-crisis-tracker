import html
from urllib.parse import urlparse
import pandas as pd
import streamlit as st
from database.db import initialize
from services import records
from agent.agent import ask

st.set_page_config(page_title='Memoria Hídrica GDL', page_icon='💧', layout='wide')
initialize()
st.markdown('''<style>
.block-container {max-width:1180px;padding-top:2rem} h1 {letter-spacing:-.05em}
[data-testid="stMetric"] {background:#eaf1ef;padding:18px;border-radius:12px}
[data-testid="stSidebar"] {border-right:1px solid #d3e2df}
</style>''', unsafe_allow_html=True)
st.sidebar.markdown('## 💧 Memoria Hídrica\n**GUADALAJARA · ARCHIVO PÚBLICO**')
page = st.sidebar.radio('Explorar el archivo', ['Línea del tiempo','Pregúntale al archivo','Comparar declaraciones','Compromisos','Fuentes y método'])
demo = st.sidebar.toggle('Mostrar datos de demostración', value=False)
st.sidebar.caption('La verificación es una revisión editorial de la fuente. No establece culpabilidad ni convierte una declaración en un hecho.')
st.title('Memoria Hídrica GDL')
st.markdown('**Una memoria verificable de cómo llegamos hasta aquí.**')
st.caption('Explora eventos, decisiones, advertencias, declaraciones y compromisos relacionados con la crisis del agua en Guadalajara.')
if demo:
    st.warning('MODO DEMO · Los registros marcados DEMO son ficticios. No describen hechos, instituciones ni responsabilidades reales. El agente siempre excluye estos registros.')


def source_link(source):
    url = source.get('url')
    label = source.get('title', source.get('source_title', 'Fuente'))
    if url and urlparse(url).scheme in ('https','http') and urlparse(url).netloc:
        st.markdown(f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(label)}</a>', unsafe_allow_html=True)
    else:
        st.caption(f'{label} · Sin enlace verificable; no sirve como evidencia histórica.')


def render_result(result):
    # Plain text keeps model-created markdown/links from becoming citation links.
    st.text(result['answer'])
    if result['notice']:
        st.info(result['notice'])
    st.markdown('**Fuentes utilizadas**')
    if not result['sources']:
        st.caption('No hay fuentes citadas en esta respuesta.')
    for s in result['sources']:
        status = 'Reporte / análisis atribuido' if s.get('evidence_tier') == 'attributed_reviewed' else 'Fuente verificada'
        st.caption(f"[S{s['id']}] · {status} · {s['publisher']} · {s['publication_date']}")
        source_link(s)
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
    st.subheader('El presente tiene una historia')
    base = records.timeline(demo=demo)
    cols = st.columns(3)
    year = cols[0].selectbox('Año', ['Todos'] + sorted({e['event_date'][:4] for e in base}))
    category = cols[1].selectbox('Categoría', ['Todas'] + sorted({e['category'] for e in base}))
    actor = cols[2].selectbox('Actor / institución', [None] + list(actor_names), format_func=lambda a: actor_names.get(a,'Todos'))
    events = records.timeline(None if year=='Todos' else year, None if category=='Todas' else category, actor, demo)
    c = st.columns(3)
    c[0].metric('Eventos en esta selección',len(events))
    c[1].metric('Años representados',len({e['event_date'][:4] for e in events}))
    c[2].metric('Eventos verificados',sum(e['verified'] for e in events))
    if not events:
        st.info('No hay eventos para esta selección. Ejecuta python seed_db.py y activa la demostración para explorar el MVP, o importa registros verificados.')
    for e in events:
        with st.container(border=True):
            st.caption(e['event_date'] + ' · ' + e['category'] + (' · DEMO' if not e['verified'] else ' · Verificado'))
            st.markdown('### ' + e['title'])
            st.write(e['description'])
            st.caption(e['location'] or '')
            involved = records.query('SELECT a.name FROM actors a JOIN event_actors ea ON ea.actor_id=a.id WHERE ea.event_id=?',(e['id'],))
            if involved:
                st.write('Actores: ' + ', '.join(a['name'] for a in involved))
            with st.expander('Contexto y fuentes'):
                st.write(e['significance'])
                for s in records.sources(e['id']):
                    source_link(s)
                    st.caption(s['reliability_notes'])
elif page == 'Pregúntale al archivo':
    st.subheader('Preguntas al archivo, respuestas con evidencia')
    st.caption('El agente separa evidencia verificada de reportes y análisis atribuidos revisados. La segunda capa no prueba por sí sola su afirmación subyacente. La búsqueda es acotada; no demuestra el primer aviso de toda la historia ni la ausencia de antecedentes.')
    suggestions = ['¿Quién sabía qué y cuándo?','¿Qué advertencias existían antes de 2026?','¿Qué prometió SIAPA?','Muéstrame eventos relacionados con Las Pintas.','¿Quién era responsable del tratamiento del agua?']
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
    st.subheader('Lo que se dijo, a través del tiempo')
    st.caption('Una declaración es una atribución documentada. Su contenido no se considera verdadero por haber sido expresado por una autoridad.')
    chosen = st.multiselect('Actores / instituciones', list(actor_names), format_func=lambda a: actor_names[a])
    rows = records.statements(chosen,demo)
    if not rows:
        st.info('Selecciona actores con declaraciones disponibles en este modo.')
    for row in rows:
        with st.container(border=True):
            st.caption(row['claim_date'] + (' · DEMO' if not row['verified'] else ' · Atribución verificada'))
            st.markdown('**' + row['name'] + '**')
            st.write(row['claim_text'])
            source_link(row)
elif page == 'Compromisos':
    st.subheader('De lo anunciado al seguimiento')
    rows = records.commitments(demo)
    groups = {'Cumplidos':['completed'],'Pendientes':['announced','in_progress'],'Retrasados / incumplidos':['delayed','unfulfilled'],'Estado desconocido':['unknown']}
    for col,(label,statuses) in zip(st.columns(4),groups.items()):
        col.metric(label,sum(r['status'] in statuses for r in rows))
    st.caption('El estado es editorial y requiere evidencia. Una fecha vencida no determina automáticamente un incumplimiento.')
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
    st.subheader('Evidencia que puedes inspeccionar')
    st.write('Este archivo separa hechos documentados, declaraciones atribuidas, responsabilidades institucionales y compromisos. La selección inicial es una demostración ficticia; no contiene una investigación histórica de Guadalajara.')
    st.write('Para incorporar historia real, conserva la URL original, la fecha, la atribución y las notas de revisión. Marca verified=1 solo después de revisar el documento. Una fuente que documenta una declaración no demuestra que esa declaración sea cierta.')
    st.info('La búsqueda del agente usa como máximo 25 eventos y 50 registros por entidad relacionada. El SQL se construye con plantillas y parámetros; el modelo no ejecuta SQL libre.')
    for source in records.query('SELECT * FROM sources' + ('' if demo else ' WHERE verified=1') + ' ORDER BY publication_date'):
        with st.container(border=True):
            st.caption(f"S{source['id']} · {source['source_type']} · " + ('Verificada' if source['verified'] else 'DEMO / no verificada'))
            source_link(source)
            st.write(source['reliability_notes'])
    if not demo:
        st.markdown('### Reportes y análisis atribuidos revisados')
        for material in records.attributed_material():
            with st.container(border=True):
                st.caption(f"[S{material['id']}] · Reporte / análisis atribuido · {material['source_type']}")
                source_link(material)
                st.write(material['paraphrase'])
                st.caption(material['review_notes'])
