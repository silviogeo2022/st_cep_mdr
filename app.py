import streamlit as st
import pandas as pd
import folium
import streamlit.components.v1 as components
import os

# Configuração da página
st.set_page_config(page_title="Mapa de CEPs", layout="wide")

# --- CABEÇALHO COM LOGO AJUSTADA ---
col_header_1, col_header_2 = st.columns([6, 1]) 

with col_header_1:
    # Título com ajuste de altura para alinhar verticalmente com a logo
    st.markdown("<h1 style='margin-top: 0px;'>📍 Atualização de CEPs em Mãe do Rio - PA</h1>", unsafe_allow_html=True)

with col_header_2:
    if os.path.exists("logo.png"):
        # width=150 reduz a imagem significativamente
        st.image("logo.png", width=150) 
    else:
        st.warning("logo.png não encontrada")

# --- CSS para a tabela ---
st.markdown("""
<style>
    table {width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px;}
    th {background-color: #f0f2f6; color: #31333F; padding: 10px; border-bottom: 2px solid #ddd; text-align: left;}
    td {padding: 8px; border-bottom: 1px solid #ddd; color: #31333F;}
    tr:nth-child(even) {background-color: #f9f9f9;}
    tr:hover {background-color: #f1f1f1;}
</style>
""", unsafe_allow_html=True)

# --- 1. Carregamento dos Dados ---
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("dataset.xlsx")
        df.columns = df.columns.str.strip()
        df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
        df = df.dropna(subset=['Latitude', 'Longitude'])
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- 2. Filtros ---
    st.sidebar.header("Filtros")

    # Bairro
    lista_bairros = ['Todos'] + sorted(df['Bairro'].unique().tolist())
    bairro_selecionado = st.sidebar.selectbox("Selecione o Bairro", options=lista_bairros)
    df_temp = df if bairro_selecionado == 'Todos' else df[df['Bairro'] == bairro_selecionado]

    # Tipo
    lista_tipos = ['Todos'] + sorted(df_temp['Tipo'].unique().tolist())
    tipo_selecionado = st.sidebar.selectbox("Selecione o Tipo", options=lista_tipos)
    if tipo_selecionado != 'Todos': df_temp = df_temp[df_temp['Tipo'] == tipo_selecionado]

    # Logradouro
    lista_logradouros = ['Todos'] + sorted(df_temp['Logradouro'].unique().tolist())
    logradouro_selecionado = st.sidebar.selectbox("Selecione o Logradouro", options=lista_logradouros)

    # Filtragem Final
    df_final = df.copy()
    if bairro_selecionado != 'Todos': df_final = df_final[df_final['Bairro'] == bairro_selecionado]
    if tipo_selecionado != 'Todos': df_final = df_final[df_final['Tipo'] == tipo_selecionado]
    if logradouro_selecionado != 'Todos': df_final = df_final[df_final['Logradouro'] == logradouro_selecionado]

    # --- 3. Exibição ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader(f"Resultados: {len(df_final)}")
        if not df_final.empty:
            tabela_html = df_final[['CEP', 'Tipo', 'Logradouro', 'Bairro']].head(50).to_html(index=False, classes='minimalistBlack')
            st.markdown(tabela_html, unsafe_allow_html=True)
            if len(df_final) > 50: st.caption("⚠️ Exibindo apenas os primeiros 50 resultados.")
        else:
            st.warning("Nenhum dado encontrado.")

    with col2:
        st.subheader("Mapa")
        if not df_final.empty:
            try:
                lat_media = df_final['Latitude'].mean()
                lon_media = df_final['Longitude'].mean()
                
                m = folium.Map(location=[lat_media, lon_media], zoom_start=14)

                limit = 200
                for idx, row in df_final.head(limit).iterrows():
                    folium.Marker(
                        [row['Latitude'], row['Longitude']],
                        popup=f"<b>{row['Tipo']} {row['Logradouro']}</b><br>CEP: {row['CEP']}",
                        tooltip=row['Logradouro'],
                        icon=folium.Icon(color="blue", icon="info-sign")
                    ).add_to(m)

                mapa_html = m.get_root().render()
                components.html(mapa_html, height=500)
                
            except Exception as e:
                st.error(f"Erro ao gerar mapa: {e}")
        else:
            st.info("Selecione filtros para visualizar o mapa.")
else:
    st.info("Aguardando dados...")