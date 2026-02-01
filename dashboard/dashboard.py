import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Carrega os dados
@st.cache_data
def load_data():
    return pd.read_csv('microdados_atualizados.csv')

df = load_data()

# Configuração da página
st.set_page_config(page_title="Dashboard ENEM - Eficiência por Município", layout="wide")
st.title("📊 Dashboard: Eficiência Educacional no ENEM por Município")
st.markdown("Análise de notas ENEM ajustadas por ISE e fatores socioeconômicos em 5 capitais brasileiras.")

# Sidebar para filtros
st.sidebar.header("Filtros")
tp_escola = st.sidebar.multiselect("Tipo de Escola", options=df['TP_ESCOLA'].unique(), default=df['TP_ESCOLA'].unique())
df_filtered = df[df['TP_ESCOLA'].isin(tp_escola)]

# Dados agregados
agg_df = df_filtered.groupby('municipio').agg({
    'ISE': 'mean',
    'Score_Renda': 'mean',
    'Score_Escolaridade': 'mean',
    'Score_Internet': 'mean',
    'NU_NOTA_GERAL': 'mean'
}).round(2).reset_index()

mun_order = ['Belo Horizonte', 'Fortaleza', 'Manaus', 'Rio de Janeiro', 'São Paulo']

# Row 1: Mapa + Pizza Internet
col1, col2 = st.columns(2)

with col1:
    st.subheader("🗺️ Localização dos Municípios")
    fig_map = px.scatter_geo(
        df_filtered, lat='latitude', lon='longitude',
        hover_name='municipio', color='municipio',
        projection='natural earth', title="Municípios no Brasil",
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig_map.update_layout(height=400)
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("📱 % Acesso à Internet (Q025)")
    tem_internet_pct = df_filtered.groupby('municipio')['Score_Internet'].mean().reindex(mun_order) * 100
    fig_pie = px.pie(values=tem_internet_pct.values, names=tem_internet_pct.index,
                      title="Média Score Internet por Município (%)",
                      color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

# Row 2: Barras Horizontais Contagem ISE
st.subheader("📈 Contagens por Score ISE Médio")
fig_hbar = go.Figure()
for score in ['ISE', 'Score_Renda', 'Score_Escolaridade']:
    fig_hbar.add_trace(go.Bar(
        y=agg_df['municipio'].reindex(mun_order), x=agg_df[score].reindex(mun_order),
        name=score.replace('Score_', '').replace('_', ' '), orientation='h',
        marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'][list(agg_df.columns).index(score)-1]
    ))
fig_hbar.update_layout(barmode='group', height=400, xaxis_title="Score Médio", yaxis_title="Município")
st.plotly_chart(fig_hbar, use_container_width=True)

# Row 3: Gráficos de Linha e Barras Verticais para Nota e Eficiência
col3, col4 = st.columns(2)

with col3:
    st.subheader("📉 Evolução Nota ENEM Média (simulada por ISE)")
    # Simula linha decrescente baseada em ISE (como na imagem)
    fig_line = make_subplots(specs=[[{"secondary_y": False}]])
    fig_line.add_trace(go.Scatter(x=agg_df['ISE'].reindex(mun_order), y=agg_df['NU_NOTA_GERAL'].reindex(mun_order),
                                  mode='lines+markers', name='Nota vs ISE'), secondary_y=False)
    fig_line.update_xaxes(title="Média ISE")
    fig_line.update_yaxes(title="Média Nota ENEM")
    fig_line.update_layout(height=350, title="Nota ENEM por Nível ISE")
    st.plotly_chart(fig_line, use_container_width=True)

with col4:
    eficiencia = (agg_df['NU_NOTA_GERAL'] / (agg_df['ISE'] + 1)).round(0)  # +1 para evitar divisão zero
    st.subheader("🏆 Eficiência (Nota / ISE)")
    fig_bar_eff = px.bar(x=agg_df['municipio'].reindex(mun_order), y=eficiencia.reindex(mun_order),
                         title="Eficiência Educacional por Município",
                         color=eficiencia.reindex(mun_order), color_continuous_scale='viridis')
    st.plotly_chart(fig_bar_eff, use_container_width=True)

# Tabela de Insights
st.subheader("📋 Resumo Estatístico")
st.dataframe(agg_df.reindex(mun_order)[['municipio', 'ISE', 'NU_NOTA_GERAL', 'Score_Internet']].style.highlight_max(axis=0, color='lightgreen'))

# Métricas chave
col5, col6, col7, col8 = st.columns(4)
col5.metric("Média Geral ISE", f"{agg_df['ISE'].mean():.1f}")
col6.metric("Média Nota ENEM", f"{agg_df['NU_NOTA_GERAL'].mean():.0f}")
col7.metric("Top Eficiência", agg_df.loc[agg_df['municipio'].isin(mun_order), 'municipio'][eficiencia.reindex(mun_order).idxmax()])
col8.metric("Maior % Internet", f"{tem_internet_pct.max():.0f}% ({tem_internet_pct.idxmax()})")

st.markdown("---")
st.caption("Dashboard criado com Streamlit e Plotly. Dados: microdados_atualizados.csv | Foco: Eficiência para bonificações justas.")[file:3]
