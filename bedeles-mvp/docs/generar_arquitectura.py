"""Genera el diagrama de arquitectura del diseño de solución."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

SALIDA = Path(__file__).resolve().parent.parent / "assets"
SALIDA.mkdir(exist_ok=True)

AZUL = "#4a6fa5"
GRIS = "#e8e8e8"
VERDE = "#d9f0d9"
NARANJA = "#fde8d0"

fig, ax = plt.subplots(figsize=(10, 6.2))
ax.set_xlim(0, 12.4)
ax.set_ylim(0, 8)
ax.axis("off")


def nodo(x, y, w, h, titulo, detalle="", color=GRIS, texto_oscuro=True):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06",
                                fc=color, ec="#666", lw=1.2))
    c1 = "#222" if texto_oscuro else "white"
    c2 = "#444" if texto_oscuro else "#e8e8e8"
    ax.text(x + w / 2, y + h - 0.38, titulo, ha="center", va="center",
            fontsize=10, fontweight="bold", color=c1)
    if detalle:
        ax.text(x + w / 2, y + (h - 0.38) / 2, detalle, ha="center", va="center",
                fontsize=8, color=c2)


def flecha(x1, y1, x2, y2, etiqueta="", estilo="-", dx=0, dy=0.25):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=14, color="#555", lw=1.4,
                                 linestyle=estilo))
    if etiqueta:
        ax.text((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy, etiqueta, ha="center",
                fontsize=8, color="#555")


# Fila superior: flujo del chat
nodo(0.3, 5.5, 2.2, 1.5, "Usuario", "estudiante /\npersonal", color=VERDE)
nodo(3.4, 5.5, 2.4, 1.5, "Interfaz", "Streamlit\n(app.py)", color=AZUL, texto_oscuro=False)
nodo(6.8, 5.4, 2.9, 1.6, "Motor de recuperación", "TF-IDF + coseno\numbral 0.45")
nodo(10.1, 5.7, 1.9, 1.0, "Catálogo FAQ", "data/faq.csv\n(25 FAQs)")

# Fila media: datos
nodo(3.4, 3.2, 2.4, 1.4, "Incidencias", "SQLite\ntickets y estados", color=NARANJA)
nodo(6.8, 3.2, 2.9, 1.4, "Registro de consultas", "SQLite\nconsultas_chat", color=NARANJA)

# Fila inferior: salidas
nodo(4.6, 0.9, 2.6, 1.4, "Panel de métricas", "cobertura y\ntrazabilidad")
nodo(10.1, 0.9, 1.9, 1.4, "Evaluación", "eval/evaluate.py\n90 preguntas")

# Flechas del flujo del chat
flecha(2.5, 6.25, 3.4, 6.25)
flecha(5.8, 6.15, 6.8, 6.15)
flecha(9.7, 6.2, 10.1, 6.2)

# Interfaz -> incidencias
flecha(4.6, 5.5, 4.6, 4.6, "reporta", dx=0.55, dy=0)

# Motor -> registro de consultas
flecha(8.1, 5.4, 8.1, 4.6, "log", dx=0.4, dy=0)

# Bases de datos -> panel
flecha(4.6, 3.2, 5.4, 2.3)
flecha(8.2, 3.2, 6.6, 2.3)

# Evaluación (mide al motor)
flecha(9.7, 5.7, 10.7, 2.35, estilo="--")

ax.text(0.3, 7.65, "Arquitectura del MVP Bedeles (todo open source, sin servicios pagos)",
        fontsize=11, fontweight="bold", color="#333")
ax.text(10.15, 4.2, "mide el motor", fontsize=8, color="#555", ha="left")

fig.savefig(SALIDA / "arquitectura.png", dpi=150, bbox_inches="tight")
print("Diagrama generado")
