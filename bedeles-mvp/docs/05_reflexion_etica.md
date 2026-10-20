# Reflexión ética: riesgos de sesgo y mitigaciones

Esta reflexión está ligada a las mediciones reales del prototipo de referencia, no a escenarios genéricos.

## ¿De dónde puede venir el sesgo?

**1. Datos y cobertura del catálogo.** El catálogo de 25 FAQs fue redactado por los autores del prototipo, para un campus ficticio. Esa forma de preguntar no representa a toda la población estudiantil, y la evaluación lo señala: las preguntas casi idénticas al catálogo se recuperan al 100%, pero las paráfrasis coloquiales dominicanas ("¿Hay parqueo para gente de afuera?", "¿Dónde se paga la carrera?") caen al 54.5% de acierto, y las formales al 66.7%. **A quién podría afectar:** estudiantes que escriben de forma coloquial o con menos exposición a registros formales recibirían más abstenciones y más respuestas erróneas. Conviene ser honestos con el límite de la evidencia: el conjunto de prueba es sintético, pequeño y redactado por los mismos autores, así que esta brecha es una señal exploratoria (una hipótesis sobre cobertura de vocabulario) y no una demostración de discriminación hacia ningún grupo. Validarla o descartarla es tarea del piloto.

**2. Proxies y decisiones automatizadas.** El formulario de incidencias usa listas cerradas (4 edificios, 6 categorías) y prioridad autodeclarada. Quien reporta desde un edificio fuera de la lista queda mal clasificado, y la prioridad la define quien reporta, no un criterio operacional: un reporte "baja" de una persona que subestima la urgencia puede esperar más de lo justo. **A quién podría afectar:** usuarios de zonas menos representadas en el diseño del formulario.

**3. Bucles de retroalimentación.** El panel de métricas solo ve lo que pasa por el sistema: si la universidad reasigna personal de bedelía con base en "el bot responde el 79% de las consultas del catálogo", las consultas de quienes no usan el sistema (sin smartphone, sin datos móviles, con discapacidad visual que dificulta el chat) desaparecen de las estadísticas y, por tanto, de la justificación de recursos. **A quién podría afectar:** la población menos digitalizada, justo la que más depende de la atención presencial que el proyecto quiere reducir.

**4. Falsos positivos con apariencia de autoridad.** En la evaluación, la pregunta "¿Cómo hackeo el wifi de la universidad?" recibió como respuesta la FAQ del horario de cierre del campus (similitud 0.558, por encima del umbral), y una consulta de becas fue respondida con el trámite de reintegro. Una respuesta automática con tono institucional, aunque errónea, puede convencer a un estudiante de que un trámite imposible es posible (o viceversa). **A quién podría afectar:** estudiantes de primer ingreso, con menos criterio para detectar la respuesta incorrecta.

**5. Privacidad y datos.** El MVP no solicita datos personales por diseño, pero sí almacena texto libre (la pregunta del chat y la descripción de la incidencia) en una base local, y la consulta de tickets por número no tiene control de acceso. Por eso la interfaz lleva advertencias visibles ("demo con datos ficticios; no escribas nombres, matrículas ni contraseñas") y la documentación declara que esta base no es adecuada para incidencias reales confidenciales. Un despliegue real requeriría autenticación y políticas de retención.

## Mitigaciones aplicadas y propuestas

**Ya implementadas en el prototipo:**

- Abstención por diseño: sin confianza suficiente, el sistema admite que no sabe y orienta hacia la atención humana (visitar la bedelía o reportar una incidencia); no inventa respuestas. Cabe la precisión: el MVP orienta, no escala automáticamente el caso a una persona (no hay notificación ni asignación).
- Aviso de respuesta aproximada cuando la similitud es baja, y catalogación del campus como ficticio para no atribuir información inventada a una institución real.
- Advertencias visibles sobre datos ficticios y sensibles en el chat y el formulario, y documentación de las limitaciones de la base local.

**Propuestas para el piloto (con responsables):**

1. Ampliar el catálogo con paráfrasis redactadas por usuarios reales y diversos (equipo de producto), no solo por el equipo técnico, y re-medir la brecha por registro en cada iteración.
2. Mantener el canal humano como salida permanente: medir el volumen de consultas orientadas al canal presencial como indicador de salud del sistema, no como fracaso (equipo de operaciones).
3. Revisar las listas cerradas del formulario con personal de bedelía real antes del piloto (equipo de diseño).
4. Reportar métricas del sistema digital junto con las del canal presencial en decisiones de personal (gestión de la universidad).
5. Pruebas de accesibilidad con usuarios con discapacidad visual antes de considerar el canal chat suficiente (equipo de diseño).
6. Definir autenticación y políticas de retención de datos antes de cualquier uso con usuarios reales (equipo técnico).

## Conclusión

El mayor riesgo ético del proyecto no es técnico sino de gobernanza: que la universidad use el porcentaje de respuesta automática para justificar recortes de atención humana, dejando fuera a quienes menos usan el canal digital. La mitigación principal ya está en la arquitectura: la abstención honesta y la orientación hacia el canal humano como parte del diseño, no como excepción. Lo que el MVP garantiza es que no inventa respuestas; lo que no garantiza (todavía) es que la respuesta automática resuelva la necesidad del usuario: eso se valida en el piloto.
