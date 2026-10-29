# Guía de revisión · Memoria Hídrica GDL

**Corte de investigación: 28 de octubre de 2026.** `candidate_records.json` sigue siendo una capa de candidatos: todos sus registros permanecen `verified=0`. La primera importación controlada aprobó únicamente E1201, E1202, E1204, E1205, E1206, E1211, E1222, E1212, E1219, E1217, E1218 y E1220 en la representación separada [`approved_records.json`](approved_records.json); su alcance y límites están en [`APPROVED_RECORDS.md`](APPROVED_RECORDS.md). La fecha de una recomendación posterior no es la fecha de los expedientes anteriores que reproduce.

## Cómo revisar y aprobar

1. Abra las fuentes originales y compruebe en la ubicación indicada la fecha, alcance, actor y atribución. Los enlaces con acceso `snippet_only` o `link_only` requieren abrir el texto completo.
2. Distinga el documento que recoge una denuncia, la denuncia misma, el conocimiento institucional y el conocimiento personal. Corrobore afirmaciones técnicas y políticas con documentación independiente.
3. Revise cada declaración, relación, responsabilidad y compromiso en el JSON. `unknown` significa que no se comprobó el estado; no supone incumplimiento.
4. La aprobación debe ser expresa y por registro. Este JSON incorpora metadatos de investigación que el importador actual no acepta; antes de una futura importación habrá que revisar IDs, eliminar metadatos, establecer campos compatibles y promover únicamente registros y fuentes aprobados. No usar `seed_db.py --file` directamente con este archivo.
5. Las fuentes cuya publicación sea posterior al hecho (especialmente recomendaciones de 2022 y 2026) son fuentes retrospectivas, no evidencia de publicidad de sus detalles en la fecha del hecho.

## Prioridad alta: revisar primero

Los candidatos 1201, 1202, 1204, 1205, 1211, 1212, 1217, 1218 y 1220 tienen respaldo de las recomendaciones primarias de CEDHJ. Revisar después 1214 (advertencias atribuidas al personal), 1221 (muestras ciudadanas), 1223 (cierre y explicación oficial) y 1227 (plan). Ninguno está aprobado.

## Subconjunto habilitado como evidencia atribuida revisada

El archivo `attributed_reviewed_records.json` selecciona solamente material que esta guía documenta como leído directamente o revisado de forma sustantiva. No aprueba los hechos subyacentes ni promueve automáticamente otros candidatos `verified=0`.

- A2101: hilo original de @JSTapetillo del 17 de septiembre de 2025 sobre Arroyo Seco; diagnóstico y alegaciones, sin expediente ni peritaje.
- A2102: post original de @jcrtoral del 13 de abril de 2026; observación visual periodística en El Nixticuil y testimonios atribuidos.
- A2103: reportaje de Mario Marlo/ZonaDocs del 13 de marzo de 2026; testimonios atribuidos de personal de SIAPA.
- A2104: reportaje de Violeta Meléndez/UDG Noticias del 13 de marzo de 2026; resultados reportados de un PDF oficial no recuperado.
- A2105: post original de @JSTapetillo del 4 de octubre de 2026; análisis de un supuesto pico y una queja citada, sin análisis de laboratorio.
- A2106: post original de @martinaquinoa del 18 de octubre de 2026; observación periodística y alegaciones disputadas sobre una protesta.

Cada fila usa `evidence_tier=attributed_reviewed` y `review_status=reviewed_attributed`. El agente solo puede usarla para decir quién reportó, observó, alegó o analizó algo; no para establecer que la proposición subyacente sea verdadera. Los rastros inaccesibles, espejos, extractos y demás candidatos no seleccionados siguen siendo Tier 3 y quedan fuera de respuestas normales.

## Corpus propuesto en orden cronológico

