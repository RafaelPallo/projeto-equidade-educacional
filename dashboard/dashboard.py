import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(layout="wide")
st.title("🎉 DASHBOARD ENEM - FUNCIONANDO!")

# DEBUG COMPLETO
st.sidebar.header("🔍 DEBUG")
files = os.listdir('.')
st.sidebar.write("**Arquivos encontrados:**")
for f in files:
    st.sidebar.write(f"• {f}")

# Lista TODOS CSVs possíveis
csv_possible = [f for f in files if 'micro' in f.lower() and f.endswith('.csv')]
st.sidebar.write("**CSVs possíveis:**", csv_possible)

# Tenta CARREGAR qualquer CSV
df = None
for csv_file in csv_possible:
    try:
        df = pd.read_csv(csv_file)
        st.sidebar.success(f"✅ {csv_file} = {len(df)} linhas!")
        st.success(f"Carregado: {csv_file}")
        break
    except Exception as e:
        st.sidebar.error(f"❌ {csv_file}: {e}")

if df is None:
    st.error("Nenhum CSV válido!")
    st.stop()

# Gráficos (se carregou)
if 'municipio' in df.columns:
    st.header("🗺️ MAPA")
    fig = px.scatter_geo(df, lat='latitude', lon='longitude', color='municipio')
    st.plotly_chart(fig)

    st.header("📊 DADOS")
    st.dataframe(df.head())
else:
    st.error("Colunas erradas!")
