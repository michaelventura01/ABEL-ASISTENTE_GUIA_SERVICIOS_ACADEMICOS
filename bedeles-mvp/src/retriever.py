"""Motor de recuperación FAQ con alias editoriales y abstención conservadora.

No genera texto: devuelve la respuesta de una FAQ del catálogo. Las preguntas
alternativas se mantienen en data/faq_aliases.csv para cubrir sinónimos y
variantes habituales del español dominicano.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Más conservador que el umbral inicial 0.45: reduce respuestas incorrectas.
DEFAULT_THRESHOLD = 0.60

# Peticiones de credenciales no deben resolverse con una FAQ no relacionada.
# El MVP no gestiona restablecimiento de contraseñas ni revela claves.
PATRONES_CREDENCIALES = (
    r"\bcontrasena\b", r"\bpassword\b", r"\bclave del wifi\b",
    r"\bclave de wifi\b", r"\bhackear\b.*\bwifi\b",
)


def normalizar(texto: str) -> str:
    """Normaliza mayúsculas, tildes, puntuación y espacios."""
    texto = str(texto or "").lower().strip()
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
    def __init__(self, ruta_faq: str | Path, umbral: float = DEFAULT_THRESHOLD,
                 ruta_aliases: str | Path | None = None):
        if not 0.0 <= umbral <= 1.0:
            raise ValueError("El umbral debe estar entre 0 y 1.")
        self.umbral = float(umbral)
        self.ruta_faq = Path(ruta_faq)
        if not self.ruta_faq.is_file():
            raise FileNotFoundError(f"No existe el catálogo FAQ: {self.ruta_faq}")
        self.faq = pd.read_csv(self.ruta_faq).fillna("")
        requeridas = {"id", "categoria", "pregunta", "respuesta"}
        faltantes = requeridas.difference(self.faq.columns)
        if faltantes:
            raise ValueError(f"Faltan columnas en faq.csv: {', '.join(sorted(faltantes))}")
        if self.faq.empty:
            raise ValueError("El catálogo FAQ está vacío.")
        self.faq["id"] = pd.to_numeric(self.faq["id"], errors="raise").astype(int)

        aliases_path = Path(ruta_aliases) if ruta_aliases else self.ruta_faq.with_name("faq_aliases.csv")
        alias_rows: list[tuple[int, str]] = []
        if aliases_path.is_file():
            aliases_df = pd.read_csv(aliases_path).fillna("")
            if not {"faq_id", "alias"}.issubset(aliases_df.columns):
                raise ValueError("faq_aliases.csv debe tener las columnas faq_id,alias")
            valid_ids = set(self.faq["id"].tolist())
            for row in aliases_df.itertuples(index=False):
                faq_id = int(row.faq_id)
                alias = normalizar(row.alias)
                if faq_id not in valid_ids:
                    raise ValueError(f"El alias apunta a una FAQ inexistente: {faq_id}")
                if alias:
                    alias_rows.append((faq_id, alias))

        self._faq_por_id = {int(row.id): row for row in self.faq.itertuples(index=False)}
        self._frases: list[str] = []
        self._frase_faq_ids: list[int] = []
        for row in self.faq.itertuples(index=False):
            faq_id = int(row.id)
            frase = normalizar(row.pregunta)
            if frase:
                self._frases.append(frase)
                self._frase_faq_ids.append(faq_id)
        for faq_id, alias in alias_rows:
            self._frases.append(alias)
            self._frase_faq_ids.append(faq_id)

        self.vectorizador = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 3))
        self.matriz = self.vectorizador.fit_transform(self._frases)
        self._indices_por_faq = {
            faq_id: [i for i, valor in enumerate(self._frase_faq_ids) if valor == faq_id]
            for faq_id in self._faq_por_id
        }

    def responder(self, pregunta: str) -> RespuestaFAQ:
        consulta = normalizar(pregunta)
        if not consulta:
            return RespuestaFAQ(str(pregunta or ""), None, None, None, 0.0, True)
        if any(re.search(patron, consulta) for patron in PATRONES_CREDENCIALES):
            # No se registra una respuesta aproximada para una solicitud sensible.
            return RespuestaFAQ(str(pregunta), None, None, None, 0.0, True)

        vec = self.vectorizador.transform([consulta])
        similitudes_frases = cosine_similarity(vec, self.matriz)[0]
        # Una FAQ puede tener varias formulaciones; se queda con la mejor.
        puntuaciones = {
            faq_id: float(similitudes_frases[indices].max())
            for faq_id, indices in self._indices_por_faq.items()
        }
        mejor_id = max(puntuaciones, key=puntuaciones.get)
        mejor_similitud = puntuaciones[mejor_id]
        if mejor_similitud < self.umbral:
            return RespuestaFAQ(str(pregunta), None, None, None, mejor_similitud, True)

        fila = self._faq_por_id[mejor_id]
        return RespuestaFAQ(
            pregunta=str(pregunta), faq_id=mejor_id, categoria=str(fila.categoria),
            respuesta=str(fila.respuesta), similitud=mejor_similitud, abstiene=False,
        )

    def categorias(self) -> list[str]:
        return sorted(self.faq["categoria"].astype(str).unique())
