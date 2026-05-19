# Dasboard Spotify Test

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Spotify QA Dashboard",
    page_icon="🎵",
    layout="wide",
)

# ─── SPOTIFY THEME ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Circular+Std:wght@400;700&family=DM+Mono:wght@400;500&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;900&family=DM+Mono&display=swap');

    html, body, [class*="css"] {
        background-color: #121212;
        color: #FFFFFF;
        font-family: 'Montserrat', sans-serif;
    }

    .stApp {
        background-color: #121212;
    }

    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #1DB954 0%, #158a3e 50%, #121212 100%);
        border-radius: 16px;
        padding: 36px 40px;
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 200px; height: 200px;
        background: rgba(255,255,255,0.05);
        border-radius: 50%;
    }
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 900;
        color: #FFFFFF;
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
    }
    .main-header p {
        font-size: 0.95rem;
        color: rgba(255,255,255,0.75);
        margin: 0;
        font-weight: 400;
    }
    .spotify-logo {
        font-size: 1rem;
        font-weight: 700;
        color: #1DB954;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    /* Sección títulos */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #FFFFFF;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 32px 0 16px 0;
        padding-left: 12px;
        border-left: 3px solid #1DB954;
    }

    /* Tarjetas KPI */
    .kpi-card {
        background: #1E1E1E;
        border-radius: 12px;
        padding: 20px 24px;
        border: 1px solid #2a2a2a;
        transition: border-color 0.2s;
        height: 100%;
    }
    .kpi-card:hover {
        border-color: #1DB954;
    }
    .kpi-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #b3b3b3;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
    }
    .kpi-value {
        font-size: 2.1rem;
        font-weight: 900;
        line-height: 1;
        margin-bottom: 8px;
    }
    .kpi-value.pass { color: #1DB954; }
    .kpi-value.fail { color: #E5344A; }
    .kpi-meta {
        font-size: 0.78rem;
        color: #727272;
        font-family: 'DM Mono', monospace;
    }
    .kpi-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 10px;
    }
    .badge-pass { background: rgba(29,185,84,0.15); color: #1DB954; }
    .badge-fail { background: rgba(229,52,74,0.15); color: #E5344A; }

    /* Separador */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, #1DB954, transparent);
        margin: 24px 0;
        border: none;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #535353;
        font-size: 0.75rem;
        margin-top: 48px;
        padding: 20px;
        border-top: 1px solid #2a2a2a;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── DATOS ─────────────────────────────────────────────────────────────────────
metrics = [
    {
        "label": "Tasa de Ejecución de Casos",
        "value": 100,
        "meta": 95,
        "meta_label": "Meta: ≥ 95%",
        "unit": "%",
        "higher_is_better": True,
        "formula": "(40 ejecutados / 40 totales) × 100"
    },
    {
        "label": "Tasa de Casos Aprobados",
        "value": 95,
        "meta": 90,
        "meta_label": "Meta: ≥ 90%",
        "unit": "%",
        "higher_is_better": True,
        "formula": "(38 pasaron / 40 ejecutados) × 100"
    },
    {
        "label": "Densidad de Defectos",
        "value": 0.05,
        "meta": 0.1,
        "meta_label": "Meta: < 0.1",
        "unit": "",
        "higher_is_better": False,
        "formula": "2 defectos / 40 casos ejecutados"
    },
    {
        "label": "Tasa de Casos Bloqueados",
        "value": 0,
        "meta": 5,
        "meta_label": "Meta: < 5%",
        "unit": "%",
        "higher_is_better": False,
        "formula": "(0 bloqueados / 40 ejecutados) × 100"
    },
    {
        "label": "Cobertura de Requisitos",
        "value": 100,
        "meta": 100,
        "meta_label": "Meta: 100%",
        "unit": "%",
        "higher_is_better": True,
        "formula": "(12 requisitos cubiertos / 12 totales) × 100"
    },
    {
        "label": "Casos en Ambas Plataformas",
        "value": 25,
        "meta": 90,
        "meta_label": "Meta: > 90%",
        "unit": "%",
        "higher_is_better": True,
        "formula": "(10 con paridad / 40 ejecutados) × 100"
    },
]

def cumple(m):
    if m["higher_is_better"]:
        return m["value"] >= m["meta"]
    else:
        return m["value"] < m["meta"]

# ─── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="spotify-logo">🎵 Spotify · Plan de Pruebas</div>
    <h1>Dashboard - Métricas de Calidad</h1>
    <p>Melissa Betancur, Sofia Betancur, Sebastian Echeverri, Juan Manuel Jaramillo, Emmanuel Mora Grajales</p>
</div>
""", unsafe_allow_html=True)

# ─── RESUMEN RÁPIDO ─────────────────────────────────────────────────────────────
cumplidas = sum(1 for m in metrics if cumple(m))
no_cumplidas = len(metrics) - cumplidas

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown(f"""
    <div class="kpi-card" style="text-align:center;">
        <div class="kpi-label">Total Métricas</div>
        <div class="kpi-value" style="color:#FFFFFF;">{len(metrics)}</div>
        <div class="kpi-meta">bajo análisis</div>
    </div>""", unsafe_allow_html=True)
with col_b:
    st.markdown(f"""
    <div class="kpi-card" style="text-align:center;">
        <div class="kpi-label">Métricas que Cumplen</div>
        <div class="kpi-value pass">{cumplidas}</div>
        <div class="kpi-meta">dentro de la meta</div>
    </div>""", unsafe_allow_html=True)
with col_c:
    st.markdown(f"""
    <div class="kpi-card" style="text-align:center;">
        <div class="kpi-label">Métricas Fuera de Meta</div>
        <div class="kpi-value fail">{no_cumplidas}</div>
        <div class="kpi-meta">requieren atención</div>
    </div>""", unsafe_allow_html=True)

# ─── TARJETAS KPI ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Detalle por Métrica</div>', unsafe_allow_html=True)

cols = st.columns(3)
for i, m in enumerate(metrics):
    ok = cumple(m)
    color_class = "pass" if ok else "fail"
    badge_class = "badge-pass" if ok else "badge-fail"
    badge_text = "✓ Cumple" if ok else "✗ No cumple"
    val_display = f"{m['value']}{m['unit']}"

    with cols[i % 3]:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{m['label']}</div>
            <div class="kpi-value {color_class}">{val_display}</div>
            <div class="kpi-meta">{m['meta_label']}</div>
            <div class="kpi-meta" style="margin-top:6px; font-size:0.68rem;">{m['formula']}</div>
            <span class="kpi-badge {badge_class}">{badge_text}</span>
        </div>
        <br/>
        """, unsafe_allow_html=True)

# ─── GRÁFICA DE BARRAS COMPARATIVA ─────────────────────────────────────────────
st.markdown('<div class="section-title">Valor Actual vs. Meta</div>', unsafe_allow_html=True)

labels = [m["label"] for m in metrics]
values = [m["value"] for m in metrics]
metas = [m["meta"] for m in metrics]
colors = ["#1DB954" if cumple(m) else "#E5344A" for m in metrics]

fig = go.Figure()

fig.add_trace(go.Bar(
    name="Valor Actual",
    x=labels,
    y=values,
    marker_color=colors,
    marker_line_color="rgba(0,0,0,0)",
    text=[f"{v}{m['unit']}" for v, m in zip(values, metrics)],
    textposition="outside",
    textfont=dict(color="#FFFFFF", size=12, family="Montserrat"),
))

fig.add_trace(go.Scatter(
    name="Meta",
    x=labels,
    y=metas,
    mode="markers+lines",
    marker=dict(color="#FFFFFF", size=8, symbol="diamond"),
    line=dict(color="rgba(255,255,255,0.4)", width=1.5, dash="dot"),
))

fig.update_layout(
    paper_bgcolor="#121212",
    plot_bgcolor="#1E1E1E",
    font=dict(family="Montserrat", color="#FFFFFF"),
    legend=dict(
        bgcolor="#1E1E1E",
        bordercolor="#2a2a2a",
        borderwidth=1,
        font=dict(size=11)
    ),
    xaxis=dict(
        tickfont=dict(size=10, color="#b3b3b3"),
        gridcolor="#2a2a2a",
        linecolor="#2a2a2a",
    ),
    yaxis=dict(
        gridcolor="#2a2a2a",
        linecolor="#2a2a2a",
        tickfont=dict(size=11, color="#b3b3b3"),
    ),
    bargap=0.35,
    height=420,
    margin=dict(t=30, b=10, l=10, r=10),
)

st.plotly_chart(fig, use_container_width=True)

# ─── GRÁFICA DE PASTEL: CUMPLIMIENTO GENERAL ───────────────────────────────────
st.markdown('<div class="section-title">Cumplimiento General</div>', unsafe_allow_html=True)

col_pie, col_detail = st.columns([1, 1])

with col_pie:
    fig_pie = go.Figure(go.Pie(
        labels=["Cumplen meta", "No cumplen meta"],
        values=[cumplidas, no_cumplidas],
        hole=0.6,
        marker=dict(colors=["#1DB954", "#E5344A"]),
        textfont=dict(family="Montserrat", size=12),
        hovertemplate="%{label}: %{value} métricas<extra></extra>",
    ))
    fig_pie.update_layout(
        paper_bgcolor="#121212",
        plot_bgcolor="#121212",
        font=dict(family="Montserrat", color="#FFFFFF"),
        legend=dict(bgcolor="#1E1E1E", bordercolor="#2a2a2a", borderwidth=1),
        height=300,
        margin=dict(t=20, b=20, l=20, r=20),
        annotations=[dict(
            text=f"<b>{round(cumplidas/len(metrics)*100)}%</b>",
            x=0.5, y=0.5,
            font=dict(size=26, color="#FFFFFF", family="Montserrat"),
            showarrow=False
        )]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_detail:
    st.markdown("<br><br>", unsafe_allow_html=True)
    for m in metrics:
        ok = cumple(m)
        icon = "🟢" if ok else "🔴"
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;
                    background:#1E1E1E; padding:10px 14px; border-radius:8px;">
            <span style="font-size:1.1rem;">{icon}</span>
            <div>
                <div style="font-size:0.8rem; font-weight:600; color:#FFFFFF;">{m['label']}</div>
                <div style="font-size:0.72rem; color:#b3b3b3; font-family:'DM Mono',monospace;">
                    Valor: {m['value']}{m['unit']} · {m['meta_label']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Pruebas de Software · Melissa Betancur, Sofia Betancur, Sebastian Echeverri, Juan Manuel Jaramillo, Emmanuel Mora Grajales, <br>
    Spotify QA Dashboard · Mayo 2026
</div>
""", unsafe_allow_html=True)