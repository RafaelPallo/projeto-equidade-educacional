# Projeto Equidade – Índice de Valor Adicionado (IVA)

Projeto de Data Science para políticas públicas em educação, focado na construção de um **Índice de Valor Adicionado (IVA)** para identificar escolas eficientes, descontando o contexto socioeconômico dos alunos.

## Contexto

Historicamente, o bônus de desempenho era distribuído com base apenas na nota bruta do ENEM, o que favorecia escolas em regiões mais ricas. O objetivo deste projeto é propor uma métrica de **eficiência educacional**, que considere a realidade socioeconômica e destaque escolas que geram grande aprendizado mesmo em contextos de vulnerabilidade.

## Objetivos do projeto

- Construir um **Índice Socioeconômico (ISE)** contínuo a partir do questionário do INEP.
- Enriquecer a base com indicadores municipais via **API do IBGE** (PIB per capita, população).
- Treinar um modelo de **Regressão Linear** para estimar a nota esperada de cada aluno.
- Calcular o **Valor Adicionado** (resíduo entre nota observada e nota prevista).
- Estruturar um **Data Warehouse** para análises históricas.
- Desenvolver um **dashboard em Power BI** para apoiar decisões da Secretaria de Educação.

## Stack e tecnologias

- Linguagem: Python
- Bibliotecas principais:
  - `pandas`, `numpy` – manipulação e vetorização de dados
  - `scikit-learn` – modelagem de regressão
  - `requests` – consumo de APIs (IBGE)
- Banco de dados / SQL:
  - Modelo dimensional com tabelas `DIM_ESCOLA` e `FACT_PERFORMANCE`
- Visualização:
  - Power BI (scatter plots, mapas, painéis gerenciais)

## Estrutura do repositório

- `data/`
  - `raw/` – microdados INEP, bases originais (não versionar dados sensíveis)
  - `processed/` – dados tratados com ISE e variáveis agregadas
- `notebooks/`
  - Análises exploratórias, testes de features e protótipos do modelo
- `src/`
  - `etl_edu.py` – pipeline ETL: leitura de CSV, engenharia do ISE, consumo da API do IBGE e geração da base final
  - `education_model.py` – treinamento da regressão linear, cálculo dos resíduos (IVA) e exportação dos resultados
- `dashboard/`
  - Arquivos `.pbix` e capturas de tela do painel de gestão
- `docs/`
  - Descrição metodológica, dicionário de dados, anotações de modelagem

## Lógica do Índice de Valor Adicionado

1. **ISE (Índice Socioeconômico)**
   - Transformação de respostas qualitativas do questionário (ex.: posse de bens, escolaridade dos pais) em um score numérico de 0 a 10.
2. **Enriquecimento via API IBGE**
   - Consulta a indicadores municipais (PIB per capita, população) a partir do município da escola.
3. **Modelo de Regressão Linear**
   - Features (X): ISE do aluno + variáveis de contexto (por exemplo, PIB da cidade).
   - Target (Y): Nota ENEM.
   - O modelo estima a **nota esperada** dado o contexto socioeconômico.
4. **Cálculo do Valor Adicionado**
   - Valor Adicionado = Nota Observada – Nota Esperada (resíduo da regressão).
   - Escolas com resíduos consistentemente positivos são consideradas mais eficientes.

## Modelo de dados (SQL / DW)

- `DIM_ESCOLA`
  - ID_Escola
  - Nome, Rede (Pública/Privada)
  - Município, UF
  - Coordenadas (Lat, Lon)
- `FACT_PERFORMANCE`
  - Ano
  - ID_Escola
  - Nota_Bruta_Media
  - ISE_Medio
  - Valor_Adicionado_Calculado

Esse modelo permite análises históricas e comparações entre redes, municípios e regiões.

## Dashboard (Power BI)

Principais elementos do painel:

- **Scatter Plot (Gráfico da “verdade”)**
  - Eixo X: Nível socioeconômico (ISE ou indicador agregado).
  - Eixo Y: Nota ENEM.
  - Linha de tendência: desempenho médio do estado.
  - Destaque para outliers positivos (escolas muito acima da linha).
- **Mapa de Equidade**
  - Mapa temático pintado pelo **Valor Adicionado** e não pela nota bruta.
  - Identificação de escolas públicas que superam privadas em eficiência.
- Filtros por:
  - Ano, rede, município, faixa de ISE, entre outros.

## Como executar (ambiente local)

1. Clonar o repositório:
   ```bash
   git clone https://github.com/[seu-usuario]/[nome-do-repositorio].git
   cd [nome-do-repositorio]
