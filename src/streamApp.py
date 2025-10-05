import streamlit as st
from pathlib import Path
from streamlit.components.v1 import html

st.set_page_config(page_title="2Geopandas Viewer", layout="wide")
st.title("Geospatial Analysis of Hospitals in Peru")

SCRIPT_DIR = Path(__file__).parent.resolve()
CANDIDATE_BASES = [
    SCRIPT_DIR,            # .../src
    SCRIPT_DIR.parent,     # repo root
    Path.cwd().resolve(),  # cwd
]

def _resolve(relpath: str):
    tried = []
    for base in CANDIDATE_BASES:
        p = (base / relpath).resolve()
        tried.append(str(p))
        if p.exists():
            return p, tried
    return None, tried

def show_img(relpath: str):
    p, tried = _resolve(relpath)
    if p is None:
        st.error(f"❌ No encontrado: {relpath}\nProbé:\n- " + "\n- ".join(tried))
    else:
        st.image(str(p), use_container_width=True)
        st.caption(f"✓ {relpath} → {p}")

def show_html(relpath: str, height: int = 650):
    p, tried = _resolve(relpath)
    if p is None:
        st.error(f"❌ No encontrado: {relpath}\nProbé:\n- " + "\n- ".join(tried))
        return
    try:
        html(p.read_text(encoding="utf-8"), height=height, scrolling=True)
        st.caption(f"✓ {relpath} → {p}")
    except Exception as e:
        st.exception(e)

tab1, tab2, tab3 = st.tabs([
    "Data Desctription",
    "Static Maps & Department Analysis",
    "Dynamic Maps",
])

with tab1:
    # Texto + link (tal cual lo pediste)
    st.write("This application presents a geoespacial analyisis of hospital distribución in Peru.")
    st.markdown("Más información en https://github.com/qlabpucp/Python-Intermedio_Tarea-2")

    # Dos gráficos, cada uno al 50% del ancho (dos columnas)
    c1, c2 = st.columns(2)
    with c1:
        show_img("out/2geopandas/bars.png")
    with c2:
        show_img("out/2geopandas/mapaDEP.png")

with tab2:
    # map1, map2, map3 en 3 columnas lado a lado
    c1, c2, c3 = st.columns(3)
    with c1:
        show_img("out/2geopandas/map1.png")
    with c2:
        show_img("out/2geopandas/map2.png")
    with c3:
        show_img("out/2geopandas/map3.png")

    # Debajo, los folium (apilados)
    for f in [
        "out/2geopandas/folium_LIMA_1.html",
        "out/2geopandas/folium_LIMA_2.html",
        "out/2geopandas/folium_LORETO_1.html",
        "out/2geopandas/folium_LORETO_2.html",
    ]:
        show_html(f, height=650)

with tab3:
    for f in [
        "out/3folium/choropleth.html",
        "out/3folium/folium_completo.html",
    ]:
        show_html(f, height=700)

with st.expander("Debug rápido"):
    st.write("SCRIPT_DIR:", SCRIPT_DIR)
    st.write("CANDIDATE_BASES:", [str(x) for x in CANDIDATE_BASES])

