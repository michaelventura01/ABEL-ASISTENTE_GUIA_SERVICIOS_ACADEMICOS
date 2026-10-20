"""Pruebas funcionales de la demo con streamlit.testing.

Uso: python tests/test_app.py

Las pruebas usan una base de datos temporal (BEDELES_DB) para no tocar la
base de la demo (data/bedeles.db).
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

# Base temporal para todas las pruebas: debe configurarse antes de importar la app
os.environ["BEDELES_DB"] = str(Path(tempfile.mkdtemp()) / "bedeles_pruebas.db")

from streamlit.testing.v1 import AppTest  # noqa: E402

APP = str(RAIZ / "app.py")

# La base temporal se comparte entre sesiones del mismo proceso;
# las pruebas que verifican métricas del panel la reinician antes.
import src.incidencias as _inc  # noqa: E402


def nueva_sesion(reiniciar: bool = False) -> AppTest:
    """Abre la app sin tocar la base de la demo."""
    if reiniciar and _inc.DB_PATH.exists():
        _inc.DB_PATH.unlink()
    at = AppTest.from_file(APP, default_timeout=30)
    at.run()
    assert not at.exception, f"la app falló al arrancar: {at.exception}"
    return at


def valor_metrica(at: AppTest, etiqueta: str) -> str:
    for m in at.metric:
        if str(m.label).strip() == etiqueta:
            return str(m.value)
    raise AssertionError(f"no se encontró la métrica {etiqueta}")


def probar_chat_cubierto() -> None:
    at = nueva_sesion()
    at.chat_input[0].set_value("¿Dónde queda el aula 302?")
    at.run()
    assert not at.exception
    mensajes = at.session_state["mensajes"]
    assert mensajes[-2]["rol"] == "user"
    respuesta = mensajes[-1]["contenido"]
    assert "Edificio Central" in respuesta, f"respuesta inesperada: {respuesta}"
    print("OK  chat con pregunta cubierta")


def probar_chat_abstencion() -> None:
    at = nueva_sesion()
    # pregunta claramente fuera de alcance (no universitaria): debe abstenerse
    at.chat_input[0].set_value("¿Cuál es el sentido de la vida?")
    at.run()
    assert not at.exception
    respuesta = at.session_state["mensajes"][-1]["contenido"]
    assert "No tengo esa información" in respuesta, f"debía abstenerse: {respuesta}"
    print("OK  chat con pregunta fuera de alcance (abstención)")


def probar_ejemplo_rapido() -> None:
    at = nueva_sesion(reiniciar=True)
    # sin elegir nada, no debe registrarse ninguna consulta (sin autoenvío)
    assert valor_metrica(at, "Consultas al asistente") == "0", \
        "abrir la sesión no debe enviar ni registrar consultas"
    at.selectbox[0].set_value("¿A qué hora abre la biblioteca?")
    at.run()
    assert not at.exception
    mensajes = at.session_state["mensajes"]
    assert mensajes and mensajes[-1]["rol"] == "assistant", "el ejemplo no generó respuesta"
    assert "biblioteca" in mensajes[-1]["contenido"].lower()
    print("OK  ejemplo rápido conectado al chat (y sin autoenvío al abrir)")


def probar_panel_registra_uso() -> None:
    at = nueva_sesion(reiniciar=True)
    assert valor_metrica(at, "Consultas al asistente") == "0"
    at.chat_input[0].set_value("¿A qué hora abre la biblioteca?")
    at.run()
    assert not at.exception
    assert valor_metrica(at, "Consultas al asistente") == "1", \
        "el panel no registró la consulta enviada"
    assert valor_metrica(at, "Respondidas por el catálogo") == "1"
    print("OK  panel registra el uso real (0 al abrir, 1 tras una pregunta)")


def probar_formulario_invalido() -> None:
    at = nueva_sesion()
    at.run()
    # completar el formulario (descripción demasiado corta)
    at.text_area[0].set_value("corto")
    at.button[0].click()
    at.run()
    assert not at.exception
    assert any("al menos 10 caracteres" in str(e.value) for e in at.error), \
        "debía rechazar la descripción corta"
    print("OK  formulario rechaza descripción inválida")


def probar_ticket() -> None:
    at = nueva_sesion()
    at.run()
    at.text_area[0].set_value("Proyector del aula 204 no enciende")
    at.button[0].click()
    at.run()
    assert not at.exception
    exitos = [str(e.value) for e in at.success]
    assert exitos and "ticket" in exitos[0].lower(), f"no creó el ticket: {exitos}"
    print("OK  creación de ticket")

    # consultar el ticket 1
    at2 = nueva_sesion()
    at2.number_input[0].set_value(1)
    # el botón Buscar es el segundo button (el primero es el submit del formulario)
    at2.button[1].click()
    at2.run()
    assert not at2.exception
    cuerpo = " ".join(str(m.value) for m in at2.markdown)
    assert "Proyector del aula 204" in cuerpo, "no encontró el ticket 1"
    print("OK  consulta de ticket existente")

    # ticket inexistente
    at3 = nueva_sesion()
    at3.number_input[0].set_value(999)
    at3.button[1].click()
    at3.run()
    assert not at3.exception
    assert any("No existe" in str(w.value) for w in at3.warning), "debía avisar que no existe"
    print("OK  consulta de ticket inexistente")


if __name__ == "__main__":
    probar_chat_cubierto()
    probar_chat_abstencion()
    probar_ejemplo_rapido()
    probar_panel_registra_uso()
    probar_formulario_invalido()
    probar_ticket()
    print("\nTodas las pruebas pasaron.")
