"""Gráfico de métricas por subgrupo para el informe de evaluación."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SALIDA = Path(__file__).resolve().parent.parent / "assets"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Por categoría
categorias = ["Horarios", "Avisos", "Aulas", "Trámites", "Servicios", "Fuera de\nalcance*"]
acierto = [90.9, 75.0, 66.7, 60.0, 33.3, 58.3]
colores = ["#4a6fa5" if c != "Servicios" else "#c0504d" for c in categorias]
barras = ax1.bar(categorias, acierto, color=colores, width=0.62)
ax1.set_title("Acierto por categoría de consulta (%)", fontsize=11, pad=12)
ax1.set_ylim(0, 100)
ax1.axhline(64.2, color="#888", ls="--", lw=1)
ax1.text(5.4, 66, "global: 64.2%", fontsize=8, color="#888", ha="right")
for b, v in zip(barras, acierto):
    ax1.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.1f}", ha="center", fontsize=8)
ax1.spines[["top", "right"]].set_visible(False)
ax1.tick_params(axis="x", labelsize=8)

# Por tipo de pregunta (solo en alcance)
registros = ["Casi idénticas\n(con errores)", "Paráfrasis\nformal", "Paráfrasis\ncoloquial"]
valores = [100, 66.7, 54.5]
barras2 = ax2.bar(registros, valores, color=["#4a6fa5", "#7a9cc6", "#c0504d"], width=0.5)
ax2.set_title("Acierto por tipo de pregunta, solo en alcance (%)", fontsize=11, pad=12)
ax2.set_ylim(0, 118)
for b, v in zip(barras2, valores):
    ax2.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.1f}", ha="center", fontsize=8)
ax2.spines[["top", "right"]].set_visible(False)
ax2.tick_params(axis="x", labelsize=8)

fig.text(0.02, -0.02, "* Fuera de alcance: se muestra la tasa de abstención correcta (el criterio de éxito cambia).\nEl grupo «casi idénticas» no es comparable en dificultad con las paráfrasis.",
         fontsize=8, color="#666")
fig.tight_layout()
fig.savefig(SALIDA / "metricas_subgrupos.png", dpi=150, bbox_inches="tight")
print("Gráfico generado")
