import streamlit as st
from datetime import datetime, timedelta
from scraper import NoticiasScraper

st.set_page_config(
    page_title="Noticias MUTCHA INTELIGENCIA",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Noticias MUTCHA INTELIGENCIA")
st.markdown("### Scraping de noticias municipales de Nuevo León y Coahuila")

# Configuración de días
dias_historial = st.slider(
    "¿Cuántos días de historial deseas obtener?",
    min_value=1,
    max_value=30,
    value=7
)

# Mostrar URLs fuente
with st.expander("🔗 URLs fuente por municipio"):
    from utils import MUNICIPIOS_URLS
    st.json(MUNICIPIOS_URLS)

# Botón de inicio
if st.button("🚀 Iniciar Scraping", type="primary"):
    scraper = NoticiasScraper()
    with st.spinner("⏳ Procesando noticias..."):
        df = scraper.ejecutar(dias_historial)
        
    # Descarga CSV
    fecha_hoy = datetime.now().strftime("%Y%m%d")
    filename = f"REPORTENOTICIAS{fecha_hoy}.csv"
    st.download_button(
        label="📥 Descargar CSV",
        data=df.to_csv(index=False, encoding='utf-8-sig'),
        file_name=filename,
        mime="text/csv"
    )