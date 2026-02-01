import streamlit as st
import os

st.title("🔍 VERIFICAÇÃO ARQUIVOS")

st.header("Lista TODOS arquivos:")
for arquivo in os.listdir('.'):
    st.write(f"📄 **{arquivo}**")
    st.write(f"Tamanho: {os.path.getsize(arquivo)} bytes")

st.header("Testa CSV:")
csvs = [f for f in os.listdir('.') if f.endswith('.csv')]
st.write("**CSVs encontrados:**", csvs)

if csvs:
    primeiro_csv = csvs[0]
    st.success(f"🎉 Vou tentar carregar: {primeiro_csv}")
    
    import pandas as pd
    try:
        df = pd.read_csv(primeiro_csv)
        st.success(f"✅ SUCESSO! {len(df)} linhas, colunas: {list(df.columns)}")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"❌ Erro: {e}")
else:
    st.error("❌ NENHUM .csv!")
