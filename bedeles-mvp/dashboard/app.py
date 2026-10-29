import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="ABEL | KPIs y Monte Carlo",
    page_icon="🎓",
    layout="wide",
)

# Paleta y contraste accesible para el dashboard.
st.markdown(
    """
    <style>
    :root {
        --abel-navy: #123B82;
        --abel-blue: #2378F7;
        --abel-sky: #54B8FF;
        --abel-bg: #F3F8FF;
        --abel-text: #183568;
        --abel-muted: #425466;
        --abel-border: #D5E5FF;
    }

    .stApp {
        background: var(--abel-bg);
        color: var(--abel-text);
    }

    .block-container {
        max-width: 1200px;
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
    }

    /* Texto general: evita que herede colores casi blancos del tema. */
    .stApp, .stApp p, .stApp label, .stApp li,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: var(--abel-text);
    }

    h1, h2, h3, h4 {
        color: var(--abel-navy) !important;
    }

    .hero {
        background: linear-gradient(115deg, #123B82, #2378F7, #54B8FF);
        padding: 1.5rem 2rem;
        border-radius: 18px;
        color: #FFFFFF;
        margin-bottom: 0.5rem;
    }

    .hero h1, .hero p {
        color: #FFFFFF !important;
    }

    .hero h1 {
        margin: 0 0 0.65rem 0;
        line-height: 1.2;
    }

    .hero p {
        margin: 0;
    }

    /* Métricas estándar de Streamlit. */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid var(--abel-border);
        border-radius: 14px;
        padding: 16px 14px;
        min-height: 105px;
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] p,
    div[data-testid="stMetricLabel"] label {
        color: #425466 !important;
        opacity: 1 !important;
    }

    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] div,
    div[data-testid="stMetricValue"] p {
        color: #123B82 !important;
        opacity: 1 !important;
    }

    div[data-testid="stMetricDelta"],
    div[data-testid="stMetricDelta"] div {
        opacity: 1 !important;
    }

    /* Advertencia con texto oscuro legible. */
    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] div {
        color: #664D03 !important;
        opacity: 1 !important;
    }

    /* Sidebar, tablas y controles. */
    section[data-testid="stSidebar"] {
        background: #EAF3FF;
    }

    section[data-testid="stSidebar"] * {
        color: #183568;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--abel-border);
        border-radius: 10px;
    }

    .stCaption, [data-testid="stCaptionContainer"] {
        color: #526B8F !important;
    }

    hr {
        border-color: #D5E5FF;
    }
    </style>
    <div class="hero">
      <h1>🎓 ABEL · Asistencia Universitaria Inteligente</h1>
      <p>Dashboard ejecutivo · KPIs, escenarios probabilísticos y sensibilidad</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.warning(
    "Los valores iniciales son supuestos ilustrativos editables, "
    "no resultados medidos ni promesas de ahorro."
)

with st.sidebar:
    st.header("Supuestos mensuales")
    n = st.number_input("Consultas mensuales", 1, 1_000_000, 1200, 100)
    cov = st.slider("Proporción cubierta por FAQs", 0.0, 1.0, 0.60, 0.05)
    manual = st.number_input("Minutos por consulta manual", 0.5, 120.0, 8.0, 0.5)
    abel = st.number_input("Minutos por consulta con ABEL", 0.0, 120.0, 2.0, 0.5)
    wage = st.number_input("Costo por hora (moneda local)", 0.0, 100_000.0, 250.0, 25.0)
    opcost = st.number_input("Costo mensual de operación", 0.0, 10_000_000.0, 8000.0, 500.0)
    setup = st.number_input("Costo inicial", 0.0, 10_000_000.0, 35000.0, 2500.0)
    runs = st.select_slider(
        "Corridas Monte Carlo",
        options=[1000, 5000, 10000, 25000, 50000],
        value=10000,
    )
    seed = st.number_input("Semilla reproducible", 1, 999999, 42)

hours = n * cov * max(manual - abel, 0) / 60
gross = hours * wage
net = gross - opcost
roi = (net / opcost * 100) if opcost else float("nan")

st.subheader("Indicadores estimados")
a, b, c, d = st.columns(4)
a.metric("Consultas cubiertas", f"{n * cov:,.0f}", f"{cov:.0%} del volumen")
b.metric("Horas potencialmente liberadas", f"{hours:,.1f} h/mes")
c.metric("Ahorro bruto estimado", f"{gross:,.0f}/mes")
d.metric("Balance mensual estimado", f"{net:,.0f}/mes")
st.caption(
    "El tiempo liberado representa capacidad potencial que puede reasignarse; "
    "no implica automáticamente ahorro de caja."
)

st.divider()
st.subheader("Simulación Monte Carlo")
st.write(
    "Distribuciones triangulares para volumen, cobertura, duración de atención "
    "y costo operativo. Ajuste los supuestos con mediciones reales."
)

rng = np.random.default_rng(int(seed))
vol = rng.triangular(max(1, n * 0.75), n, n * 1.30, int(runs))
coverage = rng.triangular(max(0, cov - 0.15), cov, min(1, cov + 0.15), int(runs))
tm = rng.triangular(max(0.5, manual * 0.7), manual, manual * 1.35, int(runs))
ta = rng.triangular(max(0, abel * 0.5), abel, abel * 1.75 + 0.1, int(runs))
cost = rng.triangular(opcost * 0.8, opcost, opcost * 1.25 + 1, int(runs))

saved = vol * coverage * np.maximum(tm - ta, 0) / 60
balance = saved * wage - cost
roi_sim = np.where(cost > 0, balance / cost * 100, np.nan)
p5, p50, p95 = np.percentile(balance, [5, 50, 95])
prob = (balance > 0).mean() * 100

x, y, z, w = st.columns(4)
x.metric("Balance P50", f"{p50:,.0f}")
y.metric("Intervalo P5–P95", f"{p5:,.0f} a {p95:,.0f}")
z.metric("Prob. balance positivo", f"{prob:.1f}%")
w.metric("Horas liberadas P50", f"{np.percentile(saved, 50):,.1f}")

df = pd.DataFrame({
    "Balance mensual": balance,
    "Horas liberadas": saved,
    "ROI mensual (%)": roi_sim,
})

fig = px.histogram(
    df,
    x="Balance mensual",
    nbins=45,
    title="Distribución simulada del balance mensual",
    color_discrete_sequence=["#2378F7"],
)
fig.add_vline(
    x=0,
    line_dash="dash",
    line_color="#E5484D",
    annotation_text="Punto de equilibrio",
)
fig.update_layout(
    paper_bgcolor="#F3F8FF",
    plot_bgcolor="#FFFFFF",
    font_color="#183568",
)
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    hours_fig = px.histogram(
        df,
        x="Horas liberadas",
        nbins=40,
        title="Horas potencialmente liberadas",
        color_discrete_sequence=["#54B8FF"],
    )
    hours_fig.update_layout(
        paper_bgcolor="#F3F8FF",
        plot_bgcolor="#FFFFFF",
        font_color="#183568",
    )
    st.plotly_chart(hours_fig, use_container_width=True)

with right:
    summary = pd.DataFrame({
        "Indicador": ["Balance mensual", "Horas liberadas", "ROI mensual (%)"],
        "P5": [
            np.percentile(balance, 5),
            np.percentile(saved, 5),
            np.nanpercentile(roi_sim, 5),
        ],
        "P50": [
            np.percentile(balance, 50),
            np.percentile(saved, 50),
            np.nanpercentile(roi_sim, 50),
        ],
        "P95": [
            np.percentile(balance, 95),
            np.percentile(saved, 95),
            np.nanpercentile(roi_sim, 95),
        ],
    })
    st.dataframe(summary.round(2), use_container_width=True, hide_index=True)

st.subheader("Métricas técnicas que se deben medir")
st.dataframe(
    pd.DataFrame(
        [
            ["Precisión de recuperación", "Respuestas relevantes / respuestas entregadas", "Revisión humana de muestra etiquetada"],
            ["Tasa de cobertura", "Consultas respondidas / consultas evaluadas", "Logs y conjunto de prueba"],
            ["Abstención correcta", "Fuera de alcance rechazadas / fuera de alcance evaluadas", "Conjunto etiquetado"],
            ["Latencia p50/p95", "Tiempo de respuesta", "Logs de aplicación"],
            ["Tasa de error", "Solicitudes fallidas / solicitudes totales", "Logs de aplicación"],
            ["Disponibilidad", "Tiempo disponible / tiempo observado", "Monitorización"],
        ],
        columns=["Métrica", "Definición", "Fuente"],
    ),
    use_container_width=True,
    hide_index=True,
)

st.info(
    "Monte Carlo cuantifica incertidumbre bajo supuestos; no demuestra causalidad. "
    "Para medir impacto real, ejecutar un piloto con medición antes/después."
)
st.download_button(
    "Descargar muestra de simulación CSV",
    df.sample(min(1000, len(df)), random_state=int(seed)).to_csv(index=False).encode("utf-8"),
    "abel_monte_carlo_sample.csv",
    "text/csv",
)