### E1201 · 2020-08-22 · Queja por agua recibida en CEDHJ
- **Prioridad / estado:** alta / primary_source_found.
- **Actores:** Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA), Comisión Estatal de Derechos Humanos Jalisco (CEDHJ).
- **Qué establece la evidencia:** Recomendación 10/2022, antecedentes, p. 6, narra recepción de queja 6072/2020-I.
- **Incertidumbre:** Leer el expediente antes de inferir causa o frecuencia; no atribuir conocimiento a una persona.
- **Relevancia histórica:** Sitúa una queja sobre calidad ante CEDHJ seis años antes de octubre de 2026.
- **Fuentes:**
  - S1101 · primary · CEDHJ · 2022-02-14 · CEDHJ · human_rights_report · acceso read · [Recomendación 10/2022](https://historico.cedhj.org.mx/recomendaciones/emitidas/2022/Reco%2010-2022%20VP.pdf)

### E1202 · 2020-08-25 · SIAPA responde a medidas cautelares de la CEDHJ
- **Prioridad / estado:** alta / primary_source_found.
- **Actores:** Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA), Comisión Estatal de Derechos Humanos Jalisco (CEDHJ).
- **Qué establece la evidencia:** Recomendación 10/2022 p. 7, oficio DAO/219/2020.
- **Incertidumbre:** La recepción por CEDHJ no demuestra cumplimiento ni conocimiento individual del gobernador.
- **Relevancia histórica:** Conecta reportes previos con una respuesta institucional documentada.
- **Fuentes:**
  - S1101 · primary · CEDHJ · 2022-02-14 · CEDHJ · human_rights_report · acceso read · [Recomendación 10/2022](https://historico.cedhj.org.mx/recomendaciones/emitidas/2022/Reco%2010-2022%20VP.pdf)

### E1203 · 2020-10-15 · Advertencia universitaria sobre calidad del agua
- **Prioridad / estado:** alta / needs_additional_source.
- **Actores:** Universidad de Guadalajara (UdeG), Especialistas de la Universidad de Guadalajara.
- **Qué establece la evidencia:** El índice del comunicado universitario muestra fecha, autor y declaraciones.
- **Incertidumbre:** Página original devolvió 502; contrastar el comunicado completo y datos de muestreo.
- **Relevancia histórica:** Muestra preocupación académica anterior a la crisis de 2026.
- **Fuentes:**
  - S1124 · primary · Universidad de Guadalajara · 2020-10-15 · Martha Eva Loera · official_statement · acceso snippet_only · [Agua potable contaminada y de mala calidad en AMG, advierten especialistas](https://ww1.udg.mx/es/noticia/agua-potable-contaminada-y-de-mala-calidad-en-amg-advierten-especialistas)

### E1204 · 2022-02-14 · CEDHJ emite Recomendación 10/2022
- **Prioridad / estado:** alta / primary_source_found.
- **Actores:** Comisión Estatal de Derechos Humanos Jalisco (CEDHJ), Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA), Comisión Estatal del Agua de Jalisco (CEA), Comisión para la Protección contra Riesgos Sanitarios de Jalisco (COPRISJAL), Secretaría de Gestión Integral del Agua de Jalisco (SEGIA).
- **Qué establece la evidencia:** Documento original fechado y cobertura posterior de seguimiento.
- **Incertidumbre:** La nota de 2023 se basa en la misma recomendación; no es una nueva prueba de sus resultados.
- **Relevancia histórica:** Documenta un antecedente institucional sobre calidad y suministro en la administración anterior.
- **Fuentes:**
  - S1101 · primary · CEDHJ · 2022-02-14 · CEDHJ · human_rights_report · acceso read · [Recomendación 10/2022](https://historico.cedhj.org.mx/recomendaciones/emitidas/2022/Reco%2010-2022%20VP.pdf)
  - S1105 · secondary · El Informador · 2023-09-21 · Ilse Martínez · news · acceso read · [¿Qué ha pasado con la recomendación sobre calidad de agua en Guadalajara?](https://www.informador.mx/jalisco/Que-ha-pasado-con-la-recomendacion-sobre-calidad-de-agua-en-Guadalajara-20230921-0069.html)

### E1205 · 2022-06-20 · Vecina presenta queja sobre la presa Las Pintas
- **Prioridad / estado:** alta / primary_source_found.
- **Actores:** Comisión Estatal de Derechos Humanos Jalisco (CEDHJ), Vecinas y vecinos de Las Pintas.
- **Qué establece la evidencia:** Recomendación 10/2026, expediente 3583/2022/IV, p. 6.
- **Incertidumbre:** Es una denuncia, no prueba independiente de todas sus alegaciones ni de la causa del agua suministrada.
- **Relevancia histórica:** Sitúa la preocupación por Las Pintas en un expediente institucional cuatro años antes de octubre de 2026.
- **Fuentes:**
  - S1102 · primary · CEDHJ · 2026-04-30 · CEDHJ · human_rights_report · acceso read · [Recomendación 10/2026](https://cedhj.org.mx/assets_web/doc/recomendaciones/emitidas/2026/20260430150739/recomendacion_1777583259457.pdf)

### E1206 · 2023-08-04 · SIAPA informa sobre limpieza del sistema Chapala-Santiago
- **Prioridad / estado:** alta / primary_source_found.
- **Actores:** Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA), Comisión Estatal de Derechos Humanos Jalisco (CEDHJ), Comisión Estatal del Agua de Jalisco (CEA).
- **Qué establece la evidencia:** Recomendación 10/2026 p. 15 reproduce oficio DJ/0120/2023 y memorándum SA/1446/2023.
- **Incertidumbre:** Es lo informado por SIAPA; no acredita que los trabajos bastaran ni sus resultados.
- **Relevancia histórica:** Muestra cómo el organismo describía su mantenimiento antes de 2026.
- **Fuentes:**
  - S1102 · primary · CEDHJ · 2026-04-30 · CEDHJ · human_rights_report · acceso read · [Recomendación 10/2026](https://cedhj.org.mx/assets_web/doc/recomendaciones/emitidas/2026/20260430150739/recomendacion_1777583259457.pdf)

### E1207 · 2023-08-15 · Colectivos presentan campaña #SiapaCorrupto
- **Prioridad / estado:** media / needs_review.
- **Actores:** Organizaciones de la campaña #SiapaCorrupto, Instituto Mexicano para el Desarrollo Comunitario (IMDEC), Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA).
- **Qué establece la evidencia:** Reportaje con fecha y firma identifica lanzamiento y demandas.
- **Incertidumbre:** Buscar comunicado original; las acusaciones son del colectivo y no resoluciones.
- **Relevancia histórica:** Expone una organización pública de reclamos antes de 2026.
- **Fuentes:**
  - S1104 · secondary · ZonaDocs · 2023-08-15 · Mario Marlo · news · acceso read · [#SiapaCorrupto: colectivos ciudadanos unen fuerzas contra la corrupción en el manejo del agua en Guadalajara](https://www.zonadocs.mx/2023/08/15/siapacorrupto-colectivos-ciudadanos-unen-fuerzas-contra-la-corrupcion-en-el-manejo-del-agua-en-guadalajara/)

### E1208 · 2023-09-21 · Seguimiento reportado de la Recomendación 10/2022
- **Prioridad / estado:** alta / needs_additional_source.
- **Actores:** Comisión Estatal de Derechos Humanos Jalisco (CEDHJ), Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA).
- **Qué establece la evidencia:** La nota de Ilse Martínez atribuye la cifra al director de seguimiento de CEDHJ.
- **Incertidumbre:** La declaración citada ocurrió en agosto sin día exacto; la fecha de evento es la publicación. Buscar informe de seguimiento de CEDHJ.
- **Relevancia histórica:** Distingue emisión de recomendaciones, aceptación y cumplimiento posterior.
- **Fuentes:**
  - S1105 · secondary · El Informador · 2023-09-21 · Ilse Martínez · news · acceso read · [¿Qué ha pasado con la recomendación sobre calidad de agua en Guadalajara?](https://www.informador.mx/jalisco/Que-ha-pasado-con-la-recomendacion-sobre-calidad-de-agua-en-Guadalajara-20230921-0069.html)
  - S1101 · primary · CEDHJ · 2022-02-14 · CEDHJ · human_rights_report · acceso read · [Recomendación 10/2022](https://historico.cedhj.org.mx/recomendaciones/emitidas/2022/Reco%2010-2022%20VP.pdf)

### E1209 · 2024-03-14 · Organizaciones cuestionan políticas hídricas y tandeos
- **Prioridad / estado:** media / needs_review.
- **Actores:** Instituto Mexicano para el Desarrollo Comunitario (IMDEC), Organizaciones de la campaña #SiapaCorrupto.
- **Qué establece la evidencia:** Nota identificada con fecha y autor recoge postura de organizaciones.
- **Incertidumbre:** Localizar comunicado conjunto y distinguir fecha de pronunciamiento de fecha de publicación.
- **Relevancia histórica:** Recoge una perspectiva ciudadana de la administración anterior sin adoptar sus conclusiones.
- **Fuentes:**
  - S1106 · secondary · ZonaDocs · 2024-03-14 · Mario Marlo · news · acceso read · [Organizaciones en Jalisco denuncian la crisis hídrica en el estado y critican las políticas gubernamentales](https://www.zonadocs.mx/2024/03/14/organizaciones-en-jalisco-denuncian-la-crisis-hidrica-en-el-estado-y-critican-las-politicas-gubernamentales/)

### E1210 · 2025-03-25 · Campaña ciudadana expone quejas y fugas
- **Prioridad / estado:** alta / needs_additional_source.
- **Actores:** Instituto Mexicano para el Desarrollo Comunitario (IMDEC), Organizaciones de la campaña #SiapaCorrupto, Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA).
- **Qué establece la evidencia:** Reportaje identifica comunicado y relata denuncias.
- **Incertidumbre:** No se localizó comunicado ni base primaria de conteos; no generalizar cifras.
- **Relevancia histórica:** Sitúa quejas organizadas sobre la calidad antes de las protestas de 2026.
- **Fuentes:**
  - S1107 · secondary · ZonaDocs · 2025-03-25 · Mario Marlo · news · acceso read · [#ElSiapaQueQueremos: exigen colectivos gestión del agua justa y sin corrupción](https://www.zonadocs.mx/2025/03/25/elsiapaquequeremos-exigen-colectivos-gestion-del-agua-justa-y-sin-corrupcion/)

### E1211 · 2025-09-18 · CEDHJ recibe queja sobre Arroyo Seco
- **Prioridad / estado:** alta / primary_source_found.
- **Actores:** Comisión Estatal de Derechos Humanos Jalisco (CEDHJ), Vecinas y vecinos de Arroyo Seco, Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA), Comisión Estatal del Agua de Jalisco (CEA), Ayuntamiento de San Pedro Tlaquepaque.
- **Qué establece la evidencia:** Recomendación 10/2026 p. 57, expediente 2362/2025/IV.
- **Incertidumbre:** Los posibles vertidos son alegatos de quejosos; no se establece contaminación del agua de grifo.
- **Relevancia histórica:** Añade un antecedente de denuncias ambientales cerca del sistema antes de 2026.
- **Fuentes:**
  - S1102 · primary · CEDHJ · 2026-04-30 · CEDHJ · human_rights_report · acceso read · [Recomendación 10/2026](https://cedhj.org.mx/assets_web/doc/recomendaciones/emitidas/2026/20260430150739/recomendacion_1777583259457.pdf)

### E1222 · 2025-09-19 · CONAGUA notifica a SIAPA riesgo en la descarga de Arroyo Seco
- **Prioridad / estado:** alta / primary_source_found.
- **Actores:** Comisión Nacional del Agua (CONAGUA), Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA).
- **Qué establece la evidencia:** La Recomendación 10/2026, p. 63, reproduce que el comunicado CONAGUA **BOO.812.01625**, de 19 de septiembre de 2025, notificó al titular del SIAPA una afectación del temporal en la descarga de Arroyo Seco al Canal Las Pintas y solicitó intervención y remediación urgente. El riesgo descrito era un posible rompimiento de talud, inundaciones y afectaciones en la zona, con riesgo para el sistema de abasto de la ZMG.
- **Incertidumbre:** La recomendación dice que se adjuntó copia; el original autónomo de CONAGUA no apareció en una búsqueda focalizada por su número. Este candidato se apoya en esa copia/reproducción en el expediente CEDHJ. No prueba que CONAGUA hubiera advertido específicamente sobre la contaminación de agua potable de octubre de 2026, ni que la remediación se ejecutara o fuera eficaz.
- **Seguimiento posterior:** El mismo pasaje dice que SIAPA pidió a CEA apoyo para contratar con urgencia una empresa y que CEA programó recursos e inició contratación. No se crea un evento separado: el pasaje no fecha ni la petición de SIAPA, ni el inicio del procedimiento, ni la intervención; el oficio CEA que lo relata fue recibido el 7 de noviembre de 2025.
- **Relevancia histórica:** Registra un aviso formal de riesgo de infraestructura/ambiental en Arroyo Seco–Canal Las Pintas, no una determinación técnica de la causa de una crisis posterior.
- **Fuentes:**
  - S1102 · primary · CEDHJ · 2026-04-30 · CEDHJ · human_rights_report · acceso read · [Recomendación 10/2026](https://cedhj.org.mx/assets_web/doc/recomendaciones/emitidas/2026/20260430150739/recomendacion_1777583259457.pdf)

### E1212 · 2026-01-14 · Queja colectiva por agua e infraestructura en La Duraznera
- **Prioridad / estado:** alta / primary_source_found.
- **Actores:** Comisión Estatal de Derechos Humanos Jalisco (CEDHJ), Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA), Ayuntamiento de San Pedro Tlaquepaque.
- **Qué establece la evidencia:** Recomendación 10/2026 p. 71, expediente 89/2026/IV.
- **Incertidumbre:** La queja no verifica por sí sola los hechos ni su causa; el requerimiento a SIAPA fue posterior.
- **Relevancia histórica:** Registra denuncias en 2026 antes del debate de octubre.
- **Fuentes:**
  - S1102 · primary · CEDHJ · 2026-04-30 · CEDHJ · human_rights_report · acceso read · [Recomendación 10/2026](https://cedhj.org.mx/assets_web/doc/recomendaciones/emitidas/2026/20260430150739/recomendacion_1777583259457.pdf)

### E1213 · 2026-01-28 · Se presenta estudio exploratorio de olores en Las Pintas
- **Prioridad / estado:** media / needs_review.
- **Actores:** Universidad de Guadalajara (UdeG), Vecinas y vecinos de Las Pintas.
- **Qué establece la evidencia:** Gaceta describe la presentación y enlaza al estudio original.
- **Incertidumbre:** PDF enlazado excedió límite de lectura; revisar metodología antes de usar cualquier resultado.
- **Relevancia histórica:** Documenta investigación ambiental previa a octubre, sin confundir aire con agua potable.
- **Fuentes:**
  - S1108 · secondary · Gaceta UDG · 2026-01-28 · Gaceta UDG · news · acceso read · [Olores ofensivos, la realidad cotidiana en El Salto, Juanacatlán y Las Pintas](https://www.gaceta.udg.mx/olores-ofensivos-la-realidad-cotidiana-en-el-salto-juanacatlan-y-las-pintas/)
  - S1126 · primary · Universidad de Guadalajara y colaboradores · fecha de publicación no confirmada · autor no confirmado · academic · acceso link_only · [Olores ofensivos en El Salto, Juanacatlán y Las Pintas, Jalisco](https://www.seguirenlatierra.org/wp-content/uploads/2025/11/Estudio-exploratorio-olores-ofensivos_ISBN.pdf)

### E1219 · 2026-03-05 · CEDHJ abre Acta de Investigación 15/2026/DQOS
- **Prioridad / estado:** alta / primary_source_found.
- **Actores:** Comisión Estatal de Derechos Humanos Jalisco (CEDHJ), Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA).
- **Qué establece la evidencia:** Recomendación 10/2026, p. 74, apartado 1.4, arábigos 1–2. A raíz de una nota de *El Informador* titulada «SIAPA reconoce problemas en calidad del agua», CEDHJ abrió de oficio el Acta de Investigación 15/2026/DQOS. Ese mismo día requirió al titular de SIAPA informar si había obras en tuberías, cuáles eran las causas del problema de calidad, qué protocolo se aplicaba y en qué plazo se estimaba resolverlo.
- **Incertidumbre:** La nota periodística es el antecedente que activó la actuación; esta fuente no verifica por sí misma sus afirmaciones fácticas ni la causa del problema. El candidato registra la apertura de la investigación y el requerimiento de CEDHJ, no la conclusión de que hubiese obras, una causa identificada o un plazo cierto.
- **Relación con E1217:** La respuesta de SIAPA mediante oficio DJ/099/2026, recibida el 15 de abril, sigue siendo un evento posterior y separado (E1217); no se fusiona con la actuación de CEDHJ del 5 de marzo.
- **Relevancia histórica:** Documenta conocimiento y actuación institucional de CEDHJ antes de la respuesta formal de SIAPA.
- **Fuentes:**
  - S1102 · primary · CEDHJ · 2026-04-30 · CEDHJ · human_rights_report · acceso read · [Recomendación 10/2026](https://cedhj.org.mx/assets_web/doc/recomendaciones/emitidas/2026/20260430150739/recomendacion_1777583259457.pdf)

### E1214 · 2026-03-13 · Personal entrevistado denuncia descargas y falta de equipo
- **Prioridad / estado:** alta / needs_additional_source.
- **Actores:** Trabajadoras y trabajadores entrevistados del SIAPA, Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA).
- **Qué establece la evidencia:** Nota identifica al autor y presenta testimonios de trabajadores sin nombrarlos.
- **Incertidumbre:** No se localizaron oficios ni entrevista original específica; los avisos internos y la causalidad requieren corroboración.
- **Relevancia histórica:** Registra advertencias laborales publicadas antes de octubre, sin presumir quién recibió cada aviso.
- **Fuentes:**
  - S1109 · secondary · ZonaDocs · 2026-03-13 · Mario Marlo · interview · acceso read · [Trabajadores del SIAPA denuncian descargas contaminantes, falta de equipo y deterioro del sistema de agua en Guadalajara](https://www.zonadocs.mx/2026/03/13/trabajadores-del-siapa-denuncian-descargas-contaminantes-falta-de-equipo-y-deterioro-del-sistema-de-agua-en-guadalajara/)

### E1215 · 2026-03-18 · Especialistas UdeG piden mesa técnica
- **Prioridad / estado:** media / needs_review.
- **Actores:** Universidad de Guadalajara (UdeG), Especialistas de la Universidad de Guadalajara.
- **Qué establece la evidencia:** Gaceta UDG identifica fecha, especialistas y propuesta.
- **Incertidumbre:** Las explicaciones sobre causas son opiniones de los expertos; revisar estudios específicos.
- **Relevancia histórica:** Hay advertencias académicas públicas meses antes de octubre.
- **Fuentes:**
  - S1110 · secondary · Gaceta UDG · 2026-03-18 · Gaceta UDG · news · acceso read · [Expertos de UdeG proponen mesa técnica sobre calidad del agua](https://www.gaceta.udg.mx/mesa-tecnica-calidad-agua/)

### E1216 · 2026-03-22 · Protesta y anuncio de red vecinal de monitoreo
- **Prioridad / estado:** media / needs_additional_source.
- **Actores:** Instituto Mexicano para el Desarrollo Comunitario (IMDEC), Organizaciones de la campaña #SiapaCorrupto, Personas que protestaron por agua limpia.
- **Qué establece la evidencia:** Extracto de ZonaDocs y nota posterior de abril registran la protesta del 22 de marzo.
- **Incertidumbre:** Primera página devuelve 500; recuperar autor y texto completo. La segunda fuente es retrospectiva y no independiente para cada detalle.
- **Relevancia histórica:** Muestra organización ciudadana y reclamos anteriores a octubre.
- **Fuentes:**
  - S1111 · secondary · ZonaDocs · 2026-03-23 · autor no confirmado · news · acceso snippet_only · [En protesta anuncian Red de Monitores del Agua Vecinales, además de exigir alerta sanitaria y destitución del Director de SIAPA](https://www.zonadocs.mx/2026/03/23/protesta-por-el-agua-en-guadalajara-anuncian-red-de-monitores-del-agua-vecinales-y-exigen-alerta-sanitaria-y-destitucion-del-director-de-siapa/)
  - S1112 · secondary · ZonaDocs · 2026-04-20 · Mario Marlo · news · acceso read · [Mercurio, aluminio y sin cloro: el agua del SIAPA reprueba el primer monitoreo ciudadano en el AMG](https://www.zonadocs.mx/2026/04/20/mercurio-aluminio-y-sin-cloro-el-agua-del-siapa-reprueba-el-primer-monitoreo-ciudadano-en-el-amg/)

### E1217 · 2026-04-15 · SIAPA expone una explicación ante la CEDHJ
- **Prioridad / estado:** alta / primary_source_found.
- **Actores:** Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA), Comisión Estatal de Derechos Humanos Jalisco (CEDHJ), Ayuntamiento de Tlajomulco de Zúñiga.
- **Qué establece la evidencia:** Recomendación 10/2026 p. 74 reproduce oficio DJ/099/2026 recibido el 15 de abril.
- **Incertidumbre:** No establece por sí solo el origen ni la distribución de responsabilidades; ver también la respuesta municipal.
- **Relevancia histórica:** Conserva una explicación institucional previa a octubre y una limitación de tratamiento afirmada por SIAPA.
- **Fuentes:**
  - S1102 · primary · CEDHJ · 2026-04-30 · CEDHJ · human_rights_report · acceso read · [Recomendación 10/2026](https://cedhj.org.mx/assets_web/doc/recomendaciones/emitidas/2026/20260430150739/recomendacion_1777583259457.pdf)

### E1218 · 2026-04-15 · Tlajomulco comunica una versión distinta sobre puntos de descarga
- **Prioridad / estado:** alta / primary_source_found.
- **Actores:** Ayuntamiento de Tlajomulco de Zúñiga, Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA), Comisión Estatal de Derechos Humanos Jalisco (CEDHJ), Ayuntamiento de San Pedro Tlaquepaque.
- **Qué establece la evidencia:** Recomendación 10/2026 pp. 52–53 reproduce oficio municipal DAPIH/0331-01/2026.
- **Incertidumbre:** La versión municipal es una afirmación; cotejar inspecciones, coordenadas y oficios originales.
- **Relevancia histórica:** Conserva otra versión institucional para revisar discrepancias sin resolverlas automáticamente.
- **Fuentes:**
  - S1102 · primary · CEDHJ · 2026-04-30 · CEDHJ · human_rights_report · acceso read · [Recomendación 10/2026](https://cedhj.org.mx/assets_web/doc/recomendaciones/emitidas/2026/20260430150739/recomendacion_1777583259457.pdf)

### E1220 · 2026-04-30 · CEDHJ emite Recomendación 10/2026
- **Prioridad / estado:** alta / primary_source_found.
- **Actores:** Comisión Estatal de Derechos Humanos Jalisco (CEDHJ), Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA), Comisión Estatal del Agua de Jalisco (CEA), Ayuntamiento de Tlajomulco de Zúñiga, Ayuntamiento de San Pedro Tlaquepaque, Comisión para la Protección contra Riesgos Sanitarios de Jalisco (COPRISJAL), Secretaría de Gestión Integral del Agua de Jalisco (SEGIA).
- **Qué establece la evidencia:** Documento original, portada y antecedentes.
- **Incertidumbre:** Revisar cada conclusión y destinatario; no asumir que todo expediente trata el mismo fenómeno.
- **Relevancia histórica:** Reúne antecedentes anteriores a octubre y posiciones de varias instituciones en un documento primario.
- **Fuentes:**
  - S1102 · primary · CEDHJ · 2026-04-30 · CEDHJ · human_rights_report · acceso read · [Recomendación 10/2026](https://cedhj.org.mx/assets_web/doc/recomendaciones/emitidas/2026/20260430150739/recomendacion_1777583259457.pdf)

### E1221 · 2026-06-29 · IMDEC presenta monitoreo ciudadano ampliado
- **Prioridad / estado:** alta / needs_additional_source.
- **Actores:** Instituto Mexicano para el Desarrollo Comunitario (IMDEC), Personas que protestaron por agua limpia.
- **Qué establece la evidencia:** IMDEC identifica fecha de presentación; ZonaDocs describe instrumentos y resultados del mismo corpus.
- **Incertidumbre:** Acceso directo a IMDEC solo por extracto; localizar informe íntegro, protocolo, resultados de laboratorio y evaluar representatividad.
- **Relevancia histórica:** Recoge evidencia ciudadana anterior a octubre sin extrapolar muestras seleccionadas.
- **Fuentes:**
  - S1113 · primary · IMDEC / Agua · fecha de publicación no confirmada · IMDEC · NGO · acceso snippet_only · [Monitoreo ciudadano revela agua contaminada con plomo, fluoruros y sin cloro en 42 puntos de la ZMG](https://www.imdecdhagua.org/monitoreo-ciudadano-revela-agua-contaminada-con-plomo-fluoruros-y-sin-cloro-en-42-puntos-de-la-zmg/)
  - S1114 · secondary · ZonaDocs · 2026-07-02 · Mario Marlo · investigation · acceso read · [El agua limpia que no llega y los metales que sí: 184 muestras ciudadanas desnudan la crisis hídrica de la ZMG](https://www.zonadocs.mx/2026/07/02/el-agua-limpia-que-no-llega-y-los-metales-que-si-184-muestras-ciudadanas-desnudan-la-crisis-hidrica-de-la-zmg/)

### E1223 · 2026-10-07 · Gobernador informa cierre de compuertas de Las Pintas
- **Prioridad / estado:** alta / needs_additional_source.
- **Actores:** Pablo Lemus Navarro, Gobierno de Jalisco, Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA).
- **Qué establece la evidencia:** Entrevista a Lemus del 7 y reseña posterior de El País reportan el cierre del 6 de octubre.
- **Incertidumbre:** Fecha del evento es la declaración del 7; la operación se reporta el día 6. Dos notas usan declaraciones oficiales; no son mediciones independientes de causa o calidad.
- **Relevancia histórica:** Registra una explicación oficial y un cambio operativo reportado a comienzos de octubre.
- **Fuentes:**
  - S1116 · secondary · Quadratín Jalisco · 2026-10-07 · Haremy Reyes · news · acceso read · [Cierran entrada de agua de Las Pintas; líquido deberá mejorar en 3 días](https://jalisco.quadratin.com.mx/principal/cierran-entrada-de-agua-de-las-pintas-liquido-debera-mejorar-en-3-dias/)
  - S1117 · secondary · El País · 2026-10-16 · Erika Rosete y Patricia San Juan Flores · news · acceso read · [Un acueducto sustituto y una inversión de 12.000 millones de pesos: a prueba la solución al problema del agua en Jalisco](https://elpais.com/mexico/2026-10-16/un-acueducto-sustituto-y-una-inversion-de-12000-millones-de-pesos-a-prueba-la-solucion-al-problema-del-agua-en-jalisco.html)

### E1224 · 2026-10-11 · Marcha ciudadana por agua limpia
- **Prioridad / estado:** media / strong_candidate.
- **Actores:** Personas que protestaron por agua limpia, Gobierno de Jalisco.
- **Qué establece la evidencia:** Dos coberturas periodísticas diferentes describen la marcha del 11 de octubre.
- **Incertidumbre:** Las cifras de detenciones no se incorporan como hechos unificados: [ZonaDocs](https://www.zonadocs.mx/2026/10/11/queremos-agua-no-represion-marcha-por-agua-limpia-en-la-zmg-termina-con-51-detenciones-arbitrarias/) atribuye 51 a IMDEC, mientras UnoTV reporta 39 atribuidas al Gobierno. Revisar cortes horarios y fuentes.
- **Relevancia histórica:** La movilización muestra el alcance público del reclamo, con testimonios independientes.
- **Fuentes:**
  - S1118 · secondary · ZonaDocs · 2026-10-11 · Karen Garcia · news · acceso read · [¿Esa agua quieres para nosotros, Lemus?](https://www.zonadocs.mx/2026/10/11/esa-agua-quieres-para-nosotros-lemus/)
  - S1119 · secondary · El País · 2026-10-11 · Pablo Ferri y Patricia San Juan Flores · news · acceso read · [Miles de vecinos se manifiestan contra el agua sucia en Guadalajara](https://elpais.com/mexico/2026-10-11/miles-de-vecinos-se-manifiestan-contra-el-agua-sucia-en-guadalajara.html)
  - S1125 · secondary · UnoTV · 2026-10-11 · F. López · news · acceso read · [Confirman 39 detenidos en marcha por el agua, mientras universidades critican uso de la fuerza](https://www.unotv.com/estados/jalisco/confirman-39-detenidos-en-marcha-por-el-agua-mientras-universidades-critican-uso-de-la-fuerza/)

### E1225 · 2026-10-15 · Inicio reportado del esquema de rotación
- **Prioridad / estado:** media / needs_additional_source.
- **Actores:** Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA), Gobierno de Jalisco.
- **Qué establece la evidencia:** Reportaje del 22 de octubre sitúa el inicio oficial el 15 de octubre y recoge testimonios.
- **Incertidumbre:** Localizar programa original de SIAPA, cobertura y fecha de entrada en vigor por colonia.
- **Relevancia histórica:** Vincula una medida de emergencia con cambios en el acceso al servicio.
- **Fuentes:**
  - S1120 · secondary · El País · 2026-10-22 · Erika Rosete · news · acceso read · [El racionamiento de agua en Guadalajara deja sin servicio a miles de hogares](https://elpais.com/mexico/2026-10-22/el-racionamiento-de-agua-en-guadalajara-deja-sin-servicio-a-miles-de-hogares.html)

### E1226 · 2026-10-27 · CEA reconoce en prensa problemas en colectores
- **Prioridad / estado:** alta / needs_additional_source.
- **Actores:** Comisión Estatal del Agua de Jalisco (CEA).
- **Qué establece la evidencia:** Nota atribuye la declaración al director de CEA.
- **Incertidumbre:** Fecha es la publicación; verificar cuándo se hizo la declaración, grabación y diagnóstico original. Evitar inferir culpabilidad.
- **Relevancia histórica:** Añade una explicación oficial sobre infraestructura pública al debate sobre descargas.
- **Fuentes:**
  - S1121 · secondary · Semanario Conciencia Pública · 2026-10-27 · Redacción Conciencia Pública · news · acceso read · [CEA admite responsabilidad en contaminación de Las Pintas; detectan 150 descargas irregulares](https://concienciapublica.com.mx/2026/10/27/cea-admite-responsabilidad-en-contaminacion-de-las-pintas-detectan-150-descargas-irregulares/)

### E1227 · 2026-10-28 · Federación y Jalisco presentan plan de acueductos
- **Prioridad / estado:** alta / needs_additional_source.
- **Actores:** Gobierno de Jalisco, Pablo Lemus Navarro, Comisión Nacional del Agua (CONAGUA), Gobierno federal de México, Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA).
- **Qué establece la evidencia:** Cobertura identifica fecha, actores, montos anunciados y calendario previsto.
- **Incertidumbre:** Obtener conferencia y proyecto oficial; montos y cronograma pueden cambiar y no prueban cumplimiento.
- **Relevancia histórica:** Registra compromisos anunciados en la fase de respuesta, sin asumir ejecución.
- **Fuentes:**
  - S1122 · secondary · El País · 2026-10-28 · Erika Rosete · news · acceso read · [Dos nuevos acueductos y una inversión conjunta de 25.000 millones de pesos: Jalisco y la Federación presentan su plan para Guadalajara](https://elpais.com/mexico/2026-10-28/dos-nuevos-acueductos-y-una-inversion-conjunta-de-25000-millones-de-pesos-jalisco-y-la-federacion-presentan-su-plan-para-guadalajara.html)

## Qué significa la corroboración

- E1224: ZonaDocs y El País tienen coberturas periodísticas distintas de la marcha; corroboran el hecho general, no cada cifra o acusación.
- E1223: Quadratín y El País reportan el cierre, pero se apoyan en versiones oficiales; son dos coberturas, no dos mediciones independientes de calidad o causalidad.
- E1204: CEDHJ y El Informador documentan la recomendación y su seguimiento; el segundo se refiere al mismo documento original.
- E1221: IMDEC y ZonaDocs se refieren al mismo monitoreo y no constituyen muestras independientes. El enlace de IMDEC fue consultable solo en resultados de búsqueda.
- E1216: la nota de marzo devolvió error 500; la nota de abril la menciona retrospectivamente. No tratar la repetición como corroboración independiente.

## Candidatos que necesitan evidencia adicional

- **E1203:** comunicado de UdeG de 2020 devolvió 502; verificar comunicado, muestras y contexto en copia institucional.
- **E1208 / E1210:** localizar seguimiento oficial de CEDHJ y comunicado/datos de la campaña. Aceptación de puntos no equivale a cumplimiento.
- **E1213 / E1214 / E1221:** revisar estudio de olores, identificar entrevista original y registros de avisos a SIAPA, y obtener protocolos y resultados originales de monitoreo; no confundir olores ambientales con composición del agua potable.
- **E1217 / E1218:** contrastar los oficios, inspecciones y coordenadas de ambas versiones; no inferir que una sea verdadera solo por tratarse de una autoridad.
- **E1219:** obtener la nota original que motivó el acta, pero mantenerla separada de la apertura de oficio y del oficio SIAPA DJ/099/2026.
- **E1222:** solicitar o localizar el original de CONAGUA BOO.812.01625 y los documentos fechados de la solicitud SIAPA–CEA, contratación, intervención y recepción; el pasaje retrospectivo no permite fechar esas acciones de seguimiento.
- **E1223 / E1225 / E1226 / E1227:** obtener texto oficial del decreto, órdenes y anuncios, calendario de rotación, inventario de colectores y proyecto de inversión.

## Pistas interesantes aún no listas

- ZonaDocs, [El agua sucia no empezó ayer. La irresponsabilidad tampoco](https://www.zonadocs.mx/2026/10/13/el-agua-sucia-no-empezo-ayer-la-irresponsabilidad-tampoco/) es opinión; orienta hacia documentos anteriores pero sus juicios no se incorporaron como hechos.
- El estudio original de olores [S1126](https://www.seguirenlatierra.org/wp-content/uploads/2025/11/Estudio-exploratorio-olores-ofensivos_ISBN.pdf) se enlazó desde Gaceta UDG, pero el archivo excedió el límite de la herramienta.
- Informes y datos brutos de SIAPA/COPRISJAL, registros originales de desazolve, laboratorios acreditados, reportes históricos de trabajadores, expedientes de CEDHJ y convenios municipales requieren investigación adicional.
- Buscar una copia completa del [comunicado universitario de 2020](https://ww1.udg.mx/es/noticia/agua-potable-contaminada-y-de-mala-calidad-en-amg-advierten-especialistas), que devolvió 502.

## Fuentes, límites y controles

En los metadatos de cada fuente `primary` describe proximidad a la comunicación o documento; el propio comunicado de IMDEC es fuente primaria de lo que la organización informó, no equivale automáticamente a datos de laboratorio certificados. `secondary` identifica cobertura o reconstrucción. `read` significa que se examinó el texto disponible, no que se haya comprobado el documento subyacente.

La investigación utilizó búsqueda web y páginas originales. El PDF del estudio de olores excedió el límite de tamaño; IMDEC agotó el tiempo de acceso; un artículo de ZonaDocs devolvió 500, el comunicado UdeG 502 y SIAPA devolvió 403 para páginas concretas. Los extractos de búsqueda se marcan como tales. La versión de ley SIAPA consultada requiere comprobar reformas y convenios; la función federal propuesta requiere base normativa vigente y titularidad de los cuerpos receptores.

No hay cobertura suficiente aquí para establecer por primera vez cuándo empezó el problema, precisar una cadena causal, evaluar científicamente toda la red ni resolver el cumplimiento de compromisos. Los años 2021 y gran parte de 2024–2025 necesitan más fuentes; en 2026 hacen falta datos crudos, cronologías de notificación y expedientes de seguimiento.

Para repetir los controles estructurales sin modificar SQLite, ejecute `python data/validate_candidates.py`. Estos controles no verifican el contenido real de las fuentes ni sustituyen la revisión humana.

## Primary-source deepening findings

**Investigación adicional, corte 28 de octubre de 2026.** Estos hallazgos son pistas para revisión, no nuevas filas aprobadas ni conclusiones verificadas. En la primera pasada las páginas de X devolvieron 403; en una segunda pasada directa, con sesión iniciada, se leyeron los seis posts/hilos concretos listados abajo y se anotaron la URL, fecha y hora que muestra X. La interfaz no mostró zona horaria: la fecha/hora es la que presentó X y no debe reconciliarse automáticamente con la fecha editorial de una nota. La relación entre un informe retrospectivo y el año que analiza no demuestra cuándo una persona específica recibió los resultados.

### P01 · Toluquilla: antecedentes más antiguos que la nota de 2024

- **Rastro:** Sonia Serrano Íñiguez, [reproducción de su nota de NTR del 31 de enero de 2024](https://labcsa.org/2024/01/31/sin-actualizar-datos-de-calidad-del-agua/) → [documento original de CONAGUA sobre Toluquilla](https://sigagis.conagua.gob.mx/gas1/Edos_Acuiferos_18/jalisco/DR_1402.pdf), pp. 8–9 del PDF (numeración impresa 7–8).
- **Documento obtenido:** sí, resumen institucional. Refiere un estudio IMTA de 1992–1993 y un estudio del SIAPA de 1995 sobre ciertos pozos del sistema Toluquilla; resume resultados fisicoquímicos fuera de límites aplicables en esos estudios. La versión consultada refiere un corte de registro de 2022; **no se estableció la fecha exacta de publicación**. La nota de 2024 es evidencia independiente de que la información se discutía entonces.
- **Límites:** CONAGUA resume estudios anteriores; no se recuperaron los informes originales de 1992–1995 ni los datos por pozo. No demuestra calidad actual ni resultado del agua tratada en todas las casas. No extrapolar a Las Pintas, que es otro sistema.
- **Para revisión:** buscar los informes IMTA y SIAPA originales, identificar puntos, fechas, unidades, norma aplicable y tratamientos; proponer un registro de la publicación de la nota en 2024 y, solo con precisión temporal adecuada, uno separado para los estudios históricos.

### P02 · Auditoría ASEJ sobre datos e indicadores 2021–2023

- **Rastro:** la búsqueda de auditorías asociadas al SIAPA identificó [análisis secundario](https://mayacomunicacion.com.mx/agua-siapa-guadalajara-auditorias-cedhj-preguntas-pendientes/) → [informe individual ASEJ, cuenta pública 2023](https://www.asej.gob.mx/transparencia_asej/sites/default/files/informes_finales/Sistema%20Intermunicipal%20de%20los%20Servicios%20de%20Agua%20Potable%20y%20Alcantarillado%202023.pdf), pp. 91–94 de 110, y [apartado de desempeño](https://www.asej.gob.mx/transparencia_asej/sites/default/files/informes_finales/Sistema%20Intermunicipal%20de%20los%20Servicios%20de%20Agua%20Potable%20y%20Alcantarillado%202023%20Apartado%20Desempe%C3%B1o.pdf).
- **Documento obtenido:** informe individual leído; apartado de desempeño identificado mediante extracto, pero la descarga completa agotó el tiempo. ASEJ expone observaciones sobre indicadores, desinfección y monitoreo y reproduce una respuesta del SIAPA con una medida prevista para marzo–diciembre de 2025. La [ficha ASEJ del 8 de julio de 2025](https://www.asej.gob.mx/noticias/es/node/535) confirma la auditoría de la cuenta pública 2023, no la fecha exacta en que se notificó cada hallazgo.
- **Límites:** la cuenta auditada es 2023 y la revisión se realizó después; no describir la fecha de la auditoría como fecha de cada muestra. El informe usa métricas por parámetro; no convertir porcentajes de parámetros en proporciones de viviendas o de población. Verificar datos, denominadores, norma, puntos de muestreo y respuesta completa del organismo. Una respuesta o plan no demuestra ejecución ni que una persona conociera una advertencia.
- **Para revisión:** cotejar pp. 91–94 y anexo completo; solicitar datos base y acuses de notificación. Proponer una nueva entrada por la auditoría con la fecha de publicación/notificación acreditada, no el 1 de enero de 2023.

### P03 · Muestreos domiciliarios 2025 identificados por Violeta Meléndez

- **Rastro:** [UDG Noticias, Violeta Meléndez, 13 de marzo de 2026](https://udgtv.com/noticias/siapa-detecta-bacterias-fecales-en-agua-domiciliaria/308835) → [PDF de SIAPA sobre muestreos domiciliarios enero–diciembre 2025](https://www.siapa.gob.mx/sites/default/files/muestreos_domiciliarios_ene-dic_2025.pdf).
- **Documento obtenido:** no. El enlace del artículo al PDF oficial devolvió 502. La periodista reportó resultados de algunas muestras; su interpretación y las cifras se conservan como periodismo atribuido hasta cotejar la tabla original, puntos, unidades y parámetros.
- **Para revisión:** recuperar el PDF o pedirlo por transparencia; verificar fecha de publicación, fechas y ubicaciones de toma, resultados completos, método, condiciones de conservación y respuestas oficiales. No usar la apariencia del agua como sustituto de análisis. No inferir la fecha en que una autoridad determinada fue informada.

### P04 · Auditoría interna y plan maestro de Miravalle, 2025–2026

- **Rastro 1:** [NTR, Sonia Serrano, 3 de agosto de 2026](https://www.ntrguadalajara.com/post.php?id_nota=248040) → auditoría de calidad del Órgano Interno de Control que NTR dice haber obtenido por transparencia y cuya orden fecha el 12 de marzo de 2025. El documento no se localizó; la fecha de orden **no es** por sí sola la fecha de resultados ni de comunicación a directivos.
- **Rastro 2:** [NTR, Sonia Serrano, 17 de julio de 2026](https://www.ntrguadalajara.com/post.php?id_nota=247388) → Plan Maestro de Modernización de la PP1 Miravalle, que la nota dice asignado en abril de 2025 y entregado al Congreso en julio de 2026. No se recuperó ese plan maestro íntegro. La [Recomendación CEDHJ 10/2026](https://cedhj.org.mx/assets_web/doc/recomendaciones/emitidas/2026/20260430150739/recomendacion_1777583259457.pdf) solicita publicar resultados del plan; por sí misma no confirma cada detalle de la noticia.
- **Para revisión:** solicitar expediente completo de transparencia, órdenes, metodología, oficio de entrega y fecha de recepción de resultados; obtener el plan maestro de ingeniería y sus versiones. Evitar concluir que las fallas descritas causaron cada incidencia doméstica.

### P05 · La Calera y el sistema antiguo: obras y capacidad

- **Rastro:** [republicación indexada de @JPMS79 del 25 de octubre](https://teapawt.org/clauscm) expresa dudas sobre interconexión y capacidad; la publicación original y hora no se pudieron abrir. [NTR, Lauro Rodríguez, 10 de octubre de 2026](https://mail.ntrguadalajara.com/post.php?id_nota=250996) atribuye dudas a Josué Sánchez Tapetillo y Juan Pablo Macías Salazar y menciona una iniciativa y documentos entregados al Congreso → [ficha oficial Sistema La Calera, anexo 3](https://planintegraldelagua.jalisco.gob.mx/pdf/an-0014.pdf), pp. 1–5, y [índice oficial del plan](https://planintegraldelagua.jalisco.gob.mx/).
- **Documento obtenido:** sí, ficha oficial. Describe una interconexión proyectada con el tanque de cambio de régimen y reporta inversiones y trabajos de La Calera en 2024–2025; presenta una capacidad de diseño propuesta. El índice enlaza también la etapa 2; ambos enlaces consultados conducen a fichas de contenido equivalente, **no son evidencia independiente**.
- **Límites:** la ficha consultada no demuestra automáticamente el estado operativo, el caudal real ni la viabilidad hidráulica; no se confirmó su fecha original ni si corresponde exactamente a la versión citada en octubre. Las cifras y reservas de los especialistas son análisis atribuido; no se recalcularon. La obra 2024 de desvío de aguas residuales debe cotejarse con contratos, actas y planos antes de describirla como finalizada o eficaz.
- **Para revisión:** buscar expediente legislativo, iniciativa, memorias hidráulicas, mediciones de caudal y presión, recepción y pruebas. Separar lo realizado en 2024/2025 de obras propuestas en 2026.

### P06 · Atención previa a equipos de bombeo, 2024

- **Rastro:** [NTR, Lauro Rodríguez, 11 de junio de 2024](https://www.ntrguadalajara.com/post.php?id_nota=215117) informa que Juan Pablo Macías Salazar solicitó bitácoras 2019–2024 y resume la respuesta del SIAPA sobre las subestaciones de Chapala y Ocotlán.
- **Documento obtenido:** no se recuperaron la solicitud de transparencia ni la respuesta original. La ausencia de registros descrita en la nota no prueba por sí misma ausencia de toda actividad de mantenimiento. Buscar folio, respuesta íntegra y bitácoras de CFE antes de formular un candidato sobre conocimiento o causa de fallas.

### P07 · Información de operación de SIAPA, 2024–2025

- **Rastro 2024:** [Mural / Violeta Meléndez, reproducida por LABCSA el 15 de julio de 2024](https://labcsa.org/2024/07/15/oculta-siapa-informes-sobre-abasto-de-agua/), identifica como documentos subyacentes informes trimestrales SIAPA. La nota evalúa como incompleto un informe del segundo trimestre y comenta volúmenes; no se obtuvo la versión original ni capturas archivadas y no se infiere una intención de ocultar.
- **Rastro 2025:** [NTR / Sonia Serrano, reproducida por LABCSA el 14 de julio de 2025](https://labcsa.org/2025/07/14/alfaro-inflo-cifras-de-abasto-de-agua/) recoge la comparación de Juan Pablo Macías Salazar de un informe gubernamental con informes anuales SIAPA. El titular contiene un juicio; la posible discrepancia de extracción y suministro es una interpretación atribuida, no un hallazgo calculado aquí.
- **Para revisión:** recuperar informes originales por periodo, hojas de cálculo, definiciones de extracción/suministro, unidades y versiones; reproducir la operación y comparar series equivalentes.

### P08 · Testimonio de personal y mediciones del sistema antiguo

- **Rastro:** la [entrevista de ZonaDocs a personal del SIAPA, 13 de marzo de 2026](https://www.zonadocs.mx/2026/03/13/trabajadores-del-siapa-denuncian-descargas-contaminantes-falta-de-equipo-y-deterioro-del-sistema-de-agua-en-guadalajara/) corresponde a E1214; [Mural / Paulina Fonseca, reproducido por LABCSA el 10 de septiembre de 2026](https://labcsa.org/2026/09/10/se-elevan-contaminantes-en-agua-en-8-anos/) relata un análisis de Juan Pablo Macías Salazar basado en mediciones SIAPA de 2018–2024.
- **Límites:** no se localizaron las bitácoras de avisos laborales, el informe íntegro de Macías ni las series de laboratorio originales. La noticia identifica agua **cruda** y cita una comparación con normas de agua para consumo; no trasladar automáticamente esos valores al agua tratada ni afirmar causalidad. Comparar normas, unidades, puntos, valores máximos y métodos por año.

### P09 · Explicaciones oficiales, antes de octubre

- [Agustín del Castillo, UDG TV, 9 de agosto de 2023](https://udgtv.com/noticias/siapa-hay-corresponsables-de-la-mala-calidad-del-agua/194211) reproduce una explicación del SIAPA y recomienda medidas dentro de domicilios, además de recoger quejas vecinales. Buscar el comunicado y análisis originales del 22 de junio de 2023; atribuir la explicación al organismo y las quejas a sus autores.
- [Violeta Meléndez, UDG TV, 11 de marzo de 2026](https://udgtv.com/noticias/siapa-planta-miravalle-entrega-agua-turbia-en-guadalajara/308378) refiere el informe anual SIAPA 2025 y un anteproyecto presentado a la Junta de Gobierno en noviembre de 2025. Ninguno de esos dos documentos subyacentes se recuperó en esta investigación. El presupuesto propuesto y la mejora esperada no son prueba de ejecución.
- [Sonia Serrano, NTR, 10 de diciembre de 2025](https://www.ntrguadalajara.com/post.php?id_nota=238104) reporta una revisión de expedientes de incorporación municipal decidida por la Junta de Gobierno. Solicitar acta y convenios; no confundir cobertura de municipios con calidad de cada fuente.

### Registro de publicaciones y rastros sociales

Los siguientes originales fueron leídos en X. Ver un post acredita su texto, autor visible y fecha de publicación; **no** acredita por sí solo los hechos que afirma. Las categorías de cada entrada separan evidencia de primera mano, opinión o alegación, y corroboración externa.

1. **@JPMS79 · «J P» · [post original](https://x.com/JPMS79/status/2106538977687658619) · 3 de octubre de 2026, 18:16 (hora/zona no indicada por X).** Dice que durante los dos días anteriores los reportes de agua contaminada del SIAPA «han desbordado» redes y que, *según su percepción*, superaron meses previos. No adjunta enlace, documento ni base de datos. **Clasificación:** opinión/observación agregada del autor, no testimonio de un domicilio ni conteo verificable. **Corroborado de forma limitada:** [UDG Noticias, 4 de octubre](https://udgtv.com/noticias/arrecian-reportes-por-agua-turbia-y-maloliente-en-la-zmg/333482) documentó publicaciones, imágenes y videos de quejas en varias colonias y citó 145 inconformidades recibidas por CEDHJ en septiembre; no verifica el periodo de dos días ni la comparación con meses anteriores. La discrepancia entre la fecha que muestra X (3 de octubre) y el rótulo «October 4» usado por UDG debe conservarse, no resolverse por inferencia.
2. **@JSTapetillo · «Josué Sánchez» · [post original](https://x.com/JSTapetillo/status/2106757575630872957) · 4 de octubre de 2026, 08:45 (hora/zona no indicada por X).** Afirma que hay un «nuevo pico» de mala calidad y cuestiona a la alcaldesa. Cita el [post de Ofelia Márquez](https://x.com/OfeliaMarquezS/status/2106747733675561275), que reporta agua negra en Álamo Industrial y olor a herrumbre en Jardines de San José; incluye imagen, no análisis de laboratorio ni documento. **Clasificación:** la conclusión de «pico» es opinión/análisis; el post citado es una queja de primera mano alegada, no una prueba técnica. **Corroborado de forma limitada:** la nota UDG anterior recoge quejas visuales/olfativas y datos de quejas CEDHJ, pero advierte que las quejas no constituyen todavía una determinación oficial de contaminación. Sigue sin recuperarse una muestra, cadena de custodia o resultado por esas dos colonias.
3. **@JSTapetillo · «Josué Sánchez» · hilo [1/3](https://x.com/JSTapetillo/status/1968267797819265026), [2/3](https://x.com/JSTapetillo/status/1968267800105074702), [3/3](https://x.com/JSTapetillo/status/1968267803489951848) · 17 de septiembre de 2025, inicio 04:56 (hora/zona no indicada por X).** No es el hilo histórico de Las Pintas que describía el índice: trata de riesgo de inundación/urbanización en Arroyo Seco, Parques del Bosque, Parques de Santa María y Real del Valle. Atribuye el problema a urbanización, una inmobiliaria, permisos municipales, fincas en zona federal y abandono institucional; enlaza un [post de @kikanaj](https://x.com/kikanaj/status/1968196766509244775) que ahora no está disponible. **Clasificación:** diagnóstico y alegaciones de responsabilidad; no presenta expediente, mapas oficiales ni peritaje. **No verificado:** las causalidades, permisos concretos y la calificación de negligencia. La Recomendación CEDHJ 10/2026 contiene antecedentes de Arroyo Seco (E1211), pero no valida este diagnóstico ni lo conecta con calidad de agua doméstica o Las Pintas.
4. **@JSTapetillo · «Josué Sánchez» · hilo [1/6](https://x.com/JSTapetillo/status/1854533784227484027), [2/6](https://x.com/JSTapetillo/status/1854533786655936868), [3/6](https://x.com/JSTapetillo/status/1854533789097034101), [4/6](https://x.com/JSTapetillo/status/1854533791122878796), [5/6](https://x.com/JSTapetillo/status/1854533793245179999), [6/6](https://x.com/JSTapetillo/status/1854533794977501301) · 7 de noviembre de 2024, inicio 08:38 (hora/zona no indicada por X).** El hilo refiere como versión de SIAPA/Gobierno estatal que el colapso del acueducto Gabriel Castaños obedeció a vandalismo y enlaza una [nota oficial de Jalisco](https://www.jalisco.gob.mx/prensa/noticias/siapa-atiende-fuga-de-agua-potable). La página oficial fue recuperada directamente: está fechada el 6 de noviembre de 2024 y dice que SIAPA atribuyó a actos de vandalismo daños en la Galería de avenida Montevideo, entre Bombeo Colomos y Tanque Diana, que produjeron una fuga; también informa reparaciones y colonias con afectación. Esto **verifica que esa fue la declaración institucional**, no que el vandalismo fuera la causa técnica probada. La página no usa «Gabriel Castaños»; no equiparar ambos nombres/instalaciones sin plano o parte técnico. El hilo cuestiona la explicación: alega una fuga reportada por al menos tres días y originada semanas antes, daños en varios puntos y plantea como posibilidad la sobrepresión. También cita un [post restringido de 2021](https://x.com/MiguelALeyvaS/status/1387208921811759108), que no se pudo leer. **Clasificación:** el comunicado es fuente primaria de la postura oficial; las fechas de reporte, extensión de daños, atribución de falta de atención y la hipótesis de sobrepresión son alegaciones/análisis del autor. **Aún no resuelto:** no decidir la causa de la rotura sin parte técnico, reportes, bitácoras, fotografías con metadatos y peritaje independiente.
5. **@jcrtoral · «Pepe Toral» · [post original](https://x.com/jcrtoral/status/2043742831412416622) · 13 de abril de 2026, 11:27 (hora/zona no indicada por X).** El periodista dice haber acudido al Bosque El Nixticuil y constatado aguas negras corriendo a un arroyo del ANP; atribuye a vecinos la denuncia de que Zapopan, SIAPA y Hito Urbano no asumían responsabilidad. Cita el [aviso previo del Comité en Defensa del Bosque El Nixticuil](https://x.com/bosquenixticuil/status/2043110791969128604), del 11 de abril, que afirma que una fuga *al parecer* provenía del cárcamo Altavista y enlaza ubicación; el post principal contiene video. **Clasificación:** el recorrido/video y la observación del periodista son evidencia visual de primera mano limitada; origen de la descarga, responsabilidades y composición del agua siguen siendo alegaciones. **Corroborado como reportaje, no como peritaje independiente:** su [nota UDG](https://udgtv.com/noticias/contaminan-con-aguas-negras-el-bosque-el-nixticuil/312137) informa que el medio observó un colector descargando a un paso pluvial y que residentes dijeron haber reportado el caso a Zapopan y SIAPA. No hay expediente de inspección, respuesta de autoridad ni análisis de laboratorio recuperado. Es otra cuenca: no inferir ingreso a Las Pintas ni contaminación de agua de grifo.
6. **@martinaquinoa · «Martín Aquino» · [post original](https://x.com/martinaquinoa/status/2111989475534684381) · 18 de octubre de 2026, 19:15 (hora/zona no indicada por X).** Con video de 2:40, afirma que, después de la represión de la marcha del 11 de octubre, policías estatales se mantuvieron al margen de la protesta del 18; alega que hubo infiltrados que hicieron detonaciones y dañaron inmuebles. **Clasificación:** descripción periodística y alegaciones de atribución; el video es material audiovisual de primera mano, pero no se evaluó forensemente y no identifica por sí mismo a infiltrados ni prueba una orden o inacción policial. **Corroborado parcialmente / disputado en la atribución:** [El País](https://elpais.com/mexico/2026-10-19/un-grupo-de-personas-encapuchadas-causan-destrozos-en-el-congreso-y-el-palacio-de-justicia-en-jalisco.html) confirmó daños, presencia de personas encapuchadas con bates y petardos y la suspensión de la movilización; recogió versiones de organizadores y del gobernador. No corroboró que fueran infiltrados ni la afirmación de que la policía los dejó actuar, y la responsabilidad individual seguía siendo una versión en disputa.

### Cuentas de seguimiento y verificación de identidad

| Cuenta | Clasificación para investigación | Identidad y evidencia pública; límite |
|---|---|---|
| [@JPMS79](https://x.com/JPMS79) | `unknown` provisional | La consulta directa del post lo muestra como «J P» y con insignia de cuenta verificada, pero no muestra su nombre civil. Una [republicación secundaria](https://www.sotwe.com/urbanredale) vincula el alias con una nota de Mural atribuida a Juan Pablo Macías Salazar; [NTR](https://www.ntrguadalajara.com/post.php?id_nota=251635) describe a Macías como investigador y especialista hídrico. La unión inequívoca de cuenta y persona sigue pendiente; no asignar periodista ni credenciales de ingeniería. |
| [@JSTapetillo](https://x.com/JSTapetillo) | `technical specialist` | En los originales consultados, X rotula la cuenta «Josué Sánchez - @jstapetillo.bsky.social». [Columna de Jonathan Lomelí](https://www.informador.mx/ideas/Esperando-a-Godoty-al-SIAPA-20240512-0115.html) vincula el usuario con Sánchez Tapetillo como especialista hídrico; [NTR](https://mail.ntrguadalajara.com/post.php?id_nota=250996) identifica a Josué Daniel Sánchez Tapetillo. Esto robustece la correspondencia handle/persona, no prueba afiliaciones actuales ni convierte sus diagnósticos en peritajes. |
| [@viogu](https://x.com/viogu) | `journalist` | Violeta Meléndez firma [notas de UDG TV](https://udgtv.com/noticias/siapa-detecta-bacterias-fecales-en-agua-domiciliaria/308835); el identificador fue dado en la solicitud y está pendiente de cotejar en el perfil original. Su nota de muestreos es reportaje, no fuente primaria del laboratorio. |
| [@agdelcastillo](https://x.com/agdelcastillo) | `environmental journalist` | [Página de autor de UDG TV](https://udgtv.com/autor/agustin-del-castillo/98753) y [entrevista sobre su especialidad ambiental](https://concienciapublica.com.mx/2025/04/06/la-vision-de-agustin-del-castillo-el-populismo-del-gobierno-de-alfaro-llevo-a-la-crisis-al-siapa/). El handle fue proporcionado por el usuario; falta cotejo directo. Sus hipótesis de causalidad son análisis. |
| [@sonia_ssi](https://x.com/sonia_ssi) | `journalist` | Sonia Serrano Íñiguez firma [reportaje de NTR sobre auditoría interna](https://www.ntrguadalajara.com/post.php?id_nota=248040) y también publica [columnas de opinión](https://mail.ntrguadalajara.com/post.php?id_nota=246916); diferenciarlas. El handle fue proporcionado por el usuario; falta cotejo directo. |
| [@martinaquinoa](https://x.com/martinaquinoa) | `journalist` | El original consultado muestra «Martín Aquino» y cuenta verificada. [El Occidental](https://oem.com.mx/eloccidental/local/periodistas-se-reunen-en-la-fil-para-hablar-sobre-los-retos-de-ejercer-en-tiempos-de-corrupcion-27032453) lo identificó como periodista de Mural en 2025. La correspondencia del handle queda corroborada públicamente; su post sigue siendo una fuente de afirmaciones atribuidas, no prueba autónoma de responsabilidad. |
| [@jcrtoral](https://x.com/jcrtoral) | `environmental journalist` | El original consultado muestra «Pepe Toral»; [UDG TV](https://udgtv.com/noticias/contaminan-con-aguas-negras-el-bosque-el-nixticuil/312137) vincula su nota firmada por José Toral con el post y proporciona una biografía profesional ambiental. La identidad/autoría queda corroborada; el contenido técnico continúa sin peritaje independiente. |
| [@Jnlomeli](https://x.com/Jnlomeli) | `journalist` | Jonathan Lomelí firma una [columna de El Informador de 2024](https://www.informador.mx/ideas/Esperando-a-Godoty-al-SIAPA-20240512-0115.html) que identifica a @JSTapetillo. La columna es opinión con observaciones atribuidas; no se confirmó el handle directamente. |
| [@imdecac](https://x.com/imdecac) | `civil_society` | [Red TDT](https://redtdt.org.mx/nuestra-red/region-occidente) identifica al IMDEC y su cuenta. Ver P03/P08 y E1221: no tratar análisis ciudadanos como muestreos independientes cuando se repite el mismo informe. |
| [@CEPAD_AC](https://x.com/CEPAD_AC) | `civil_society` | [Documento de CEPAD alojado por el Congreso](https://infolej.congresojal.gob.mx/documentos/estados/R_155113.pdf) identifica a la organización, su función y su cuenta; útil para rastrear declaraciones y acompañamiento sobre protestas, no para atribuir por sí solo responsabilidades penales. |

**Acciones pendientes:** recuperar los informes anuales SIAPA de 2023–2025 y datos de laboratorios; solicitudes de transparencia de Macías y Serrano; el plan maestro de PP1, actas de Junta, informe OIC, expediente del Congreso sobre el acueducto y respaldos de las publicaciones originales. Priorizar versiones archivadas y respuestas oficiales con fecha verificable. Los hallazgos P01–P09 no se añadieron a `candidate_records.json`; cada propuesta necesita revisión y modelado con precisión temporal antes de incorporarse al corpus candidato.
