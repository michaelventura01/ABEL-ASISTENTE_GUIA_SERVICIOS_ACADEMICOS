# Guía paso a paso: instalar, ejecutar y validar Bedeles MVP

## A. Preparación

1. Instala Python 3.11 o 3.12.
2. Clona el repositorio y entra en la carpeta de la aplicación:

   ```bash
   git clone https://github.com/michaelventura01/ABEL-ASISTENTE_GUIA_SERVICIOS_ACADEMICOS.git
   cd ABEL-ASISTENTE_GUIA_SERVICIOS_ACADEMICOS/bedeles-mvp
   ```

3. Crea y activa un entorno virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   ```

   En Windows PowerShell, usa `py -3.12 -m venv .venv` y `\.venv\Scripts\Activate.ps1`.

4. Instala las dependencias:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Verifica imports y versiones:

   ```bash
   python -c "import streamlit, pandas, sklearn; print(streamlit.__version__, pandas.__version__, sklearn.__version__)"
   ```

## B. Arranque

Desde la carpeta que contiene `app.py`:

```bash
python -m streamlit run app.py
```

Abre `http://localhost:8501` si Streamlit no abre el navegador automáticamente. Detén el servidor con `Ctrl+C`.

## C. Pruebas de código

```bash
python -m compileall -q app.py src tests eval
python tests/test_retriever.py
python tests/test_app.py
python eval/evaluate.py --conjunto dev --umbral 0.60
python eval/evaluate.py --conjunto test --umbral 0.60
```

`test_app.py` requiere Streamlit instalado. Las evaluaciones generan métricas y CSV en `eval/`.

## D. Pruebas manuales de aceptación

1. En la pestaña **Asistente**, pregunta `¿Dónde queda el aula 302?`; debe responder con el Edificio Central.
2. Pregunta `¿Dónde quedan los laboratorios de informática?`; debe devolver la FAQ de laboratorios de informática.
3. Pregunta `¿Cuál es el sentido de la vida?`; debe abstenerse y mostrar el mensaje de orientación.
4. Pregunta `¿Cómo cambio mi contraseña del correo institucional?`; debe abstenerse y no devolver una FAQ de contacto con profesores.
5. En **Reportar incidencia**, envía una descripción de 10 caracteres o más y confirma que se genera un ticket.
6. Busca ese ticket en **Consultar estado**.
7. Abre **Panel de métricas** y comprueba que se reflejen las consultas y las incidencias.

## E. Modificaciones incluidas

- Alias editoriales para las 25 preguntas frecuentes en `data/faq_aliases.csv`.
- Recuperación por similitud máxima entre la consulta y las variantes de cada FAQ.
- Umbral conservador por defecto de `0.60`.
- Abstención explícita para solicitudes de contraseñas/credenciales.
- Pruebas unitarias del recuperador.

En el conjunto sintético de prueba (65 preguntas), esta versión obtuvo 45/53 respuestas correctas dentro del alcance, 0 respuestas incorrectas dentro del alcance y abstención en 12/12 consultas etiquetadas fuera del alcance. Ocho preguntas cubiertas se abstuvieron; deben analizarse antes de considerar el MVP listo para un piloto.

## F. Límites y seguridad

- Los datos de la Universidad Nueva Aurora son ficticios.
- SQLite no implementa usuarios ni permisos; no expongas los tickets en Internet sin añadir controles.
- Las consultas y descripciones se guardan localmente; no introduzcas datos sensibles.
- Los resultados de prueba son sintéticos y no sustituyen pruebas con usuarios reales.
