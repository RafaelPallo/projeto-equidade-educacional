import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

st.set_page_config(page_title="Dashboard ENEM", layout="wide")
st.title("📊 ENEM: Eficiência por Município")

# DEBUG - Mostra arquivos
st.sidebar.title("🔍 Debug")
arquivos = os.listdir('.')
st.sidebar.write("Arquivos aqui:", arquivos)
if 'microdados_atualizados.csv' in arquivos:
    st.sidebar.success("✅ CSV OK!")
else:
    st.error("❌ CSV faltando!")

# Carrega com segurança
try:
    df = pd.read_csv('microdados_atualizados.csv')
    st.success(f"✅ Dados carregados: {len(df)} linhas")
except:
    st.error("❌ Erro CSV. Verifique nome exato!")
    st.stop()

# Sidebar filtro
st.sidebar.header("Filtros")
tp_escola = st.sidebar.multiselect("Escola", df['TP_ESCOLA'].unique(), default=df['TP_ESCOLA'].unique())
df_f = df[df['TP_ESCOLA'].isin(tp_escola)]

# Agregado
agg = df_f.groupby('municipio').agg({
    'ISE': 'mean', 'Score_Renda': 'mean', 'Score_Escolaridade': 'mean', 
    'Score_Internet': 'mean', 'NU_NOTA_GERAL': 'mean'
}).round(2)

mun_order = ['Belo Horizonte', 'Fortaleza', 'Manaus', 'Rio de Janeiro', 'São Paulo']

# Row 1: Mapa + Pizza
col1, col2 = st.columns(2)
with col1:
    st.subheader("🗺️ Mapa")
    fig_map = px.scatter_geo(df_f, lat='latitude', lon='longitude', color='municipio', hover_name='municipio')
    st.plotly_chart(fig_map)

with col2:
    st.subheader("📱 Internet")
    internet = df_f.groupby('municipio')['Score_Internet'].mean() * 100
    fig_pie = px.pie(values=internet.values, names=internet.index, title="% Internet")
    st.plotly_chart(fig_pie)

# Row 2: Barras
st.subheader("📊 ISE/Renda/Escolaridade")
fig_bar = go.Figure()
for col in ['ISE', 'Score_Renda', 'Score_Escolaridade']:
    fig_bar.add_trace(go.Bar(x=agg.index, y=agg[col], name=col))
fig_bar.update_layout(barmode='group')
st.plotly_chart(fig_bar)

# Row 3: Eficiência
efic = agg['NU_NOTA_GERAL'] / (agg['ISE'] + 1)
st.subheader("🏆 Eficiência")
fig_eff = px.bar(x=efic.index, y=efic.values, title="Nota/ISE")
st.plotly_chart(fig_eff)

st.dataframe(agg)
