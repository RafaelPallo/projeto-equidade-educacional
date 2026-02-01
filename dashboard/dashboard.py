import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")
st.title("📊 DASHBOARD ENEM - EFICIÊNCIA!")

# DEBUG
st.sidebar.header("🔍 DEBUG")
files = os.listdir('.')
st.sidebar.text("Arquivos:")
for f in files:
    st.sidebar.text(f"  {f}")

# CARREGA
csv_file = 'microdados_atualizados.csv'
df = pd.read_csv(csv_file)
st.success(f"✅ {len(df)} alunos carregados!")

st.sidebar.success("✅ DADOS OK!")

# Sidebar filtro
st.sidebar.header("Filtros")
escola = st.sidebar.multiselect("Tipo Escola", df['TP_ESCOLA'].unique())
df_f = df[df['TP_ESCOLA'].isin(escola)]

# MAPA
col1, col2 = st.columns(2)
with col1:
    st.subheader("🗺️ Brasil")
    fig_map = px.scatter_geo(df_f, lat='latitude', lon='longitude', 
                            color='municipio', hover_name='municipio',
                            title="Municípios")
    st.plotly_chart(fig_map, use_container_width=True)

# PIZZA INTERNET
with col2:
    st.subheader("📱 % Internet")
    internet = df_f.groupby('municipio')['Score_Internet'].mean()*100
    fig_pie = px.pie(values=internet.values, names=internet.index, title="%")
    st.plotly_chart(fig_pie)

# BARRAS
st.subheader("📈 ISE vs Notas")
agg = df_f.groupby('municipio').agg({
    'ISE': 'mean', 'NU_NOTA_GERAL': 'mean'
}).round(1)
fig_bar = px.bar(agg, barmode='group', title="Eficiência")
st.plotly_chart(fig_bar)

# TABELA
st.subheader("📋 Resumo")
st.dataframe(agg)
