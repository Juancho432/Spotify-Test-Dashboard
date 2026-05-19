import streamlit as st
import plotly.graph_objects as go
import uuid

def circular_progress(
    value: float, 
    max_value: float = 100.0, 
    progress_color: str = "#00C0F2", 
    ring_color: str = "#333333", 
    text_color: str = "white",
    height: int = 300
):
    """
    Crea y renderiza una barra de progreso circular en Streamlit usando Plotly,
    con fondo transparente ideal para temas oscuros.
    
    Parámetros:
    - value: El valor actual del progreso.
    - max_value: El valor máximo posible (por defecto 100).
    - progress_color: Color de la barra de progreso (Hex o nombre de color).
    - ring_color: Color del fondo del anillo (la parte no completada).
    - text_color: Color del porcentaje en el centro.
    - height: Altura del gráfico en píxeles.
    """
    
    # Asegurarnos de que el valor no supere el máximo y calcular el porcentaje
    value = min(value, max_value)
    porcentaje = int((value / max_value) * 100)
    
    # Crear el gráfico de Dona
    fig = go.Figure(go.Pie(
        values=[value, max_value - value],
        hole=0.8,
        marker_colors=[progress_color, ring_color],
        textinfo='none',
        hoverinfo='none',
        direction='clockwise',
        sort=False
    ))

    # Agregar el texto central
    fig.add_annotation(
        text=f"<b>{porcentaje}%</b>",
        showarrow=False,
        font=dict(size=int(height * 0.15), color=text_color), # El texto escala con la altura
        x=0.5, y=0.5
    )

    # Configurar la transparencia y los márgenes
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",  
        margin=dict(t=10, b=10, l=10, r=10),
        height=height
    )

    # Renderizar directamente en Streamlit
    st.plotly_chart(fig, use_container_width=True, key = uuid.uuid4().hex)


if __name__ == "__main__":
    # Configuración de la página
    st.set_page_config(
        page_title="Spotify Dashboard",
        page_icon="🎵",
        layout="wide"
    )

    # Título principal
    st.title("Spotify Test Dashboard")
    st.divider()

    st.header("Tasa de Exito por Tipo de Prueba")
    # Espacio para gráficos y visualizaciones
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.subheader("Integracion", text_alignment="center")
        circular_progress(75, progress_color="#1DB954", height=150)
    with col2:
        st.subheader("Funcionales", text_alignment="center")
        circular_progress(100, progress_color="#1DB954", height=150)
    with col3:
        st.subheader("Regresion", text_alignment="center")
        circular_progress(100, progress_color="#1DB954", height=150)
    with col4:
        st.subheader("UAT", text_alignment="center")
        circular_progress(100, progress_color="#1DB954", height=150)

    st.divider()

    # Contenedor para métricas principales (KPIs)
    st.header("KPIs")
    
    # Inyectar CSS para cambiar el color de los valores de las métricas

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Tiempo Medio de Registro", value="120 Seg", delta = "-90 Seg")
    with col2:
        st.metric(label="Tiempo de Sincronizacion", value="1.5 Seg", delta = "3.5 Seg")
    with col3:
        st.metric(label="Clics antes de Reproduccion", value="3 Clics", delta = "2 Clics")

    

    