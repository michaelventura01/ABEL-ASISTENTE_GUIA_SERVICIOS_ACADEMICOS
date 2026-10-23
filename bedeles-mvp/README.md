# Bedeles · Asistencia Universitaria Inteligente (MVP)

MVP de un asistente de orientación universitaria con cuatro funciones: preguntas frecuentes, registro de incidencias con ticket, consulta del estado del ticket y panel de métricas.

> **Demo académica:** el catálogo representa a la Universidad Nueva Aurora, una institución ficticia. Sustituye y valida la información con la institución real antes de cualquier piloto. No introduzcas contraseñas, matrículas, datos de salud ni otra información sensible.

## 1. Requisitos

- Python 3.11 o 3.12 recomendado.
- `pip` y `venv`.
- Conexión a Internet para instalar las dependencias la primera vez.
- Aproximadamente 200 MB libres.
- No necesita API key, modelo generativo, base de datos externa ni Docker.

## 2. Descargar el proyecto

Este repositorio contiene la aplicación dentro de la carpeta `bedeles-mvp`.

```bash
git clone https://github.com/michaelventura01/ABEL-ASISTENTE_GUIA_SERVICIOS_ACADEMICOS.git
cd ABEL-ASISTENTE_GUIA_SERVICIOS_ACADEMICOS/bedeles-mvp
```

Si descargaste un ZIP desde GitHub, descomprímelo y entra en la carpeta `bedeles-mvp` que contiene `app.py` y `requirements.txt`.

## 3. Crear el entorno virtual

### Ubuntu / Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Si `venv` no está disponible en Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip
```

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Si PowerShell bloquea la activación, puedes ejecutar el intérprete directamente con `.venv\Scripts\python.exe` o seguir la política de ejecución aprobada por tu organización.

## 4. Instalar dependencias

Con el entorno virtual activado:

```bash
python -m pip install -r requirements.txt
```

Comprueba las dependencias:

```bash
python -c "import streamlit, pandas, sklearn; print('Streamlit', streamlit.__version__); print('Pandas', pandas.__version__); print('scikit-learn', sklearn.__version__)"
```

Si la instalación falla por falta de Internet o por una versión de Python incompatible, revisa el error de `pip`; no continúes hasta que la importación anterior funcione.

## 5. Ejecutar ABEL / Bedeles

Desde la carpeta `bedeles-mvp` y con el entorno activado:

```bash
python -m streamlit run app.py
```

Abre la URL local que muestra la terminal, normalmente `http://localhost:8501`.

Para detener la aplicación, vuelve a la terminal y pulsa `Ctrl+C`.

## 6. Probar el motor de respuestas

Estas pruebas no requieren que la interfaz Streamlit esté ejecutándose:

```bash
python tests/test_retriever.py
python -m compileall -q app.py src tests eval
```

Ejecuta la evaluación del conjunto de desarrollo y del conjunto de prueba:

```bash
python eval/evaluate.py --conjunto dev --umbral 0.60
python eval/evaluate.py --conjunto test --umbral 0.60
```

La evaluación genera/actualiza `eval/resultados_*.csv` y `eval/metricas_*.json`. El conjunto de prueba tiene 65 casos; no debe utilizarse para ajustar repetidamente el sistema sin crear otro conjunto independiente de validación.

## 7. Ejecutar pruebas de interfaz

Con todas las dependencias instaladas:

```bash
python tests/test_app.py
```

Estas pruebas utilizan `streamlit.testing.v1.AppTest` y una base de datos temporal. Si aparece `ModuleNotFoundError: streamlit`, activa el entorno virtual correcto e instala `requirements.txt`.

## 8. Qué cambió en esta versión

- `src/retriever.py`: el motor indexa tanto las preguntas oficiales como sus variantes editoriales, agrega las puntuaciones por FAQ y valida el umbral.
- `data/faq_aliases.csv`: incorpora formulaciones alternativas para las 25 FAQs.
- Umbral predeterminado elevado de `0.45` a `0.60` para priorizar la precisión y reducir respuestas no sustentadas.
- Peticiones explícitas de contraseña/credenciales se abstienen en lugar de recuperar una FAQ no relacionada.
- `tests/test_retriever.py`: pruebas independientes del motor, incluida la abstención para solicitudes sensibles.
- `docs/07_instalacion_y_validacion.md`: guía de instalación, ejecución, pruebas y límites conocidos.

### Resultado de evaluación de referencia

Con `--conjunto test --umbral 0.60`, en el conjunto sintético actual:

- Acierto entre preguntas dentro del alcance: **84.9% (45/53)**.
- Respuestas incorrectas dentro del alcance: **0/53**.
- Omisiones dentro del alcance: **8/53 (15.1%)**.
- Abstención correcta en preguntas fuera de alcance: **12/12 (100%)**.

Estos resultados son una medición del conjunto de prueba del proyecto, no una garantía sobre consultas de usuarios reales. Las variantes añadidas deben revisarse por una persona que conozca los servicios de la institución.

## 9. Base de datos

SQLite crea `data/bedeles.db` automáticamente al iniciar o utilizar la aplicación. Para pruebas, se puede cambiar la ruta sin tocar la base principal:

### Linux / macOS

```bash
BEDELES_DB=/tmp/bedeles-test.db python -m streamlit run app.py
```

### Windows PowerShell

```powershell
$env:BEDELES_DB = "$env:TEMP\bedeles-test.db"
python -m streamlit run app.py
```

La base local no tiene autenticación ni autorización. No la expongas públicamente ni la uses para gestionar incidencias confidenciales sin controles adicionales.

## 10. Estructura

```text
bedeles-mvp/
├── app.py
├── requirements.txt
├── data/
│   ├── faq.csv
│   ├── faq_aliases.csv
│   └── test_set.csv
├── src/
│   ├── retriever.py
│   └── incidencias.py
├── tests/
│   ├── test_app.py
│   └── test_retriever.py
├── eval/
└── docs/
```

## 11. Límites antes de producción

- Reemplazar la institución ficticia por datos oficiales revisados y con fecha de actualización.
- Proteger o no almacenar texto libre sensible; definir retención y acceso a tickets.
- Añadir autenticación/autorización si se publica fuera del equipo local.
- Configurar despliegue persistente: el almacenamiento local puede perderse en servicios efímeros.
- Probar con preguntas reales, con consentimiento y sin datos personales; revisar falsos positivos y omisiones.
- Definir un responsable institucional para mantener las FAQs y los alias actualizados.
