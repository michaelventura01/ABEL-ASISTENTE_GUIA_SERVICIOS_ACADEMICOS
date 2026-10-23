"""Demo del MVP Bedeles: asistente de orientación e incidencias universitarias.

Campus de referencia: Universidad Nueva Aurora (institución ficticia creada
para este proyecto; toda la información del catálogo es demostrativa).

Ejecutar con: streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.incidencias import (  # noqa: E402
    CATEGORIAS_INCIDENCIA,
    ESTADOS_INCIDENCIA,
    crear_incidencia,
    consultar_incidencia,
    inicializar_db,
    listar_incidencias,
    registrar_consulta,
    resumen_metricas,
)
from src.retriever import FAQRetriever  # noqa: E402

FAQ_PATH = Path(__file__).resolve().parent / "data" / "faq.csv"
MENSAJE_ABSTENCION = (
    "No tengo esa información en mi catálogo todavía. Puedes: (1) reportarla "
    "como incidencia u observación en la pestaña *Reportar incidencia*, o "
    "(2) visitar la bedelía (Edificio Central, planta baja, cubículo 5) en "
    "horario de oficina."
)


@st.cache_resource
def cargar_retriever() -> FAQRetriever:
    return FAQRetriever(FAQ_PATH)


def main() -> None:
    st.set_page_config(
        page_title="Bedeles · Asistencia Universitaria Inteligente",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    inicializar_db()

    # Cargar el tema visual desde un archivo CSS independiente.
    css_path = Path(__file__).resolve().parent / "assets" / "abel_theme.css"
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )

    # Cabecera de ABEL.
    st.markdown(
        """
        <header class="abel-hero">
          <div class="abel-hero-row">
            <div class="abel-logo">🎓</div>
            <div>
              <h1>Bedeles · Asistencia Universitaria Inteligente</h1>
              <p>MVP del Grupo 3 · Maestría en Ciencias de Datos e IA (UASD). Datos del campus ficticio <em>Universidad Nueva Aurora</em>.</p>
            </div>
          </div>
        </header>
        """,
        unsafe_allow_html=True,
    )

    tab_chat, tab_reportar, tab_estado, tab_panel = st.tabs(
        ["💬 Asistente", "📋 Reportar incidencia", "🔎 Consultar estado", "📊 Panel de métricas"]
    )

    with tab_chat:
        st.subheader("💬 Consulta al asistente")
        st.markdown(
            "Pregunta sobre aulas, horarios, trámites, servicios o avisos. "
            "Si el asistente no sabe la respuesta, te lo dirá y te indicará "
            "dónde acudir. **Demo con datos ficticios:** no escribas nombres, "
            "matrículas, contraseñas ni información sensible."
        )
        ejemplo = st.selectbox(
            "Ejemplos rápidos (elige uno y se enviará al asistente)",
            index=None,
            placeholder="Elige un ejemplo…",
            options=[
                "¿Dónde queda el aula 302?",
                "¿A qué hora abre la biblioteca?",
                "¿Cómo retiro una asignatura?",
                "¿Cómo solicito una beca?",  # fuera de alcance a propósito
            ],
        )

        if "mensajes" not in st.session_state:
            st.session_state["mensajes"] = []

        def responder(pregunta: str) -> None:
            st.session_state["mensajes"].append({"rol": "user", "contenido": pregunta})
            retriever = cargar_retriever()
            resultado = retriever.responder(pregunta)
            registrar_consulta(pregunta, resultado)

            if resultado.abstiene:
                contenido = MENSAJE_ABSTENCION
            else:
                contenido = resultado.respuesta
                if resultado.similitud < 0.60:
                    contenido = (
                        f"{resultado.respuesta}\n\n"
                        "_(Respuesta aproximada; si no es lo que buscabas, "
                        "reformúlala o repórtala como incidencia.)_"
                    )
            st.session_state["mensajes"].append({"rol": "assistant", "contenido": contenido})

        # Enviar el ejemplo elegido al asistente (una sola vez por selección)
        if ejemplo and st.session_state.get("ejemplo_enviado") != ejemplo:
            st.session_state["ejemplo_enviado"] = ejemplo
            responder(ejemplo)

        pregunta = st.chat_input("Escribe tu consulta…")
        if pregunta:
            responder(pregunta)

        for m in st.session_state["mensajes"]:
            with st.chat_message(m["rol"]):
                st.markdown(m["contenido"])

        st.markdown(
            "<div class=\"abel-note\">🛡️ &nbsp; <strong>Límite del asistente:</strong> "
            "responde por recuperación del catálogo (25 FAQs). No genera respuestas nuevas. "
            "Las consultas se guardan localmente (SQLite) solo con fines de métricas: "
            "evita escribir datos personales o sensibles.</div>",
            unsafe_allow_html=True,
        )

    with tab_reportar:
        st.subheader("Registrar una incidencia")
        st.markdown(
            "Describe el problema con la mayor precisión posible. Recibirás un "
            "número de ticket para dar seguimiento. **Demo con datos ficticios:** "
            "el ticket se guarda en una base local sin control de acceso; no "
            "incluyas datos personales ni sensibles en la descripción."
        )
        with st.form("form_incidencia", clear_on_submit=True):
            col1, col2 = st.columns(2)
            categoria = col1.selectbox("Categoría", CATEGORIAS_INCIDENCIA)
            edificio = col2.selectbox(
                "Edificio",
                ["Edificio Central", "Edificio de Ciencias", "Pabellón de Servicios", "Exteriores"],
            )
            descripcion = st.text_area("Descripción del problema", max_chars=500)
            prioridad = st.selectbox("Prioridad", ["baja", "media", "alta"])
            enviado = st.form_submit_button("Enviar reporte")

        if enviado:
            if len(descripcion.strip()) < 10:
                st.error("Agrega una descripción de al menos 10 caracteres.")
            else:
                ticket = crear_incidencia(categoria, edificio, descripcion.strip(), prioridad)
                st.success(f"Incidencia registrada. Tu número de ticket es **{ticket}**.")
                st.info(
                    "El personal de bedelía atiende los reportes en horario de "
                    "oficina. Consulta el estado en la pestaña *Consultar estado*."
                )

    with tab_estado:
        st.subheader("Consultar estado de una incidencia")
        ticket = st.number_input("Número de ticket", min_value=1, step=1)
        if st.button("Buscar"):
            inc = consultar_incidencia(int(ticket))
            if inc is None:
                st.warning("No existe ninguna incidencia con ese número de ticket.")
            else:
                st.markdown(
                    f"**Ticket {inc['id']}** · estado: `{inc['estado']}` · prioridad: `{inc['prioridad']}`"
                )
                st.markdown(f"Categoría: {inc['categoria']} · Edificio: {inc['edificio']}")
                st.markdown(f"Descripción: {inc['descripcion']}")
                st.caption(f"Registrada: {inc['creado']}")
                if inc["estado"] == "resuelta":
                    st.balloons()

    with tab_panel:
        st.subheader("Panel de métricas operativas")
        st.caption(
            "Datos generados por el uso de esta demo (consultas al chat e "
            "incidencias registradas en la base de datos local)."
        )
        m = resumen_metricas()
        col1, col2, col3 = st.columns(3)
        col1.metric("Consultas al asistente", m["consultas"])
        col2.metric("Respondidas por el catálogo", m["respondidas"])
        col3.metric("Incidencias registradas", m["incidencias"])

        if m["consultas"]:
            cobertura = 100 * m["respondidas"] / m["consultas"]
            st.progress(min(cobertura / 100, 1.0), text=f"Cobertura automática: {cobertura:.0f}%")

        incidencias = listar_incidencias()
        if incidencias:
            st.markdown("**Últimas incidencias**")
            st.dataframe(
                pd.DataFrame(incidencias)[
                    ["id", "creado", "categoria", "edificio", "prioridad", "estado"]
                ],
                use_container_width=True,
            )
        else:
            st.info("Aún no hay incidencias registradas. Reporta una para ver la trazabilidad.")


if __name__ == "__main__":
    main()
