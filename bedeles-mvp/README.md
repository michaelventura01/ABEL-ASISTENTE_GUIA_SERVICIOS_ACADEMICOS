# ABEL / Bedeles — Documentación técnica

**Versión:** MVP con interfaz azul  
**Fecha:** 23 de octubre de 2026  
**Estado:** prototipo académico; no certificado para producción.

## 1. Propósito y alcance técnico

ABEL / Bedeles es una aplicación web de demostración para orientar a estudiantes sobre servicios universitarios y registrar incidencias. La interfaz se construye con Streamlit. La recuperación de preguntas frecuentes utiliza un catálogo CSV y scikit-learn; las consultas y las incidencias se guardan en SQLite local.

La institución y los datos incluidos (`Universidad Nueva Aurora`) son ficticios. No debe utilizarse con información personal, credenciales o casos reales confidenciales.

## 2. Arquitectura lógica

```text
Navegador
   │
   ▼
Streamlit (app.py)
   ├── Interfaz: Asistente / Reportar incidencia / Consultar estado / Métricas
   ├── FAQRetriever (src/retriever.py)
   │      ├── data/faq.csv
   │      └── data/faq_aliases.csv
   └── Persistencia (src/incidencias.py)
          └── SQLite local (data/bedeles.db por defecto)
```

### Componentes

- **`app.py`**: configura la página, define la identidad visual CSS azul, crea las cuatro pestañas y conecta las acciones de usuario con el recuperador y las funciones de persistencia.
- **`src/retriever.py`**: recupera una respuesta del catálogo mediante similitud textual; considera preguntas originales y variantes, combina puntuaciones por FAQ y aplica un umbral para decidir si responde o se abstiene.
- **`src/incidencias.py`**: inicializa SQLite y expone funciones para crear y consultar incidencias, registrar consultas, listar incidencias y calcular métricas.
- **`data/faq.csv`**: catálogo de preguntas frecuentes y respuestas demostrativas.
- **`data/faq_aliases.csv`**: variantes de formulación asociadas a las FAQs para mejorar la recuperación.
- **`data/test_set.csv`**: conjunto de evaluación etiquetado.
- **`eval/evaluate.py`**: ejecuta la evaluación sobre los conjuntos disponibles y produce CSV/JSON con resultados y métricas.
- **`tests/`**: pruebas del recuperador y de la interfaz Streamlit.
- **`assets/`**: imágenes y recursos visuales del proyecto.

## 3. Tecnologías y dependencias

| Tecnología | Uso |
|---|---|
| Python 3.11 o 3.12 recomendado | Runtime |
| Streamlit 1.66.0 | Aplicación web |
| pandas 3.0.6 | Lectura y tratamiento de datos tabulares |
| scikit-learn 1.9.1 | Recuperación basada en similitud textual |
| SQLite | Persistencia local sin servidor externo |
| CSV | Catálogo FAQ, alias y datos de evaluación |

No requiere API key de IA generativa, Docker ni base de datos externa para el modo demo.

## 4. Requisitos de ejecución

- Python 3.11/3.12 recomendado.
- `pip` y `venv`.
- Acceso a Internet para instalar las dependencias.
- Permisos de escritura en la carpeta de datos o configuración de una ruta alternativa para SQLite.

## 5. Instalación en Ubuntu / Linux

Desde la raíz del repositorio:

```bash
cd bedeles-mvp
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Si no existe `venv`:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip
```

Comprobar dependencias:

```bash
python -c "import streamlit, pandas, sklearn; print(streamlit.__version__, pandas.__version__, sklearn.__version__)"
```

## 6. Ejecutar la aplicación

```bash
python -m streamlit run app.py
```

Abrir la dirección local mostrada por Streamlit; normalmente `http://localhost:8501`. Detener con `Ctrl+C`.

