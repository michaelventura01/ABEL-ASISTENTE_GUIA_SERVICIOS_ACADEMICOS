# Bedeles · Asistencia Universitaria Inteligente (MVP)

MVP del **Grupo 3** para la asignatura *Implementación de Robots y Máquinas Inteligentes (Capstone Projects)*, Maestría en Ciencias de Datos e Inteligencia Artificial, UASD.

Bedeles es un asistente que responde consultas frecuentes de la vida universitaria (aulas, horarios, trámites, servicios y avisos), registra incidencias del campus con número de ticket y muestra un panel de métricas operativas.

**Importante:** el asistente funciona por **recuperación** (busca la FAQ más parecida del catálogo), no por generación. Si no encuentra una respuesta con suficiente confianza, **se abstiene** y orienta hacia la atención humana o el registro de una incidencia. Todo el catálogo corresponde a la **Universidad Nueva Aurora, un campus ficticio** creado para este proyecto; ningún dato proviene de una institución real.

Este repositorio es el **prototipo de referencia del Grupo 3** para la Fase 2: una propuesta de alcance, diseño y MVP que el equipo puede revisar, ajustar y ampliar antes de la entrega.

## ¿Qué hace el proyecto?

1. **Asistente (chat):** recibe una pregunta en lenguaje natural y responde con la FAQ del catálogo más similar (TF-IDF sobre n-gramas de caracteres + similitud coseno). Si la similitud no supera el umbral (0.45), reconoce que no sabe y orienta hacia la atención humana. Al elegir un ejemplo rápido, la pregunta se envía al asistente.
2. **Reportar incidencia:** formulario con categoría, edificio, descripción y prioridad. Cada reporte genera un **número de ticket** (almacenado en SQLite). La demo incluye advertencias visibles para no escribir datos personales.
3. **Consultar estado:** búsqueda de incidencia por número de ticket (muestra el estado inicial; las transiciones en proceso/resuelta están contempladas para el piloto).
4. **Panel de métricas:** volumen de consultas, tasa de respuesta automática (cuántas consultas respondió el catálogo) e incidencias registradas.

## Pruebas

La app cuenta con pruebas funcionales automáticas (`streamlit.testing.v1.AppTest`) que cubren: pregunta cubierta, abstención, ejemplo rápido, formulario inválido, creación de ticket y consultas de ticket existente/inexistente.

```bash
python tests/test_app.py
```

## Requisitos

- Python 3.14.3 (probado; el código debería correr en 3.10+, pero solo se verificó 3.14)
- ~200 MB de espacio para las dependencias

## Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/<usuario>/bedeles-mvp.git
cd bedeles-mvp

# 2. (Opcional pero recomendado) crear un entorno virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la demo
streamlit run app.py
```

La aplicación se abre sola en el navegador (por defecto en `http://localhost:8501`). No requiere claves de API ni conexión a servicios externos.

## Evaluación

El repositorio incluye un conjunto de evaluación etiquetado (`data/test_set.csv`) con 90 preguntas: paráfrasis de las 25 FAQs en tres registros (formal, coloquial y con errores de escritura) y 12 preguntas fuera de alcance (becas, residencias, temas no universitarios).

```bash
# Comprobación de identidad con el conjunto de desarrollo (25 preguntas casi idénticas al catálogo)
python eval/evaluate.py --conjunto dev --umbral 0.45

# Resultados reportados: conjunto de prueba (65 preguntas)
python eval/evaluate.py --conjunto test --umbral 0.45
```

El script imprime las métricas por categoría y por registro, y guarda los artefactos en `eval/`:

- `eval/resultados_test.csv`: predicción individual de cada pregunta (reproducible).
- `eval/metricas_test.json`: métricas globales y por subgrupo.

## ¿De dónde salen los datos?

| Archivo | Contenido | Origen |
|---|---|---|
| `data/faq.csv` | 25 preguntas frecuentes con su respuesta | Datos sintéticos elaborados para este prototipo (campus ficticio) |
| `data/test_set.csv` | 90 preguntas etiquetadas para evaluación | Datos sintéticos elaborados para este prototipo |
| `data/bedeles.db` | Incidencias y consultas del chat | Se crea automáticamente con SQLite al usar la app |

No se usaron datos personales ni de estudiantes reales. Las preguntas del conjunto de prueba imitan la forma natural de consultar de un estudiante (incluyendo coloquialismos dominicanos) y no se usaron para ajustar el motor, solo para medirlo; el conjunto de desarrollo (una pregunta casi idéntica por FAQ) sirvió como comprobación de identidad, y el umbral 0.45 fue una elección inicial del diseño.

Entorno probado: Python 3.14, con las versiones fijas de `requirements.txt`.

## Estructura del repositorio

```
bedeles-mvp/
├── app.py              # Demo Streamlit (chat, incidencias, estado, panel)
├── requirements.txt    # Dependencias (versiones fijas)
├── tests/test_app.py   # Pruebas funcionales (streamlit.testing)
├── src/
│   ├── retriever.py    # Motor de recuperación TF-IDF + umbral de abstención
│   └── incidencias.py  # Registro de incidencias y consultas (SQLite)
├── data/
│   ├── faq.csv         # Catálogo de conocimiento (campus ficticio)
│   └── test_set.csv    # Conjunto de evaluación etiquetado
├── eval/
│   ├── evaluate.py    # Cálculo de métricas por subgrupo
│   ├── resultados_test.csv
│   └── metricas_test.json
└── docs/               # Documentación de la Fase 2
```

## Limitaciones conocidas

- El catálogo tiene 25 FAQs de demostración; un despliegue real requeriría cargar la información institucional de cada universidad.
- La base SQLite es local y sin control de acceso: no es adecuada para incidencias reales confidenciales; en un alojamiento efímero los tickets no sobreviven reinicios.
- El asistente no solicita datos personales por diseño, pero almacena texto libre (preguntas y descripciones): las advertencias visibles piden no escribir datos sensibles.
- El motor responde en menos de 1 ms ya cargado; la latencia completa de la interfaz web no fue medida.
- El MVP registra el estado inicial del ticket (recibida); las transiciones de estado están contempladas para el piloto.
- La evaluación usa un conjunto sintético pequeño; sus resultados son indicadores del prototipo, no mediciones con usuarios reales.
