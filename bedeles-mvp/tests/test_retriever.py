"""Pruebas unitarias del motor FAQ; no requieren ejecutar Streamlit."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.retriever import FAQRetriever  # noqa: E402


retriever = FAQRetriever(ROOT / "data" / "faq.csv")


def test_pregunta_exacta():
    r = retriever.responder("¿Dónde queda el aula 302?")
    assert not r.abstiene and r.faq_id == 1


def test_parafrasis_con_alias():
    r = retriever.responder("¿Dónde quedan los laboratorios de informática?")
    assert not r.abstiene and r.faq_id == 2


def test_fuera_de_alcance():
    r = retriever.responder("¿Cuál es el sentido de la vida?")
    assert r.abstiene


def test_entrada_vacia():
    r = retriever.responder("   ")
    assert r.abstiene and r.faq_id is None


def test_solicitud_de_contrasena_se_abstiene():
    r = retriever.responder("¿Cómo cambio mi contraseña del correo institucional?")
    assert r.abstiene and r.faq_id is None


def test_umbral_invalido():
    try:
        FAQRetriever(ROOT / "data" / "faq.csv", umbral=1.5)
    except ValueError:
        return
    raise AssertionError("Debió rechazar un umbral fuera de rango")


if __name__ == "__main__":
    test_pregunta_exacta()
    test_parafrasis_con_alias()
    test_fuera_de_alcance()
    test_entrada_vacia()
    test_solicitud_de_contrasena_se_abstiene()
    test_umbral_invalido()
    print("Todas las pruebas del retriever pasaron.")
