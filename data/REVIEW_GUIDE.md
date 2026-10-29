# Guía de revisión · Memoria Hídrica GDL

**Corte de investigación: 28 de octubre de 2026.** Todos los registros son candidatos `verified=0`; ninguna evidencia se ha importado ni aprobado. La fecha de una recomendación posterior no es la fecha de los expedientes anteriores que reproduce.

## Cómo revisar y aprobar

1. Abra las fuentes originales y compruebe en la ubicación indicada la fecha, alcance, actor y atribución. Los enlaces con acceso `snippet_only` o `link_only` requieren abrir el texto completo.
2. Distinga el documento que recoge una denuncia, la denuncia misma, el conocimiento institucional y el conocimiento personal. Corrobore afirmaciones técnicas y políticas con documentación independiente.
3. Revise cada declaración, relación, responsabilidad y compromiso en el JSON. `unknown` significa que no se comprobó el estado; no supone incumplimiento.
4. La aprobación debe ser expresa y por registro. Este JSON incorpora metadatos de investigación que el importador actual no acepta; antes de una futura importación habrá que revisar IDs, eliminar metadatos, establecer campos compatibles y promover únicamente registros y fuentes aprobados. No usar `seed_db.py --file` directamente con este archivo.
5. Las fuentes cuya publicación sea posterior al hecho (especialmente recomendaciones de 2022 y 2026) son fuentes retrospectivas, no evidencia de publicidad de sus detalles en la fecha del hecho.

## Prioridad alta: revisar primero

Los candidatos 1201, 1202, 1204, 1205, 1211, 1212, 1217, 1218 y 1220 tienen respaldo de las recomendaciones primarias de CEDHJ. Revisar después 1214 (advertencias atribuidas al personal), 1221 (muestras ciudadanas), 1223 (cierre y explicación oficial) y 1227 (plan). Ninguno está aprobado.

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
