# Canvas actualizado con lo aprendido (v2)

Cambios al Business Model Canvas v1 a partir de la evidencia del MVP. Cada cambio indica qué bloque se modifica y con qué evidencia. El equipo debe reflejar estos ajustes en Canvanizer antes de la entrega.

## Cambios por bloque

| Bloque | Canvas v1 | Canvas v2 (corregido) | Evidencia del MVP |
|---|---|---|---|
| Propuesta de valor | "Atención inmediata 24/7" | "Atención 24/7 para consultas del catálogo, con orientación hacia atención humana" | El MVP recupera la FAQ correcta en 64.2% de las consultas en alcance (respuesta automática 79.2%): la promesa se matiza; el canal humano sigue siendo parte del servicio |
| Propuesta de valor | "Un solo punto para orientación, incidencias, avisos y solicitudes" | Se mantiene, con alcance explícito: MVP cubre consultas frecuentes + incidencias; avisos y solicitudes formales van por fases | El MVP solo implementa FAQ + incidencias (ver definición de alcance) |
| Canales | Portal web, app móvil, kioscos, QR | **Web primero**: demo Streamlit responsiva + código QR al enlace; app móvil y kioscos pasan a fases futuras | La demo web fue el único canal construido y validado en la Fase 2; la app móvil/kioscos no tienen evidencia aún |
| Actividades clave | "Carga y entrenamiento del asistente" | "Curaduría y ampliación continua del catálogo de FAQs" | Ampliar el catálogo es la mejora de mayor impacto según la evaluación (brecha por registro); no requiere re-entrenar nada |
| Recursos clave | Intelectuales: plataforma, base de conocimiento | Se fortalece: la **base de conocimiento es el activo central**; la tecnología de recuperación es commodity | La evaluación mostró que el desempeño depende del catálogo, no del algoritmo (TF-IDF simple alcanzó 64% con 25 FAQs) |
| Estructura de costos | "Nube, hosting y licencias de IA (variables según uso)" | MVP y piloto: **USD 0 en licencias de IA** (recuperación local TF-IDF); costo piloto estimado: VPS USD 12–20/mes + dominio; licencias de IA solo si se adopta LLM en fases futuras | Esta implementación corre sin servicios de IA pagados; las estimaciones del piloto no están verificadas (sección presupuesto del diseño de solución) |
| Relación con clientes | "Canal de escalamiento a personal humano para casos complejos" | El escalamiento humano se convierte en **componente permanente y medible** del servicio, no un extra | Las abstenciones (20.8% dentro del alcance) y falsos positivos (41.7% fuera de alcance) hacen imprescindible el canal humano |
| Socios clave | Proveedores de SIS/LMS, mensajería (WhatsApp/SMS) | Se mueven a fases futuras; en el piloto el socio clave es la **propia universidad** (dueña de la información institucional y del personal de bedelía) | El MVP demostró que sin datos institucionales reales el catálogo es la restricción; el socio crítico es quien aporta ese contenido |
| Segmentos | "Campus con alto volumen de consultas" | Se precisa: piloto en **una facultad/bedelía central** de una universidad, con personal de bedelía dispuesto a curar el catálogo | La lección del MVP: el valor depende de la calidad del contenido local; empezar pequeño facilita la curaduría |
| Flujos de ingresos | Suscripción SaaS, planes escalonados | **Sin cambios, pero ahora marcados como hipótesis no validadas**: el MVP no midió disposición a pagar ni satisfacción; se validan en el piloto con compradores reales | Ninguna métrica comercial fue medida en la Fase 2 |

## Qué se aprendió y qué sigue abierto

**Validado con evidencia técnica:** el flujo consulta → respuesta automática → orientación al canal humano funciona y es medible; la trazabilidad de incidencias con ticket es factible con tecnología gratuita; esta implementación no incurre en servicios pagados. **Nota de causalidad:** el desempeño medido es consistente con que el catálogo es la restricción, pero con un solo prototipo no se puede afirmar que el algoritmo sea indiferente: es una hipótesis razonable a validar con más catálogos y usuarios reales.

**Abierto (hipótesis del piloto):** proporción de consultas reales que son FAQs; ahorro de tiempo operativo percibido por bedelía; disposición a pagar de las universidades; adopción del canal por estudiantes.

**Acción requerida del equipo:** actualizar el Canvas en Canvanizer (versión v2, fecha de la entrega) reflejando esta tabla, y enlazar el canvas actualizado en la carpeta de evidencias.
