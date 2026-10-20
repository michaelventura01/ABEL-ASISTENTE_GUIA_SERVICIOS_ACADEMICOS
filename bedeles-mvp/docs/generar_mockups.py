"""Genera los wireframes del diseño conceptual (pantallas del MVP)."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

SALIDA = Path(__file__).resolve().parent.parent / "assets"
SALIDA.mkdir(exist_ok=True)

GRIS_CLARO = "#e8e8e8"
GRIS_MEDIO = "#c9c9c9"
GRIS_TEXTO = "#333333"
AZUL = "#4a6fa5"


def caja(ax, x, y, w, h, texto="", fc=GRIS_CLARO, ec="#888888", fs=9, bold=False, ha="center"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                                fc=fc, ec=ec, lw=1.2))
    if texto:
        tx = x + w / 2 if ha == "center" else x + 0.015
        ax.text(tx, y + h / 2, texto, ha=ha, va="center", fontsize=fs,
                color=GRIS_TEXTO, fontweight="bold" if bold else "normal", wrap=True)


def base_ventana(titulo, num):
    fig, ax = plt.subplots(figsize=(8, 5.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")
    # barra del navegador
    caja(ax, 0.3, 6.3, 9.4, 0.55, "", fc="#f4f4f4")
    ax.text(0.5, 6.57, "● ● ●", fontsize=8, color="#999")
    ax.text(1.1, 6.57, "localhost:8501", fontsize=8, color="#888")
    # encabezado
    caja(ax, 0.3, 5.55, 9.4, 0.6, "Bedeles · Asistencia Universitaria Inteligente",
         fc=AZUL, ec=AZUL, fs=11, bold=True)
    return fig, ax


# ── Pantalla 1: Asistente (chat) ──────────────────────────────
fig, ax = base_ventana("Asistente de consultas", 1)
for x, w, t in [(0, 3.2, "Ejemplos rápidos\n(¿Dónde queda el aula 302?)"),
                (3.5, 3.2, "¿A qué hora abre\nla biblioteca?"),
                (7.0, 2.7, "¿Cómo retiro\nuna asignatura?")]:
    caja(ax, x, 4.75, w, 0.5, t, fs=7.5)
caja(ax, 0.3, 3.85, 5.5, 0.55, "¿Dónde queda el aula 302?", fc="#d6e4f0", fs=9, ha="left")
caja(ax, 4.2, 3.0, 5.5, 0.75, "El aula 302 está en el Edificio\nCentral, tercer piso.", fs=8.5)
caja(ax, 0.3, 1.95, 5.5, 0.55, "¿Cómo solicito una beca?", fc="#d6e4f0", fs=9, ha="left")
caja(ax, 2.9, 0.85, 6.8, 0.9, "No tengo esa información en mi catálogo.\nPuedes reportarla como incidencia o visitar la bedelía.", fs=8.5)
caja(ax, 0.3, 0.15, 9.4, 0.5, "Escribe tu consulta…", fc="#f7f7f7", fs=9, ha="left")
fig.savefig(SALIDA / "mockup_1_asistente.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ── Pantalla 2: Reportar incidencia ────────────────────────────
fig, ax = base_ventana("Reportar incidencia", 2)
caja(ax, 0.3, 4.6, 4.5, 0.55, "Categoría  ▾", fs=9)
caja(ax, 5.2, 4.6, 4.5, 0.55, "Edificio  ▾", fs=9)
caja(ax, 0.3, 2.9, 9.4, 1.4, "Descripción del problema\n\n\n", fs=9, ha="left")
caja(ax, 0.3, 2.0, 4.5, 0.55, "Prioridad  ▾", fs=9)
caja(ax, 0.3, 1.0, 2.2, 0.5, "Enviar reporte", fc=AZUL, ec=AZUL, fs=9, bold=True)
caja(ax, 3.0, 0.35, 6.7, 0.5, "✓ Incidencia registrada. Tu ticket es #17", fc="#d9f0d9", fs=8.5)
fig.savefig(SALIDA / "mockup_2_incidencia.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ── Pantalla 3: Consultar estado ───────────────────────────────
fig, ax = base_ventana("Consultar estado", 3)
caja(ax, 0.3, 4.6, 3.0, 0.55, "Número de ticket:  17", fs=9)
caja(ax, 3.6, 4.6, 1.6, 0.55, "Buscar", fc=AZUL, ec=AZUL, fs=9, bold=True)
caja(ax, 0.3, 2.8, 9.4, 1.5, "Ticket 17 · estado: en proceso · prioridad: media\nCategoría: Tecnología · Edificio: Ciencias\nDescripción: Proyector del aula 204 no enciende", fs=8.5)
ax.text(0.3, 2.35, "Historial de estados: recibida → en proceso → resuelta", fontsize=8, color="#777")
fig.savefig(SALIDA / "mockup_3_estado.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ── Pantalla 4: Panel de métricas ──────────────────────────────
fig, ax = base_ventana("Panel de métricas", 4)
for i, (t, v) in enumerate([("Consultas", "128"), ("Respondidas", "95"), ("Incidencias", "23")]):
    caja(ax, 0.3 + i * 3.15, 4.4, 2.9, 0.9, f"{t}\n{v}", fs=9, bold=False)
caja(ax, 0.3, 3.1, 9.4, 0.55, "Cobertura automática: 74%  ▓▓▓▓▓▓▓▓░░", fs=9, ha="left")
caja(ax, 0.3, 0.7, 9.4, 2.1, "Tabla de últimas incidencias\n(id · fecha · categoría · edificio · prioridad · estado)", fs=8.5)
fig.savefig(SALIDA / "mockup_4_panel.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print("Wireframes generados en", SALIDA)