Para ejecutar la aplicación en un equipo de la red local, Streamlit puede enlazarse a una interfaz accesible por red, pero no se recomienda exponer el MVP sin autenticación y controles de seguridad. Si se requiere acceso en LAN, configurar explícitamente el host y el firewall conforme a la política local.

## 7. Base de datos y persistencia

La aplicación inicializa SQLite mediante `inicializar_db()`. La ruta por defecto se determina en el módulo de incidencias; el README del proyecto documenta la opción `BEDELES_DB` para usar una ruta alternativa.

Ejemplo temporal:

```bash
BEDELES_DB=/tmp/bedeles-test.db python -m streamlit run app.py
```

La persistencia es local. En contenedores o plataformas efímeras, el archivo puede perderse al reiniciar o volver a desplegar. La base de datos no incorpora por sí misma autenticación ni autorización.

## 8. Pruebas y evaluación

### Validación estática y pruebas

```bash
python -m compileall -q app.py src tests eval
python tests/test_retriever.py
python tests/test_app.py
```

### Evaluación del recuperador

```bash
python eval/evaluate.py --conjunto dev --umbral 0.60
python eval/evaluate.py --conjunto test --umbral 0.60
```

Los resultados se escriben en `eval/`. Las métricas disponibles son sobre un conjunto sintético de 65 preguntas; no son garantía de calidad con usuarios reales. Mantener un conjunto de prueba independiente y no ajustar repetidamente el sistema contra él.

## 9. Configuración visual

La identidad visual usa una paleta azul:

| Token | Color |
|---|---|
| Azul profundo | `#123B82` |
| Azul principal | `#2378F7` |
| Celeste | `#54B8FF` |
| Azul pálido | `#DCEEFF` |
| Fondo | `#F3F8FF` |
| Texto | `#183568` |

En la versión actual, los estilos están definidos dentro del bloque CSS de `app.py`. Si se extraen a un archivo externo, debe mantenerse la ruta y la carga del CSS de forma coherente.

## 10. Seguridad, privacidad y limitaciones

- El campus y el catálogo son ficticios.
- No introducir contraseñas, matrículas, información médica ni datos sensibles.
- El texto de las consultas puede guardarse en SQLite para métricas; informar al usuario y minimizar los datos retenidos.
- Las incidencias se guardan localmente y la demo advierte que no existe control de acceso a tickets.
- Antes de un piloto real: definir autenticación, autorización por rol, política de retención, copias de seguridad, acceso a la base, registro seguro, validación de entradas y responsable institucional de las FAQs.
- La aplicación recupera respuestas existentes; no es un chatbot generativo y no debe prometer información que no esté en el catálogo.
- La abstención y el umbral deben evaluarse con preguntas reales y aprobadas por responsables de servicios académicos.

## 11. Operación y mantenimiento

1. Revisar las FAQs con el departamento responsable.
2. Añadir o corregir respuestas y variantes en los CSV correspondientes.
3. Ejecutar pruebas unitarias y evaluación.
4. Revisar errores, omisiones y falsas coincidencias.
5. Respaldar la base SQLite si se necesita conservar el historial.
6. Registrar versión, fecha de actualización y responsable de los cambios.

## 12. Estructura del proyecto

```text
bedeles-mvp/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── faq.csv
│   ├── faq_aliases.csv
│   └── test_set.csv
├── src/
│   ├── retriever.py
│   └── incidencias.py
├── tests/
│   ├── test_retriever.py
│   └── test_app.py
├── eval/
│   ├── evaluate.py
│   ├── resultados_dev.csv
│   ├── resultados_test.csv
│   └── métricas JSON
├── assets/
└── docs/
```

## 13. Estado de validación conocido

En una validación previa de componentes se informó que la compilación sintáctica de Python, las pruebas aisladas del recuperador y una prueba de SQLite pasaron. La prueba integral de interfaz quedó pendiente en ese entorno porque Streamlit no estaba instalado y no se pudo descargar. La validación definitiva debe ejecutarse en el equipo donde se instalará el proyecto y documentar los resultados actuales.


