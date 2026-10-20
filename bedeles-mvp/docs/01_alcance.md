# Definición de alcance del MVP

## Objetivo del MVP

Demostrar, con un prototipo funcional y medible, que un asistente digital puede resolver una parte de las consultas rutinarias de servicios universitarios (orientación, aulas, horarios, trámites, avisos) y canalizar las incidencias del campus con trazabilidad, reduciendo la dependencia de la atención presencial para los casos más simples.

## Dentro del alcance del MVP

1. **Asistente de consultas (chat web):** responde preguntas frecuentes por recuperación de un catálogo de 25 FAQs (aulas, horarios, trámites, servicios y avisos), con abstención honesta cuando no conoce la respuesta y orientación hacia la atención humana.
2. **Reporte de incidencias:** formulario con categoría, edificio, descripción y prioridad; genera número de ticket y se almacena en base de datos local (SQLite).
3. **Consulta de estado de incidencias:** búsqueda por número de ticket; el MVP registra el estado inicial (recibida) y las transiciones (en proceso / resuelta) están contempladas para el piloto.
4. **Panel de métricas operativas:** volumen de consultas, cobertura automática (porcentaje de consultas respondidas por el catálogo) e incidencias registradas.
5. **Evaluación reproducible:** conjunto de 90 preguntas etiquetadas (desarrollo y prueba) con métricas desglosadas por categoría de consulta y por registro del usuario (formal, coloquial, con errores).
6. **Demo en vivo en Streamlit** ejecutable localmente con `streamlit run app.py`, sin claves de API ni servicios pagos.

## Fuera del alcance del MVP (fases futuras)

- Aplicación móvil nativa y kioscos físicos en el campus.
- Integración con sistemas académicos reales (SIS/LMS), portal de pagos o mensajería (WhatsApp, SMS, correo).
- Mapa interactivo del campus y localización en tiempo real.
- Asistente generativo (LLM), respuesta en varios idiomas y autenticación de usuarios.
- Operación con datos reales de una institución: el catálogo usa el campus ficticio *Universidad Nueva Aurora*.

## Criterios de éxito del MVP

Metas de referencia propuestas junto con este prototipo (no metas acordadas previamente por el equipo), verificadas en el conjunto de prueba:

| Criterio (propuesta de referencia) | Meta | Resultado medido |
|---|---|---|
| Demo ejecutable en vivo | Correr localmente en menos de 5 minutos | Cumplido (3 dependencias, sin claves de API) |
| Acierto en preguntas dentro del catálogo | ≥ 60% en conjunto de prueba | 64.2% |
| Abstención correcta fuera del catálogo | ≥ 50% en conjunto de prueba | 58.3% |
| Latencia del motor | < 1 segundo | 0.8 ms promedio (motor cargado) |
| Trazabilidad de incidencias | Ticket consultable con estado | Cumplido (estado inicial; transiciones contempladas en el diseño) |

## Supuestos y restricciones

- El asistente funciona por **recuperación**, no por generación: solo puede responder lo que está en el catálogo. Esta decisión es deliberada (control de calidad y de sesgos) y está documentada como limitación.
- La base de datos es local: en un alojamiento sin volumen persistente, los tickets no sobreviven reinicios.
- No se solicitan datos personales por diseño; sin embargo, la app almacena texto libre (preguntas y descripciones de incidencias) en una base local sin control de acceso: no es adecuada para incidencias reales confidenciales, y las advertencias visibles piden no escribir datos sensibles.
