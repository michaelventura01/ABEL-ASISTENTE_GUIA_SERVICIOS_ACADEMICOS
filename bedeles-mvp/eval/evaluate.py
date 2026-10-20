"""Evaluación del asistente con métricas desglosadas por subgrupo.

Uso: python eval/evaluate.py [--umbral 0.45]

Lee data/test_set.csv (columna `conjunto`: dev para ajustar el umbral,
test para reportar) y produce:
  - eval/resultados_test.csv   (predicción por pregunta)
  - eval/metricas.json         (métricas globales y por subgrupo)

Criterios:
  - Acierto: el FAQ recuperado coincide con el esperado.
  - Abstención correcta: pregunta fuera de alcance y el asistente se abstiene.
  - Error: responde con un FAQ distinto, o responde cuando debía abstenerse,
    o se abstiene cuando tenía cobertura.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from src.retriever import FAQRetriever  # noqa: E402


def clasificar(fila: pd.Series, resultado) -> str:
    if fila["faq_id_esperado"] == "fuera_alcance":
        if resultado.abstiene:
            return "abstencion_correcta"
        return "error_falso_positivo"
    if resultado.abstiene:
        return "error_omision"
    if str(resultado.faq_id) == str(fila["faq_id_esperado"]):
        return "acierto"
    return "error_respuesta_incorrecta"


def tabla_por_grupo(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    filas = []
    for grupo, sub in df.groupby(columna):
        n = len(sub)
        aciertos = (sub["resultado"] == "acierto").sum()
        abst_ok = (sub["resultado"] == "abstencion_correcta").sum()
        filas.append(
            {
                columna: grupo,
                "n": n,
                "acierto": aciertos,
                "abstencion_correcta": abst_ok,
                "correcto_total": aciertos + abst_ok,
                "tasa_acierto": round(aciertos / n, 3) if n else None,
                "tasa_correcta_global": round((aciertos + abst_ok) / n, 3) if n else None,
            }
        )
    return pd.DataFrame(filas)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--umbral", type=float, default=0.45)
    parser.add_argument("--conjunto", choices=["dev", "test", "todo"], default="test")
    args = parser.parse_args()

    test = pd.read_csv(RAIZ / "data" / "test_set.csv")
    if args.conjunto != "todo":
        test = test[test["conjunto"] == args.conjunto].copy()

    retriever = FAQRetriever(RAIZ / "data" / "faq.csv", umbral=args.umbral)
    resultados = [retriever.responder(p) for p in test["pregunta"]]
    test["faq_predicha"] = [r.faq_id for r in resultados]
    test["similitud"] = [round(r.similitud, 3) for r in resultados]
    test["abstiene"] = [r.abstiene for r in resultados]
    test["resultado"] = [
        clasificar(fila, r) for (_, fila), r in zip(test.iterrows(), resultados)
    ]

    en_alcance = test[test["faq_id_esperado"] != "fuera_alcance"]
    fuera = test[test["faq_id_esperado"] == "fuera_alcance"]

    metricas = {
        "umbral": args.umbral,
        "conjunto": args.conjunto,
        "n_total": len(test),
        "cobertura_evaluada": len(en_alcance),
        "fuera_de_alcance": len(fuera),
        "tasa_acierto_en_alcance": round(
            (en_alcance["resultado"] == "acierto").mean(), 3
        ),
        "tasa_respuesta_automatica_en_alcance": round(
            (en_alcance["resultado"] != "error_omision").mean(), 3
        ),
        "tasa_respuesta_automatica_total": round(
            (test["resultado"] != "error_omision").mean(), 3
        ),
        "tasa_omision_en_alcance": round(
            (en_alcance["resultado"] == "error_omision").mean(), 3
        ),
        "tasa_respuesta_incorrecta_en_alcance": round(
            (en_alcance["resultado"] == "error_respuesta_incorrecta").mean(), 3
        ),
        "tasa_abstencion_correcta_fuera_alcance": round(
            (fuera["resultado"] == "abstencion_correcta").mean(), 3
        ) if len(fuera) else None,
        "tasa_falso_positivo_fuera_alcance": round(
            (fuera["resultado"] == "error_falso_positivo").mean(), 3
        ) if len(fuera) else None,
        # Desglose por registro sobre TODO el conjunto (incluye fuera de alcance:
        # los denominadores mezclan poblaciones; ver informe antes de comparar).
        "por_registro": tabla_por_grupo(test, "registro").to_dict("records"),
        # Desglose por registro SOLO en preguntas dentro del alcance (comparable
        # con el informe: formal 8/12, coloquial 18/33, errores 8/8).
        "por_registro_en_alcance": tabla_por_grupo(
            en_alcance, "registro"
        ).to_dict("records"),
        "por_categoria": tabla_por_grupo(test, "categoria_esperada").to_dict("records"),
    }

    salida_csv = RAIZ / "eval" / f"resultados_{args.conjunto}.csv"
    test.to_csv(salida_csv, index=False)
    salida_json = RAIZ / "eval" / f"metricas_{args.conjunto}.json"
    salida_json.write_text(json.dumps(metricas, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(metricas, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
