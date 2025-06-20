import streamlit as st
import pandas as pd
import plotly.express as px

def clasificar_grupo(p):
    if p <= 15:
        return "Bajo"
    elif p <= 30:
        return "Medio"
    elif p <= 40:
        return "Alto"
    else:
        return "Muy Alto"

def clasificar_total(p):
    if p <= 75:
        return "Bajo"
    elif p <= 150:
        return "Medio"
    elif p <= 200:
        return "Alto"
    else:
        return "Muy Alto"


st.set_page_config(page_title="Riesgo Psicosocial", layout="wide")


st.markdown("""
    <style>
        .stApp {
            background-image: url("https://www.ixpap.com/images/2021/02/pink-wallpaper-ixpap-5.jpg");
            background-size: cover;
            background-position: center;
            font-family: 'Segoe UI', sans-serif;
            color: #1F2937;
        }

        h1, h2, h3 {
            font-weight: 600;
        }

    .bloque-central {
        background-color: rgba(255, 255, 255, 0.7);
        padding: 1.5rem;
        border-radius: 1.5rem;
        text-align: center;
        width: fit-content;
        min-width: 400px;
        margin: 2rem auto 1.5rem auto;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)


if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
if "df" not in st.session_state:
    st.session_state.df = None
if "seleccion" not in st.session_state:
    st.session_state.seleccion = None


if st.session_state.pagina == "inicio":

    st.markdown("""
    <div class="bloque-central">
        <h2>👋 ¡Bienvenida, psicóloga Laura!</h2>
        <h1>🧠 Evaluación de Riesgo Psicosocial</h1>
        <p><em>Tu herramienta para visualizar los resultados de forma clara, profesional y rápida.</em></p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown("<p style='font-size: 1.2rem; font-weight: bold; margin-bottom: 0.99rem; color: #1F2937;'>- Sube tu archivo CSV para analizar 📄</p>", unsafe_allow_html=True)
    archivo = st.file_uploader(label="", type="csv")


    if archivo:
        df = pd.read_csv(archivo, sep=';')
        print(dir(st))
        columnas_necesarias = ['nombre'] + [f'p{i}' for i in range(1, 26)]

        if not all(col in df.columns for col in columnas_necesarias):
            st.error("❌ El archivo debe tener columnas: 'nombre', 'p1' a 'p25'")
        else:
            df = df[columnas_necesarias]

            df['Grupo1'] = df[[f'p{i}' for i in range(1, 6)]].sum(axis=1)
            df['Grupo2'] = df[[f'p{i}' for i in range(6, 11)]].sum(axis=1)
            df['Grupo3'] = df[[f'p{i}' for i in range(11, 16)]].sum(axis=1)
            df['Grupo4'] = df[[f'p{i}' for i in range(16, 21)]].sum(axis=1)
            df['Grupo5'] = df[[f'p{i}' for i in range(21, 26)]].sum(axis=1)
            df['Total'] = df[['Grupo1','Grupo2','Grupo3','Grupo4','Grupo5']].sum(axis=1)

            df['Riesgo_Grupo1'] = df['Grupo1'].apply(clasificar_grupo)
            df['Riesgo_Grupo2'] = df['Grupo2'].apply(clasificar_grupo)
            df['Riesgo_Grupo3'] = df['Grupo3'].apply(clasificar_grupo)
            df['Riesgo_Grupo4'] = df['Grupo4'].apply(clasificar_grupo)
            df['Riesgo_Grupo5'] = df['Grupo5'].apply(clasificar_grupo)
            df['Riesgo_Total'] = df['Total'].apply(clasificar_total)

            st.session_state.df = df
            st.session_state.pagina = "resumen"
            st.rerun()


elif st.session_state.pagina == "resumen":
    df = st.session_state.df

    st.markdown("""
    <div class="bloque-central">
        <h1>📊 Resumen General de Resultados</h1>
    </div>
    """, unsafe_allow_html=True)

    def color_riesgo(val):
        estilos = {
            "Bajo": "background-color: #FFCCCC; color: #990000;",         
            "Medio": "background-color: #FFFF99; color: #666600;",        
            "Alto": "background-color: #CCFFCC; color: #006600;",         
            "Muy Alto": "background-color: #CCE5FF; color: #003366;"      
        }
        return estilos.get(val, "")


    styled_df = df[['nombre', 'Total', 'Riesgo_Total']].style.applymap(color_riesgo, subset=['Riesgo_Total'])
    st.dataframe(styled_df, use_container_width=True)

    st.markdown("""
    <div class="bloque-central">
        <h2 style='margin-bottom: 1rem;'>📈 Tendencia de Puntajes</h2>
    """, unsafe_allow_html=True)

    fig = px.bar(
        df, x='nombre', y='Total',
        color='Riesgo_Total',
        color_discrete_map={
            "Bajo": "#FF9999",
            "Medio": "#FFEB99",
            "Alto": "#A6F1A6",
            "Muy Alto": "#A3D2FF"
        }
    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="bloque-central">
        <h2 style='margin-bottom: 1rem;'>🔍 Detalle por Persona</h2>
    """, unsafe_allow_html=True)

    seleccion = st.selectbox("", df['nombre'])
    if st.button("Ver detalle"):
        st.session_state.seleccion = seleccion
        st.session_state.pagina = "detalle"
        st.rerun()

    st.markdown("---")
    if st.button("🔁 Subir otro archivo"):
        st.session_state.pagina = "inicio"
        st.session_state.df = None
        st.rerun()

elif st.session_state.pagina == "detalle":
    df = st.session_state.df
    persona = df[df['nombre'] == st.session_state.seleccion].iloc[0]

    st.title(f"👤 Detalle de {persona['nombre']}")
    st.markdown(f"""
    - **Grupo 1**: {persona['Grupo1']} – *{persona['Riesgo_Grupo1']}*
    - **Grupo 2**: {persona['Grupo2']} – *{persona['Riesgo_Grupo2']}*
    - **Grupo 3**: {persona['Grupo3']} – *{persona['Riesgo_Grupo3']}*
    - **Grupo 4**: {persona['Grupo4']} – *{persona['Riesgo_Grupo4']}*
    - **Grupo 5**: {persona['Grupo5']} – *{persona['Riesgo_Grupo5']}*

    ---
    - 🎯 **Total**: {persona['Total']}
    - 🟡 **Riesgo Total**: **{persona['Riesgo_Total']}**
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("⬅️ Volver al resumen"):
        st.session_state.pagina = "resumen"
        st.rerun()
