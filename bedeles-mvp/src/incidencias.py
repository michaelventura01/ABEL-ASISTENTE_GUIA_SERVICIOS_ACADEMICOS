"""Gestión de incidencias y registro de consultas en SQLite."""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from pathlib import Path

# Ruta de la base de datos: por defecto data/bedeles.db; se puede sobrescribir
# con la variable de entorno BEDELES_DB (útil para las pruebas automatizadas).
DB_PATH = Path(os.environ.get("BEDELES_DB",
                              Path(__file__).resolve().parent.parent / "data" / "bedeles.db"))

CATEGORIAS_INCIDENCIA = [
    "Aula o laboratorio",
    "Mobiliario y limpieza",
    "Electricidad o aire acondicionado",
    "Tecnología (wifi, computadoras)",
    "Baños o fontanería",
    "Otro",
]

ESTADOS_INCIDENCIA = ["recibida", "en proceso", "resuelta"]


def conexion() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def inicializar_db() -> None:
    with conexion() as con:
        con.executescript(
            """
            CREATE TABLE IF NOT EXISTS incidencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creado TEXT NOT NULL,
                categoria TEXT NOT NULL,
                edificio TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                prioridad TEXT NOT NULL DEFAULT 'media',
                estado TEXT NOT NULL DEFAULT 'recibida'
            );
            CREATE TABLE IF NOT EXISTS consultas_chat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creado TEXT NOT NULL,
                pregunta TEXT NOT NULL,
                faq_id INTEGER,
                categoria TEXT,
                similitud REAL,
                abstiene INTEGER NOT NULL
            );
            """
        )


def crear_incidencia(categoria: str, edificio: str, descripcion: str, prioridad: str = "media") -> int:
    inicializar_db()
    with conexion() as con:
        cur = con.execute(
            "INSERT INTO incidencias (creado, categoria, edificio, descripcion, prioridad) "
            "VALUES (?, ?, ?, ?, ?)",
            (datetime.now().isoformat(timespec="seconds"), categoria, edificio, descripcion, prioridad),
        )
        return int(cur.lastrowid)


def consultar_incidencia(ticket: int) -> dict | None:
    inicializar_db()
    with conexion() as con:
        fila = con.execute(
            "SELECT * FROM incidencias WHERE id = ?", (ticket,)
        ).fetchone()
        return dict(fila) if fila else None


def listar_incidencias() -> list[dict]:
    inicializar_db()
    with conexion() as con:
        filas = con.execute(
            "SELECT * FROM incidencias ORDER BY id DESC LIMIT 200"
        ).fetchall()
        return [dict(f) for f in filas]


def registrar_consulta(pregunta: str, resultado) -> None:
    """Guarda cada consulta del chat para el panel de métricas."""
    inicializar_db()
    with conexion() as con:
        con.execute(
            "INSERT INTO consultas_chat (creado, pregunta, faq_id, categoria, similitud, abstiene) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                datetime.now().isoformat(timespec="seconds"),
                pregunta,
                resultado.faq_id,
                resultado.categoria,
                resultado.similitud,
                int(resultado.abstiene),
            ),
        )


def resumen_metricas() -> dict:
    inicializar_db()
    with conexion() as con:
        total = con.execute("SELECT COUNT(*) c FROM consultas_chat").fetchone()["c"]
        respondidas = con.execute(
            "SELECT COUNT(*) c FROM consultas_chat WHERE abstiene = 0"
        ).fetchone()["c"]
        incidencias = con.execute("SELECT COUNT(*) c FROM incidencias").fetchone()["c"]
        resueltas = con.execute(
            "SELECT COUNT(*) c FROM incidencias WHERE estado = 'resuelta'"
        ).fetchone()["c"]
        return {
            "consultas": total,
            "respondidas": respondidas,
            "abstenciones": total - respondidas,
            "incidencias": incidencias,
            "incidencias_resueltas": resueltas,
        }
