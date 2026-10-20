# Informe de evaluación con métricas por subgrupo

## Metodología

Se preparó un conjunto de 90 preguntas etiquetadas, con datos sintéticos redactados imitando la forma natural de consultar de un estudiante dominicano. Este conjunto es material del prototipo de referencia, sujeto a revisión y ampliación por el equipo.

- **Desarrollo (25 preguntas):** una por FAQ, casi idénticas al catálogo. Servir como comprobación de identidad del motor (100% de acierto), no como calibración fina: el umbral de 0.45 fue una elección inicial del diseño, no ajustada con datos de prueba.
- **Prueba (65 preguntas):** 53 paráfrasis nuevas dentro del alcance y 12 fuera de alcance. **Todos los resultados de este informe corresponden al conjunto de prueba, que no se usó para ajustar el umbral ni el catálogo.**

Criterios por pregunta: **acierto** (recupera la FAQ correcta), **omisión** (se abstiene teniendo cobertura), **respuesta incorrecta** (responde con una FAQ equivocada), **abstención correcta** (se abstiene en una pregunta fuera de alcance) y **falso positivo** (responde una pregunta que no debería responder). La latencia medida (0.8 ms por consulta) corresponde al motor ya cargado en el entorno de pruebas de este prototipo; no incluye la latencia de la interfaz web ni la red.

## Resultados globales (conjunto de prueba, n=65)

| Indicador | Valor |
|---|---|
| Preguntas dentro del alcance | 53 |
| Aciertos de recuperación (dentro del alcance) | 34/53 = **64.2%** |
| Tasa de respuesta automática (dentro del alcance, incluye las incorrectas) | 42/53 = 79.2% |
| Omisiones (se abstiene teniendo cobertura) | 11/53 = 20.8% |
| Respuestas incorrectas (dentro del alcance) | 8/53 = 15.1% |
| Preguntas fuera de alcance | 12 |
| Abstención correcta (fuera de alcance) | 7/12 = 58.3% |
| Falsos positivos (fuera de alcance) | 5/12 = 41.7% |
| Latencia media del motor | 0.8 ms |

Aclaración importante: el 64.2% es un indicador operativo del prototipo (coincidencia entre la FAQ recuperada y la esperada por las etiquetas). No mide si la necesidad del usuario quedó resuelta, ni satisfacción, ni ahorro de tiempo institucional; esas dimensiones requieren un piloto con usuarios reales.

## Desempeño por categoría de consulta

| Categoría | n | Acierto | Lectura |
|---|---|---|---|
| Horarios | 11 | **90.9%** | La mejor: preguntas cortas y vocabulario característico |
| Avisos | 8 | 75.0% | Buena, confunde avisos con horarios de cierre |
| Aulas | 12 | 66.7% | Paráfrasis fuertes ("clases de computación") la afectan |
| Trámites | 10 | 60.0% | Confusión entre trámites vecinos (certificado/reintegro) |
| Servicios | 12 | **33.3%** | La peor: vocabulario coloquial disperso (parqueo, aparcar) |
| Fuera de alcance | 12 | 58.3% abstención correcta | Los falsos positivos se agrupan en temas universitarios sin cobertura (becas, residencias) |

## Desempeño por registro del usuario (solo preguntas dentro del alcance)

| Registro | Acierto en alcance | Correcto global (incluye abstenciones correctas) |
|---|---|---|
| Errores de escritura (casi idénticas al catálogo) | 8/8 = **100%** | 100% |
| Formal (paráfrasis) | 8/12 = 66.7% | 58.8% |
| Coloquial (paráfrasis) | 18/33 = 54.5% | 57.5% |

Dos lecturas honestas de esta tabla:

1. El contraste con el grupo "errores" es esperable: esas preguntas son variantes casi idénticas al catálogo (solo tildes y puntuación), mientras que formales y coloquiales son paráfrasis genuinas. El grupo "errores" no es comparable en dificultad con los otros dos; sirve para confirmar la tolerancia ortográfica del motor, no para comparar poblaciones de usuarios.
2. Aun así, la brecha entre paráfrasis formales (66.7%) y coloquiales (54.5%) es una señal exploratoria, no una conclusión: el conjunto es pequeño (n=33 y n=12), fue redactado por los mismos autores del catálogo y no incluye usuarios reales. Sugiere una hipótesis a validar en el piloto (el vocabulario coloquial queda peor cubierto), no una demostración de discriminación por formación académica.

## Métricas de negocio

- **Indicador operativo principal:** de cada 100 consultas dentro del alcance del catálogo, el prototipo responde automáticamente ~79 (de las cuales ~64 correctas y ~15 incorrectas) y deriva ~21 a orientación humana por abstención. Sobre el conjunto completo (incluyendo fuera de alcance), la tasa de respuesta automática es 72.3%.
- **Hipótesis pendiente de validar (no medición):** el ahorro de tiempo operativo depende de qué proporción de las consultas reales de bedelía corresponde a FAQs de este tipo y de si la respuesta automática resuelve la necesidad del usuario; ambos solo pueden medirse con un piloto con usuarios reales.
- **Costo por consulta:** esta implementación no hace llamadas a servicios pagados (recuperación local); el costo unitario real solo existiría al escalar a un piloto con servidor dedicado (ver diseño de solución).
- **Trazabilidad:** todas las incidencias registradas en la demo generan ticket consultable; el MVP registra el estado inicial (recibida) y el diseño contempla las transiciones en proceso/resuelta para el piloto.

## Hallazgos y trabajo futuro

1. La categoría **servicios** es la más débil (33.3%): su vocabulario real es muy diverso (wifi, parqueo, impresión). Ampliar el catálogo con paráfrasis reales de usuarios es la mejora de mayor impacto.
2. Los **falsos positivos** se concentran en temas universitarios sin cobertura (becas → confundido con reintegro; residencias → horarios de cierre). Un clasificador previo dentro/fuera de alcance, o subir el umbral (con costo en omisiones), son mitigaciones posibles.
3. El contraste por registro sugiere evaluar **embeddings semánticos** en la fase siguiente, validando que no reduzcan la abstención correcta.
