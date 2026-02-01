import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Dashboard ENEM - Equidade Educacional")

@st.cache_data
def load_data():
    return pd.read_csv('microdados_atualizados.csv')

df = load_data()
st.success(f"✅ {len(df)} alunos carregados!")

# Sidebar
st.sidebar.header("Filtros")
escola = st.sidebar.multiselect("Tipo Escola", df['TP_ESCOLA'].unique(), default=df['TP_ESCOLA'].unique())
df_f = df[df['TP_ESCOLA'].isin(escola)]

mun_order = ['Belo Horizonte', 'Fortaleza', 'Manaus', 'Rio de Janeiro', 'São Paulo']

# Layout 2 colunas
col1, col2 = st.columns(2)
with col1:
    st.subheader("🗺️ Mapa Brasil")
    fig_map = px.scatter_geo(df_f, lat='latitude', lon='longitude', 
                             color='municipio', hover_name='municipio')
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("📱 % Internet")
    internet = df_f.groupby('municipio')['Score_Internet'].mean() * 100
    fig_pie = px.pie(values=internet.values, names=internet.index, title="%")
    st.plotly_chart(fig_pie, use_container_width=True)

# Eficiência
agg = df_f.groupby('municipio')[['ISE', 'NU_NOTA_GERAL']].mean().round(1)
efic = agg['NU_NOTA_GERAL'] / agg['ISE']
st.subheader("🏆 Eficiência (Nota/ISE)")
fig_bar = px.bar(x=efic.index, y=efic.values, 
                 color=efic.values, color_continuous_scale='viridis',
                 title="Maior = Belo Horizonte!")
st.plotly_chart(fig_bar)

# Tabela
st.subheader("📋 Resumo")
st.dataframe(agg)

st.caption("Dashboard para curso análise dados - Rafael Pallo")
