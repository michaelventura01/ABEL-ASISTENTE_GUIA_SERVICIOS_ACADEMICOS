"""Motor de recuperación de preguntas frecuentes (TF-IDF + similitud coseno).

El MVP de Bedeles funciona por recuperación, no por generación: dado el
mensaje del usuario, busca la FAQ más parecida del catálogo. Si la similitud
no supera el umbral, el asistente se abstiene y ofrece derivar el caso a
una persona o registrar una incidencia.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DEFAULT_THRESHOLD = 0.45


def normalizar(texto: str) -> str:
    """Lleva el texto a minúsculas, sin tildes ni signos de puntuación."""
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9ñ\s]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


@dataclass
class RespuestaFAQ:
    """Resultado de una consulta al catálogo de FAQs."""

    pregunta: str
    faq_id: int | None
    categoria: str | None
    respuesta: str | None
    similitud: float
    abstiene: bool


class FAQRetriever:
    def __init__(self, ruta_faq: str | Path, umbral: float = DEFAULT_THRESHOLD):
        self.umbral = umbral
        self.faq = pd.read_csv(ruta_faq)
        self.vectorizador = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 3))
        self.matriz = self.vectorizador.fit_transform(
            self.faq["pregunta"].map(normalizar).tolist()
        )

    def responder(self, pregunta: str) -> RespuestaFAQ:
        if not normalizar(pregunta):
            return RespuestaFAQ(pregunta, None, None, None, 0.0, True)

        vec = self.vectorizador.transform([normalizar(pregunta)])
        sims = cosine_similarity(vec, self.matriz)[0]
        mejor = int(sims.argmax())

        if sims[mejor] < self.umbral:
            return RespuestaFAQ(pregunta, None, None, None, float(sims[mejor]), True)

        fila = self.faq.iloc[mejor]
        return RespuestaFAQ(
            pregunta=pregunta,
            faq_id=int(fila["id"]),
            categoria=str(fila["categoria"]),
            respuesta=str(fila["respuesta"]),
            similitud=float(sims[mejor]),
            abstiene=False,
        )

    def categorias(self) -> list[str]:
        return sorted(self.faq["categoria"].unique())
