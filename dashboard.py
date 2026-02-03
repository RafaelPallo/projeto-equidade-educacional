import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Dashboard ENEM - Análise Socioeconômica", layout="wide")

# Função para carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv('enem_limpo(in).csv')
    return df

df = load_data()

# --- SIDEBAR (Filtros) ---
st.sidebar.header("Filtros")
uf_selecionada = st.sidebar.multiselect("Selecione o Estado (UF):", 
                                        options=df['UF'].unique(), 
                                        default=df['UF'].unique())

internet_filtro = st.sidebar.radio("Tem Internet?", options=['Todos', 'Sim', 'Não'])

# Aplicando filtros
df_filtered = df[df['UF'].isin(uf_selecionada)]
if internet_filtro != 'Todos':
    df_filtered = df_filtered[df_filtered['Tem_Internet'] == internet_filtro]

# --- TÍTULO ---
st.title("📊 Análise de Desempenho ENEM")
st.markdown("Esta aplicação apresenta uma visão dinâmica da relação entre fatores socioeconômicos e as notas do ENEM.")

# --- MÉTRICAS PRINCIPAIS (KPIs) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Alunos", f"{len(df_filtered)}")
col2.metric("Média Nota ENEM", f"{df_filtered['Nota_Enem'].mean():.1f}")
col3.metric("Média ISE (Índice Socioeconômico)", f"{df_filtered['ISE'].mean():.2f}")
col4.metric("PIB per Capita Médio", f"R$ {df_filtered['pib_per_capta'].mean():.2f}")

st.divider()

# --- GRÁFICOS INTERATIVOS ---
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("📍 Distribuição Geográfica")
    # Mapa de calor/pontos baseado em latitude e longitude
    fig_map = px.scatter_mapbox(df_filtered, 
                                lat="latitude", 
                                lon="longitude", 
                                color="Nota_Enem", 
                                size="ISE",
                                hover_name="Municipio",
                                color_continuous_scale=px.colors.sequential.Viridis,
                                zoom=3, 
                                height=400)
    fig_map.update_layout(mapbox_style="carto-positron")
    st.plotly_chart(fig_map, use_container_width=True)

with row1_col2:
    st.subheader("📈 Distribuição das Notas")
    fig_hist = px.histogram(df_filtered, x="Nota_Enem", 
                            nbins=30, 
                            color_discrete_sequence=['#636EFA'],
                            marginal="box") # Adiciona um boxplot no topo
    st.plotly_chart(fig_hist, use_container_width=True)

st.divider()

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("💰 ISE vs Nota do ENEM")
    st.markdown("Relação entre o Índice Socioeconômico e o desempenho.")
    fig_scatter = px.scatter(df_filtered, x="ISE", y="Nota_Enem", 
                             trendline="ols", # Linha de tendência
                             color="UF",
                             hover_data=['Municipio'])
    st.plotly_chart(fig_scatter, use_container_width=True)

with row2_col2:
    st.subheader("👩‍🏫 Escolaridade da Mãe vs Nota")
    # Agrupando por score de escolaridade da mãe
    avg_score_mae = df_filtered.groupby('Score_Escolaridade_Mae')['Nota_Enem'].mean().reset_index()
    fig_bar = px.bar(avg_score_mae, x='Score_Escolaridade_Mae', y='Nota_Enem',
                     text_auto='.1f',
                     labels={'Score_Escolaridade_Mae': 'Nível de Escolaridade da Mãe', 'Nota_Enem': 'Média da Nota'},
                     color='Nota_Enem',
                     color_continuous_scale='Blues')
    st.plotly_chart(fig_bar, use_container_width=True)

# --- TABELA DE DADOS ---
with st.expander("Visualizar Dados Brutos"):
    st.dataframe(df_filtered)

# Rodapé
st.caption("Desenvolvido para análise de dados educacionais.")
